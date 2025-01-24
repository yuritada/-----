import math
import requests
from bs4 import BeautifulSoup
from db import create_database, insert_data



def fetch_page_content(url):
    """指定されたURLのHTMLコンテンツを取得する"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None
    

def extract_room_names(soup):
    """部屋名を抽出する"""
    room_elements = soup.find_all(class_='js-cassetLinkHref')
    room_data = []
    for element in room_elements:
        name_info = element.get_text(strip=True)
        room_data.append(name_info)
    return room_data

def extract_distances(soup):
    """最寄り駅とそこからの距離を抽出する"""
    distance_data = []
    station_boxes = soup.find_all('div', class_='detailnote-box')
    for i,box in enumerate(station_boxes):
        if i % 2 == 0:
            box_div = box.find_next('div')
            for div in box_div:
                station_info = div.get_text(strip=True)
                station_info = ''.join(filter(str.isdigit, station_info))
                distance_data.append(station_info)
    return distance_data

def extract_ages(soup):
    """築年数を抽出する"""
    age_elements = soup.find_all(class_='detailbox-property-col detailbox-property--col3')
    age_data = []
    for idx, element in enumerate(age_elements):
        if idx % 2 != 0:
            age_text = element.get_text(strip=True)
            age = ''.join(filter(str.isdigit, age_text))
            age_data.append(age)
    return age_data

def extract_prices(soup):
    """家賃を抽出する"""
    price_elements = soup.find_all(class_='detailbox-property-point')
    price_data = []
    for element in price_elements:
        price_text = element.get_text(strip=True)
        price = ''.join(filter(lambda c: c.isdigit() or c == '.', price_text))
        price_data.append(price)
    return price_data

def scrape_property_details(base_url):
    """一つのサイトをスクレイピングするときのメインコード"""
    """指定されたURLから物件の詳細情報をスクレイピングする"""
    html_content = fetch_page_content(base_url)
    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    room_names = extract_room_names(soup)
    distances = extract_distances(soup)
    ages = extract_ages(soup)
    price = extract_prices(soup)

    homes_data = []

    for i in range(len(room_names)):
        home_data = [room_names[i], distances[i], ages[i], price[i]]
        homes_data.append(home_data)
    return homes_data

def save_to_database(output_data, db_name='properties.db'):
    """
    出力データをデータベースに保存するメイン関数
    :param output_data: [(room_name, distance, age, price), ...] のリスト
    :param db_name: データベースのファイル名
    """
    # データベースを初期化
    create_database(db_name)
    # データを挿入
    insert_data(db_name, output_data)


def roop_scrape(base_url):
    try:
        # 初回ページを取得
        response = requests.get(base_url)
        response.raise_for_status()
        
        # HTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        total_text = soup.find(class_="paginate_set-hit").get_text(strip=True)
        total_items = int(''.join(filter(str.isdigit, total_text)))
        print(f"Total items: {total_items}")
        
        # ページ数を計算 (1ページあたり100件)
        total_pages = math.ceil(total_items / 100)
        print(f"Total pages to scrape: {total_pages}")
        
        # 各ページのスクレイピング
        for page in range(1, total_pages + 1):
            print(f"Scraping page {page}...")
            
            # ページURLを生成 (例: `&page={page}` を追加)
            page_url = f"{base_url}&page={page}"
            output_data = scrape_property_details(page_url)
            # スクレイピング結果をデータベースに保存
            save_to_database(output_data, db_name='properties.db')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}, page = {page}")


if __name__ == "__main__":
    # スクレイピング対象のベースURLを指定
    base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0005&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&po2=99&pc=100"
    roop_scrape(base_url)
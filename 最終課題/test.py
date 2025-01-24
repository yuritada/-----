import math
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from db import create_database, insert_data

async def fetch_page_content(session, url):
    """非同期で指定されたURLのHTMLコンテンツを取得する"""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching the page: {e}, URL: {url}")
        return None

def extract_room_names(soup):
    """部屋名を抽出する"""
    room_elements = soup.find_all(class_='js-cassetLinkHref')
    return [element.get_text(strip=True) for element in room_elements]

def extract_distances(soup):
    """最寄り駅とそこからの距離を抽出する"""
    distance_data = []
    station_boxes = soup.find_all('div', class_='detailnote-box')
    for i, box in enumerate(station_boxes):
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
    return [
        ''.join(filter(str.isdigit, element.get_text(strip=True)))
        for idx, element in enumerate(age_elements) if idx % 2 != 0
    ]

def extract_prices(soup):
    """家賃を抽出する"""
    price_elements = soup.find_all(class_='detailbox-property-point')
    return [
        ''.join(filter(lambda c: c.isdigit() or c == '.', element.get_text(strip=True)))
        for element in price_elements
    ]

def parse_property_details(html):
    """HTMLから物件データを解析する"""
    soup = BeautifulSoup(html, 'html.parser')
    room_names = extract_room_names(soup)
    distances = extract_distances(soup)
    ages = extract_ages(soup)
    prices = extract_prices(soup)
    return [
        [room_names[i], distances[i], ages[i], prices[i]]
        for i in range(len(room_names))
    ]

async def scrape_property_details(base_url, page, session):
    """1ページのスクレイピング"""
    page_url = f"{base_url}&page={page}"
    html = await fetch_page_content(session, page_url)
    if html:
        return parse_property_details(html)
    return []

async def scrape_pages_in_batches(base_url, total_pages, batch_size=100, db_name='properties.db'):
    """100ページずつスクレイピングを実行"""
    create_database(db_name)

    async with aiohttp.ClientSession() as session:
        for start in range(1, total_pages + 1, batch_size):
            end = min(start + batch_size - 1, total_pages)
            print(f"Scraping pages {start} to {end}...")
            tasks = [scrape_property_details(base_url, page, session) for page in range(start, end + 1)]
            # バッチごとに非同期実行
            results = await asyncio.gather(*tasks)
            # データをデータベースに保存
            for result in results:
                insert_data(db_name, result)
            print(f"Batch {start}-{end} completed!")

async def main():
    base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0005&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&po2=99&pc=100"
    try:
        # 最初のページを取得して総ページ数を計算
        async with aiohttp.ClientSession() as session:
            html = await fetch_page_content(session, base_url)
            soup = BeautifulSoup(html, 'html.parser')
            total_text = soup.find(class_="paginate_set-hit").get_text(strip=True)
            total_items = int(''.join(filter(str.isdigit, total_text)))
            total_pages = min(math.ceil(total_items / 100), 1000)  # 最大1000ページ
            print(f"Total pages to scrape: {total_pages}")

        # 100ページずつスクレイピングを開始
        await scrape_pages_in_batches(base_url, total_pages, batch_size=100)

    except Exception as e:
        print(f"Error during scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main())
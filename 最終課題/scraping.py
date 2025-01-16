import math
import requests
from bs4 import BeautifulSoup

def scrape_all_text(base_url):
    try:
        # 初回ページを取得
        response = requests.get(base_url)
        response.raise_for_status()
        
        # HTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # "197753件" から数字部分を抽出
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
            page_response = requests.get(page_url)
            page_response.raise_for_status()
            
            # ページのHTMLを解析
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            
            # 必要な要素を抽出
            elements = page_soup.find_all(class_="js-cassetLinkHref")
            all_text = [element.get_text(strip=True) for element in elements]
            
            # 結果を保存
            with open(f'page_{page}_output.txt', 'w', encoding='utf-8') as f:
                for line in all_text:
                    f.write(line + '\n')
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")

if __name__ == "__main__":
    # スクレイピング対象のベースURLを指定
    base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0005&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&po2=99&pc=100"
    scrape_all_text(base_url)
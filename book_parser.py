import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import re

def parse_single_page(page_num):
    """Парсит одну страницу, возвращает данные с меткой страницы"""
    base_url = "https://books.toscrape.com"
    
    if page_num == 1:
        url = f"{base_url}/catalogue/category/books_1/index.html"
    else:
        url = f"{base_url}/catalogue/category/books_1/page-{page_num}.html"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        page_data = []
        for book in books:
            try:
                title = book.find('h3').find('a')['title']
                price = book.find('p', class_='price_color').get_text().strip()
                relative_link = book.find('h3').find('a')['href']
                
                # 🔥 ИСПРАВЛЕННО: Правильное формирование ссылки
                if relative_link.startswith('../../../'):
                    # Убираем все ../ и берем только конечный путь
                    clean_link = re.sub(r'\.\./', '', relative_link)
                    link = base_url + '/catalogue/' + clean_link
                elif relative_link.startswith('../../'):
                    clean_link = re.sub(r'\.\./', '', relative_link)
                    link = base_url + '/catalogue/' + clean_link
                else:
                    link = base_url + '/catalogue/' + relative_link
                
                # Убедимся что ссылка корректная
                link = link.replace('//catalogue', '/catalogue')
                
                page_data.append({
                    'page': page_num,
                    'title': title,
                    'price': price,
                    'link': link
                })
                
            except Exception as e:
                print(f"❌ Ошибка книги на странице {page_num}: {e}")
                continue
        
        print(f"✅ Страница {page_num}: {len(page_data)} книг")
        return page_data
        
    except Exception as e:
        print(f"❌ Ошибка страницы {page_num}: {e}")
        return []

def main():
    print("🚀 ЗАПУСК ПАРСЕРА С ПРАВИЛЬНЫМИ ССЫЛКАМИ")
    start_time = time.time()
    
    total_pages = 50
    all_books_data = []
    
    # Многопоточный сбор
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(parse_single_page, range(1, total_pages + 1)))
    
    # Собираем и сортируем
    for page_data in results:
        all_books_data.extend(page_data)
    
    all_books_data.sort(key=lambda x: x['page'])
    
    # Записываем
    with open('books_data.txt', 'w', encoding='utf-8') as f:
        for book in all_books_data:
            f.write(f"{book['title']}|Цена: {book['price']}|{book['link']}\n")


    
    print(f"\n🎯 Собрано {len(all_books_data)} книг за {time.time()-start_time:.2f} сек")
    print("📁 Файл: books_data.txt")

if __name__ == "__main__":
    main()
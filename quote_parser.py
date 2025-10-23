import requests
from parsel import Selector

def fixed_blind_analysis():
    """Исправленный слепой анализ с фиксированными именами файлов"""
    url = "https://quotes.toscrape.com/page/2/"
    
    try:
        response = requests.get(url)
        selector = Selector(response.text)
        
        print("🔍 Запускаем исправленный слепой анализ...")
        
        # 1. Ищем ВСЕ элементы с текстом "life"
        life_elements = selector.xpath('//*[text()="life"]')
        print(f"📌 Найдено элементов с текстом 'life': {len(life_elements)}")
        
        authors_data = []
        processed_containers = set()
        
        for life_element in life_elements:
            # 2. Поднимаемся к ближайшему контейнеру цитаты
            quote_container = life_element.xpath('./ancestor::div[1]')
            
            if not quote_container:
                continue
                
            container = quote_container[0]
            container_html = container.get()
            
            if container_html in processed_containers:
                continue
            processed_containers.add(container_html)
            
            # 3. Ищем автора
            author = container.xpath('.//*[contains(@class, "author")]/text()').get()
            if not author:
                author = container.xpath('.//small/text()').get()
            
            # 4. Ищем текст цитаты
            quote_text = container.xpath('.//*[contains(@class, "text")]/text()').get()
            
            # 5. Очищаем данные
            if author:
                author = author.strip()
                if author.lower().startswith('by '):
                    author = author[3:].strip()
            
            if quote_text:
                quote_text = quote_text.strip('“”')
            
            # 6. Добавляем только если есть оба поля
            if author and quote_text and len(author) > 3:
                authors_data.append({
                    'author': author,
                    'quote': quote_text,
                    'container_class': container.xpath('@class').get() or 'unknown',
                    'author_class': container.xpath('.//*[contains(@class, "author")]/@class').get() or 'unknown',
                    'text_class': container.xpath('.//*[contains(@class, "text")]/@class').get() or 'unknown'
                })
        
        # 7. Убираем дубликаты
        unique_authors = []
        seen = set()
        for data in authors_data:
            key = (data['author'], data['quote'][:100])
            if key not in seen:
                seen.add(key)
                unique_authors.append(data)
        
        # 8. Сохраняем результаты в ФИКСИРОВАННЫЕ файлы
        if unique_authors:
            # Файл с авторами (перезаписываем)
            with open('authors_with_life_tag.txt', 'w', encoding='utf-8') as f:
                for data in unique_authors:
                    f.write(f"Автор: {data['author']} | Цитата: {data['quote']}\n")
            
            # Файл с селекторами (перезаписываем)
            with open('xpath_selectors_used.txt', 'w', encoding='utf-8') as f:
                f.write("XPath-СЕЛЕКТОРЫ ИСПОЛЬЗОВАННЫЕ ДЛЯ ИЗВЛЕЧЕНИЯ ДАННЫХ:\n\n")
                f.write("Основная логика поиска:\n")
                f.write("1. Найти все элементы с текстом 'life': //*[text()='life']\n")
                f.write("2. Подняться к контейнеру: ./ancestor::div[1]\n")
                f.write("3. Найти автора: .//*[contains(@class, 'author')]/text()\n")
                f.write("4. Найти цитату: .//*[contains(@class, 'text')]/text()\n\n")
                
                f.write("ОБНАРУЖЕННЫЕ СТРУКТУРЫ:\n")
                for i, data in enumerate(unique_authors, 1):
                    f.write(f"\nАвтор {i}:\n")
                    f.write(f"  Класс контейнера: {data['container_class']}\n")
                    f.write(f"  Класс автора: {data['author_class']}\n")
                    f.write(f"  Класс текста: {data['text_class']}\n")
        
        print(f"✅ Анализ завершен. Найдено уникальных авторов: {len(unique_authors)}")
        for i, data in enumerate(unique_authors, 1):
            print(f"  {i}. {data['author']}")
            
        return unique_authors
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def simple_and_reliable_method():
    """Простой и надежный метод с фиксированными именами файлов"""
    url = "https://quotes.toscrape.com/page/2/"
    
    response = requests.get(url)
    selector = Selector(response.text)
    
    authors_data = []
    
    # Ищем все ссылки с тегом "life"
    life_tags = selector.xpath('//a[text()="life"]')
    
    for tag in life_tags:
        # Поднимаемся к div с классом quote
        quote_div = tag.xpath('./ancestor::div[contains(@class, "quote")]')
        
        if quote_div:
            author = quote_div.xpath('.//small[@class="author"]/text()').get()
            quote_text = quote_div.xpath('.//span[@class="text"]/text()').get()
            
            if author and quote_text:
                clean_quote = quote_text.strip('“”')
                authors_data.append(f"Автор: {author} | Цитата: {clean_quote}")
    
    # Убираем дубликаты
    unique_data = list(set(authors_data))
    
    if unique_data:
        # ПЕРЕЗАПИСЫВАЕМ те же файлы
        with open('authors_with_life_tag.txt', 'w', encoding='utf-8') as f:
            for data in unique_data:
                f.write(data + '\n')
        
        with open('xpath_selectors_used.txt', 'w', encoding='utf-8') as f:
            f.write("XPath-СЕЛЕКТОРЫ ИСПОЛЬЗОВАННЫЕ ДЛЯ ИЗВЛЕЧЕНИЯ ДАННЫХ:\n\n")
            f.write("//a[text()='life']/ancestor::div[contains(@class, 'quote')] - поиск цитат с тегом 'life'\n")
            f.write(".//small[@class='author']/text() - извлечение автора\n")
            f.write(".//span[@class='text']/text() - извлечение цитаты\n")
    
    return unique_data

if __name__ == "__main__":
    print("🚀 Запуск анализа с фиксированными файлами...")
    
    # Всегда используем простой метод (надежнее)
    result = simple_and_reliable_method()
    
    if result:
        print(f"✅ Успешно! Найдено авторов: {len(result)}")
        print("📁 Файлы сохранены:")
        print("   - authors_with_life_tag.txt")
        print("   - xpath_selectors_used.txt")
        for i, data in enumerate(result, 1):
            print(f"  {i}. {data}")
    else:
        print("❌ Не удалось найти данные")
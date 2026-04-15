#!/usr/bin/env python3

"""
Amazon Product Detail Page Scraper
Function: Get product information including ASIN, title, main image, star rating, sales volume, price, About This Item, and all variants
"""

import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import time
import random
import json
import sys


def scrape_amazon_product(asin):
    # ====================== User-Agent Pool ======================
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Edge/131.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Edge/130.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ]

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.amazon.com/",
        "Origin": "https://www.amazon.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "DNT": "1",
        "Cookie": "session-token=abc123; i18n-prefs=USD; x-wl-uid=123456",
        "X-Forwarded-For": "1.1.1.1"
    }

    session = requests.Session()
    time.sleep(random.uniform(0.5, 1.2))

    try:
        resp = None
        for attempt in range(2):
            try:
                resp = session.get(
                    f"https://www.amazon.com/dp/{asin}",
                    headers=headers,
                    timeout=25
                )
                resp.raise_for_status()
                break
            except Exception as e:
                if attempt == 1:
                    raise e
                time.sleep(1)

        soup = BeautifulSoup(resp.text, 'html.parser')
        tree = etree.HTML(resp.text)

        asin_value = asin

        # Extract title
        title = ''
        title_elements = tree.xpath('//*[@id="productTitle"]')
        if title_elements:
            title = title_elements[0].text.strip()
        else:
            title_element = soup.find('title')
            if title_element:
                title = title_element.text.replace('Amazon.com:', '').strip()

        # Extract main image
        main_image = ''
        image_element = soup.find('img', id='landingImage')
        if image_element and 'src' in image_element.attrs:
            main_image = image_element['src']

        # Extract star rating
        rating = ''
        rating_element = soup.find('span', class_='a-icon-alt')
        if rating_element:
            rating = rating_element.text

        # Extract price
        price = ''
        price_selectors = [
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            ".a-price span.a-offscreen",
            "#price_inside_buybox",
            ".a-price-whole"
        ]
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price = price_elem.get_text(strip=True)
                if price:
                    if not any(c in price for c in ['$', '€', '£', '¥', 'S$']):
                        price = '$' + price
                    break
        if not price:
            price_match = re.search(r'([$€£¥S$]\s*[\d,.]+)', resp.text)
            if price_match:
                price = price_match.group(1)

        # Extract About This Item
        about_this_item = []
        feature_bullets = soup.find('div', id='feature-bullets')
        if feature_bullets:
            bullets = feature_bullets.find_all('li')
            for bullet in bullets:
                text = bullet.text.strip()
                if text and len(text) > 10:
                    about_this_item.append(text)

        # Extract sales information
        sales = ''
        sales_elements = tree.xpath('//*[@id="social-proofing-faceout-title-tk_bought"]/span[1]')
        if sales_elements:
            sales = sales_elements[0].text.strip()
        else:
            sales_match = re.search(r'([\d,]+) bought in past month', resp.text)
            if sales_match:
                sales = sales_match.group(1) + ' bought in past month'

        # Extract variant information
        variants = {}
        variant_rows = soup.find_all('div', class_='inline-twister-row')

        for row in variant_rows:
            row_id = row.get('id', '')
            if row_id.startswith('inline-twister-row-'):
                variant_type = row_id.replace('inline-twister-row-', '')
                variant_options = []
                options = row.find_all('li', class_='inline-twister-swatch')

                for option in options:
                    img = option.find('img', class_='swatch-image')
                    if img and 'alt' in img.attrs:
                        value = img['alt'].strip()
                        if value and value not in variant_options:
                            variant_options.append(value)
                    else:
                        text_elem = option.find('span', class_='swatch-title-text-display')
                        if text_elem:
                            value = text_elem.text.strip()
                            if value and value not in variant_options:
                                variant_options.append(value)

                if variant_options:
                    variants[variant_type] = variant_options

        # Fallback for color and size
        color_variation = soup.find('div', id='variation_color_name')
        if color_variation:
            color_options = []
            color_selections = color_variation.find_all('span', class_='selection')
            for selection in color_selections:
                color = selection.text.strip()
                if color and color not in color_options:
                    color_options.append(color)
            if color_options:
                variants['color_name'] = color_options

        size_variation = soup.find('div', id='variation_size_name')
        if size_variation:
            size_options = []
            size_selections = size_variation.find_all('span', class_='selection')
            for selection in size_selections:
                size = selection.text.strip()
                if size and size not in size_options:
                    size_options.append(size)
            if size_options:
                variants['size_name'] = size_options

        product_info = {
            'asin': asin_value,
            'title': title,
            'mainImage': main_image,
            'rating': rating,
            'price': price,
            'aboutThisItem': about_this_item,
            'variants': variants,
            'sales': sales
        }

        print(json.dumps(product_info, indent=2, ensure_ascii=False))
        return product_info

    except Exception as e:
        print(f'Scraping failed: {str(e)}')
        return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python scrape_amazon.py <ASIN>')
        print('Example: python scrape_amazon.py B0BLCD42J7')
        sys.exit(1)

    asin = sys.argv[1]
    result = scrape_amazon_product(asin)

    if result is None:
        sys.exit(1)
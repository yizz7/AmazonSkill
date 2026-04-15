---
name: amazon-product-scraper
description: 爬取亚马逊产品详情页信息。当用户提供ASIN、亚马逊产品链接、或请求获取亚马逊产品详情、产品信息、爬取亚马逊时触发。支持提取ASIN、标题、主图、评分、销量、价格、About This Item和变体信息。
---

# Amazon Product Scraper

用于爬取亚马逊产品详情页的产品信息。

## 何时使用

当用户：

- 提供一个ASIN（如 `B0BLCD42J7`）
- 提供亚马逊产品链接（如 `https://www.amazon.com/dp/B0BLCD42J7`）
- 请求获取亚马逊产品详情、产品信息
- 请求爬取亚马逊产品数据
- 提到"亚马逊详情"、"产品详情页"等关键词

## 如何使用

### 输入

用户提供ASIN或亚马逊产品链接。从链接中提取ASIN的规则：

- `/dp/{ASIN}` 格式：ASIN是10位字母数字组合
- 例如 `https://www.amazon.com/dp/B0BLCD42J7` 的ASIN是 `B0BLCD42J7`

### 执行

使用脚本执行爬取：

```bash
python scripts/scrape_amazon.py <ASIN>
```

脚本位于（相对路径）：`/scripts/scrape_amazon.py`

### 输出

脚本返回JSON格式：

```json
{
  "asin": "B0BLCD42J7",
  "title": "产品标题",
  "mainImage": "https://...",
  "rating": "4.5 out of 5 stars",
  "price": "$29.99",
  "aboutThisItem": ["特点1", "特点2"],
  "variants": {
    "color_name": ["Black", "White"],
    "size_name": ["Small", "Medium"]
  },
  "sales": "1000+ bought in past month"
}
```

## 注意事项

- 爬取需要网络连接
- 有随机延迟（0.5-1.2秒）和重试机制防反爬
- 使用User-Agent池模拟不同浏览器
- 单次请求timeout为25秒

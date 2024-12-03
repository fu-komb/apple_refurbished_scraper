import requests
import json
from bs4 import BeautifulSoup

load_url = "https://www.apple.com/jp/shop/refurbished/iphone"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
product_list = soup.find("div", class_="rf-refurb-category-grid-no-js")
products = product_list.find_all("li")

WEB_HOOK_URL = "https://hooks.slack.com/services/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"


results = []
for p in products:
    results.append(
        {
            "product_name": p.find("a").text,
            "price": p.find("div", class_="as-price-currentprice").text.strip()
        }
    )

blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "📱 Apple Refurbished Products",
            "emoji": True
        }
    },
    {
        "type": "section",
        "fields": [
            {"type": "mrkdwn", "text": "*Product Name*"},
            {"type": "mrkdwn", "text": "*Price*"}
        ]
    },
    {"type": "divider"}
]

for item in results:
    blocks.append({
        "type": "section",
        "fields": [
            {"type": "mrkdwn", "text": item["product_name"]},
            {"type": "mrkdwn", "text": item["price"]}
        ]
    })

blocks.append({"type": "divider"})

payload = {
    "blocks": blocks
}

response = requests.post(WEB_HOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    print("Message posted successfully!")
else:
    print(f"Failed to post message: {response.status_code}, {response.text}")

import asyncio
import aiohttp
import os
import csv
import nest_asyncio
from pyppeteer import launch

nest_asyncio.apply()

async def scrape(result_file_name, url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})

    wrapper = await page.J(".wpgb-viewport")
    articles = await wrapper.JJ("article")

    result = await asyncio.gather(*[
        process_article(page, article) for article in articles
    ])

    await page.close()
    await browser.close()

    save_result(result, result_file_name)


async def process_article(page, article):
    # Credit Card Name
    h2_card_name = await article.J(".wpgb-block-1")
    a_card_name = await h2_card_name.JJ("a")
    card_name = await page.evaluate('(node) => node.innerText', a_card_name[0])

    # Welcome Bonus
    p_welcome_bonus = await article.J(".wpgb-block-2")
    welcome_bonus = await page.evaluate('(node) => node.innerText', p_welcome_bonus)

    # Minimum Spend
    p_minimum_spend = await article.J(".wpgb-block-4")
    minimum_spend = await page.evaluate('(node) => node.innerText', p_minimum_spend)

    # Annual fee
    p_annual_fee = await article.J(".wpgb-block-3")
    annual_fee = await page.evaluate('(node) => node.innerText', p_annual_fee)

    
    '''
    # Credit Card Image
    div_thumbnail = await article.J(".wpgb-card-media-thumbnail")
    a_image = await div_thumbnail.J("a")
    img_link = await page.evaluate('(node) => node.getAttribute("href")', a_image)

    formatted_card_name = format_string(card_name)
    img_name = f'./images/{formatted_card_name}-image.png'

    os.makedirs(os.path.dirname(img_name), exist_ok=True)

    await download_image(img_link, img_name)
    '''

    return {
        'cardName': card_name, 
        'minSpend': minimum_spend,
        'annualFee': annual_fee,
        'cardReward': welcome_bonus
        # 'cardImage': img_name
            }


async def download_image(img_url, img_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            with open(img_name, 'wb') as file:
                file.write(await response.read())


def format_string(string):
    formatted_str = ''.join(e for e in string if e.isalnum() or e.isspace())
    final_str = formatted_str.replace(' ', '-')
    return final_str

"""
def save_result(result, result_file_name):
    with open(f'{result_file_name}.json', 'w') as file:
        file.write(json.dumps(result))
"""

def save_result(result, result_file_name):
    with open(f'{result_file_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        if result:
            header = result[0].keys()
            writer.writerow(header)
            for row in result:
                writer.writerow(row.values())


async def main():
    result_file_name = 'cad-scrap-results'
    url = 'https://frugalflyer.ca/compare-credit-cards/'
    await scrape(result_file_name, url)

asyncio.get_event_loop().run_until_complete(main())
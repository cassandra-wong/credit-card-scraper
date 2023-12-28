# Credit Card Scraper

The simple webscraper visits <https://frugalflyer.ca> to pull down credit card details, including card name, welcome bonus, minimum spend, and annual fee. The information is cleaned and subsequently uploaded to [Google Sheet](https://docs.google.com/spreadsheets/d/1mMyF5-Pott-xsFB9unr600p1wmNG1C95LCKHvfxlzJQ/edit?usp=sharing).

## Usage

`scraper.py` serves the purpose of web scraping credit card details from the website <https://frugalflyer.ca>.

To scrap US credit cards instead, change the last code block to the following:

```python
async def main():
    result_file_name = 'us-scrap-results'
    url = 'https://frugalflyer.ca/compare-us-credit-cards/'
    await scrape(result_file_name, url)
```

`format.py` utilizes the Pandas library to analyze and format credit card rewards data obtained from a CSV file. The script includes functions for determining the issuing institution, calculating returns based on different reward programs, and formatting the results for further analysis.

`gsheet.py` facilitates the upload of the resulting CSV file containing scraped credit card information to a Google Sheets document, and changes the title of the sheet name to the date of the last update.

Learn more about Google Workspace [here](https://developers.google.com/workspace/guides/get-started) and Python API for Google Sheets [here](https://docs.gspread.org/en/latest/).

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
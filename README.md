# Nintendo Switch Games Scraper

This project scrapes the full Nintendo Switch game catalog from the official Nintendo Store. The site uses lazy loading and only renders a small portion of the list at a time, so the scraper scrolls through the entire page until all game cards are loaded.

Once everything is visible, the script extracts:
- Game title
- Price (including free titles)
- Product page URL

The output is saved to an Excel file so it can be used for collection tracking, price analysis, or anything else that’s easier to do in a spreadsheet.

## Requirements
- Python 3
- Selenium
- ChromeDriver
- pandas

## Running the scraper
1. Install dependencies
2. Update the ChromeDriver path in the script
3. Run `nintendo_scraper.py`


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# --- Setup Chrome ---
options = Options()
options.add_argument("--start-maximized")
# Uncomment below to run headless (no visible window)
# options.add_argument("--headless=new")

service = Service("C:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
  # <-- update this path
driver = webdriver.Chrome(service=service, options=options)

# --- Open Nintendo Store ---
print("Opening Nintendo Store...")
driver.get("https://www.nintendo.com/store/games/")

# --- Function to load all games automatically ---
def load_all_games(driver):
    start_time = time.time()
    last_count = 0
    same_count_rounds = 0

    while True:
        # Try clicking "Load more results" if it exists
        try:
            load_more = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Load more results')]]")
            driver.execute_script("arguments[0].click();", load_more)
            time.sleep(2)
        except:
            # No button found, scroll instead
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Count game cards
        cards = driver.find_elements(By.XPATH, "//a[@aria-label and contains(@href, '/store/products/')]")
        current_count = len(cards)

        # Print progress every 100 games
        if current_count % 100 == 0 and current_count != last_count:
            elapsed = time.time() - start_time
            minutes = elapsed / 60
            avg_time_per_game = elapsed / current_count if current_count > 0 else 0
            est_total = avg_time_per_game * 1073  # rough estimate for full scrape
            remaining = (est_total - elapsed) / 60
            print(f"Loaded {current_count} games so far... ({minutes:.1f} min elapsed, ~{remaining:.1f} min remaining)")

        # Check if count stopped increasing
        if current_count == last_count:
            same_count_rounds += 1
        else:
            same_count_rounds = 0

        last_count = current_count

        # Stop when no new games load for 5 rounds
        if same_count_rounds >= 5:
            total_time = (time.time() - start_time) / 60
            print(f"No more games loading. Finished scrolling ({current_count} total). Took {total_time:.1f} minutes.")
            break

# --- Run the loader ---
load_all_games(driver)

# --- Extract game data ---
print("Scraping game data...")
games = []
cards = driver.find_elements(By.XPATH, "//a[@aria-label and contains(@href, '/store/products/')]")

start_extract = time.time()
for i, card in enumerate(cards, start=1):
    name = card.get_attribute("aria-label")
    url = card.get_attribute("href")
    price = "N/A"

    # Try to find price span (includes "Free")
    try:
        price_element = card.find_element(By.XPATH, ".//span[contains(text(), '$') or contains(text(), 'Free')]")
        price = price_element.text
    except:
        # If no price, look for release date
        try:
            release_element = card.find_element(By.XPATH, ".//*[contains(text(), 'Releases')]")
            price = release_element.text
        except:
            price = "N/A"

    games.append({"Name": name, "Price": price, "URL": url})

    # Progress update every 100 games
    if i % 100 == 0:
        elapsed = (time.time() - start_extract) / 60
        print(f"Processed {i}/{len(cards)} games... ({elapsed:.1f} min elapsed)")

# --- Save to Excel ---
df = pd.DataFrame(games)
df.to_excel("nintendo_games.xlsx", index=False)
print("Scraping complete! Data saved to nintendo_games.xlsx")

# --- Close browser ---
driver.quit()

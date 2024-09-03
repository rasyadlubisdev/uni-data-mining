from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import time


# FUNGSI UNTUK SCRAPPER DATA
def scraper(url):
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)

        # Get the URL given
        driver.get(url)

        # Wait until the element with ID 'course-list' is present
        try:
            wait = WebDriverWait(driver, timeout=15)
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".ipc-metadata-list-summary-item.sc-10233bc-0.TwzGn.cli-parent",
                    )
                )
            )
        except Exception as e:
            raise LookupError(f"Error locating element: {e}")

        # Parse the page source with BeautifulSoup
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(20):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")

        # Prepare the variable for JSON data
        films = []

        for index, film in enumerate(
            soup.find_all(
                "li",
                class_="ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent",
            )
        ):
            # MENGEKSTRAK DATA YANG DIPERLUKAN
            film_title = film.find("h3", class_="ipc-title__text").text
            data_desc = film.find_all(
                "span", class_="sc-b189961a-8 hCbzGp cli-title-metadata-item"
            )
            release_year = data_desc[0].text
            movie_duration = data_desc[1].text
            age_rating = data_desc[2].text if len(data_desc) > 2 else ""
            star_rating = film.find("span", class_="ipc-rating-star--rating").text

            # MENAMBAHKAN DATA YANG TELAH DI SCRAPPING KE DALAM FILE JSON
            films.append(
                {
                    "TV SHOW NAME"    : film_title,
                    "TV SHOW RELEASE" : release_year,
                    "TV SHOW EPSIODES": movie_duration,
                    "AGE RATING"      : age_rating,
                    "TV SHOW RATING"  : star_rating,
                }
            )

        # Close the WebDriver
        driver.quit()

        return films

    except Exception as e:
        print("An error occurred: ", e)

        # Close the WebDriver
        driver.quit()


if __name__ == "__main__":
    # URL NAME
    url = "https://www.imdb.com/chart/toptv/"

    # Call the scraper function
    data = scraper(url)
    print(data)
    # scraper(url)

    # MENYIMPAN DATA KE JSON FILE
    with open("data_TVSHOWS.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Data telah selesai di scraped dan disimpan ke data_TVSHOWS.json.")
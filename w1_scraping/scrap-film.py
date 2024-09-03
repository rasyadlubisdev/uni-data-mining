from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

def scraper(url):
    try:
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        driver.get(url)

        try:
            wait = WebDriverWait(driver, timeout = 15)
            wait.until(EC.presence_of_element_located((By.ID, 'ipc-wrap-background-id')))
        except Exception as e:
            raise LookupError(f"Error locating element: {e}")
        
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        films = []

        for index, film in enumerate(soup.find_all('li', class_='ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent')):
            film_title = film.find('h3', class_='ipc-title__text').text
            data_desc = film.find_all('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')
            release_year = data_desc[0].text
            movie_duration = data_desc[1].text
            age_rating = data_desc[2].text if len(data_desc) > 1 else ""
            star_rating = film.find('span', class_='ipc-rating-star--rating').text

            if index == 58:
                break

            films.append({
                'Movie Name': film_title,
                'Movie Release': release_year,
                'Movie Duration': movie_duration,
                'Age Rating': age_rating,
                'Film Rating': star_rating,
            })

        driver.quit()

        return films
    
    except Exception as e:
        print('An error occurred: ', e)
        
        driver.quit()


if __name__ == '__main__':
    url = 'https://www.imdb.com/chart/top/'
    data = scraper(url)
    print(data)    

    with open('data_film.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Data telah selesai di scraped dan disimpan ke data_film.json.")

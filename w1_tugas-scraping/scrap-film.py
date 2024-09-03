from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import time

#FUNGSI UNTUK SCRAPPER DATA 
def scraper(url):
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        # Get the URL given
        driver.get(url)

        # Wait until the element with ID 'course-list' is present
        try:
            wait = WebDriverWait(driver, timeout = 15)
            wait.until(EC.presence_of_element_located((By.ID, 'ipc-wrap-background-id')))
        except Exception as e:
            raise LookupError(f"Error locating element: {e}")
        
        # Parse the page source with BeautifulSoup
        content = driver.page_source

        # last_height = driver.execute_script("return document.body.scrollHeight")
        # for _ in range(3):
        #     # Scroll down to bottom
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #     # Wait to load page
        #     time.sleep(2)

        #     # Calculate new scroll height and compare with last scroll height
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break

        soup = BeautifulSoup(content, 'html.parser')

        # Prepare the variable for JSON data
        films = []

        # Find all containers that might contain motorcycle information
        for index, film in enumerate(soup.find_all('li', class_='ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent')):
            # Extracting the required data
            film_title = film.find('h3', class_='ipc-title__text').text
            data_desc = film.find_all('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')
            release_year = data_desc[0].text
            movie_duration = data_desc[1].text
            age_rating = data_desc[2].text if len(data_desc) > 1 else ""
            star_rating = film.find('span', class_='ipc-rating-star--rating').text
            # print(film_title)
            # print(data_desc[0].text)
            # print(data_desc[1].text)
            # print(data_desc[2].text if len(data_desc) > 1 else "")

            if index == 58:
                break

            # try:
            #     film_title = film.find('h3', class_='ipc-title__text').text
            #     # data_desc = film.soup.findAll('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')
            #     # release_year = film.soup.find('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')
            #     # movie_duration = film.soup.find('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')
            #     # age_rating = film.soup.find('span', class_= 'sc-b189961a-8 hCbzGp cli-title-metadata-item')
            #     star_rating = film.find('span', class_='ipc-rating-star--rating').text
            # except AttributeError as e:
            #     print(f"Error parsing IMDb Top 250 Movies data: {e}")
            #     continue

            #MENAMBAHKAN DATA YANG TELAH DI SCRAPPING KE DALAM FILE JSON
            # print("THIS IS FILM", film)
            films.append({
                'Movie Name': film_title,
                'Movie Release': release_year,
                'Movie Duration': movie_duration,
                'Age Rating': age_rating,
                'Film Rating': star_rating,
            })

        #Close the WebDriver
        driver.quit()

        # print(films)

        return films
    
    except Exception as e:
        # Print the error message
        print('An error occurred: ', e)
        
        # Close the WebDriver
        driver.quit()


if __name__ == '__main__':
    # Define the URL
    url = 'https://www.imdb.com/chart/top/'
    
    # Call the scraper function
    data = scraper(url)
    print(data)
    # scraper(url)
    
    # Save data to JSON file
    with open('data_film.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Data telah selesai di scraped dan disimpan ke data_film.json.")

# Tugas Scraping Data – TVShows

Dalam repository ini, saya dan teman saya melakukan pengambilan data dari web https://www.imdb.com/chart/toptv/ sebanyak 250 data. Setelah itu, kami mencoba untuk membuat chart yang menampilkan 5 TVshow terbaik berdasarkan rating di setiap kategori usia.

## Scraping Data
Kami menggunakan selenium sebagai automasi browser dan beautifulsoup sebagai parsing HTML.
Berikut adalah logika pengerjaan kami:
1. Memastikan elemen pada web https://www.imdb.com/chart/toptv/ sudah ter-load, terutama pada parent element dari konten yang akan discraping.
```python
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
```
2. Data yang banyak menyebabkan error `index out of range` karena selenium tidak melakukan scrolling lebih dalam. Sehingga, ada data yang tidak ter-load. Oleh karena itu, selenium perlu melakukan scrolling.
3. ```python
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
   ```
   4. Mengambil data
  - Tag `<li></li>` sebagai container dari data yang ingin discraping. Sehingga, kami harus menggunakan `find_all` dan melakukan `for` loop.
  - Data judul didapatkan dari tag `<h3></h3>` yang menggunakan `find` serta disimpan ke variabel `film_title`.
  - Data tahun rilis, durasi, dan batas usia memiliki nama `class` yang sama. Sehingga, kami menggunakan `find_all` dan disimpan ke dalam list `data_desc`.
  - Data rating film didapatkan dari tag `<span></span>` yang menggunakan `find` serta disimpan ke variabel `star_rating`.
  - Semua data tersebut digabung ke dalam list kosong
```python
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
```
5. List yang awalnya kosong, sekarang sudah memiliki data tv shows. Saatnya membuat list of object tersebut menjadi data JSON.
```python
with open("data_TVSHOWS.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
```

## Chart
Kami menggunakan pandas untuk mengubah file JSON menjadi data frame dan matplotlib untuk visualisasi data.
Berikut adalah logika pengerjaan kami:
1. Mengakses data JSON dari hasil scraping.
```python
with open(json_file, 'r') as file:
    data = json.load(file)
```
2. Membuat data frame dan konversi tipe data
```python
df = pd.DataFrame(data)    
df['TV SHOW RATING'] = df['TV SHOW RATING'].astype(float)
```
3. Mengelompokkan data berdasarkan age rating dan mengambil lima teratas berdasarkan tv shows rating.
```python
grouped = df.groupby('AGE RATING').apply(lambda x: x.sort_values(by='TV SHOW RATING', ascending=False).head(5))    
grouped = grouped.reset_index(drop=True)
```
4. Mempersiapkan sub-plot untuk setiap age rating.
```python
age_ratings = grouped['AGE RATING'].unique()
fig, axes = plt.subplots(len(age_ratings), 1, figsize=(10, 5 * len(age_ratings)), sharex=True)

if len(age_ratings) == 1:
    axes = [axes]
```
5. Membuat chart bar untuk setiap age rating
```python
for i, age_rating in enumerate(age_ratings):
    top_movies = grouped[grouped['AGE RATING'] == age_rating]
    axes[i].barh(top_movies['TV SHOW NAME'], top_movies['TV SHOW RATING'], color='orange')
    axes[i].set_title(f'Top 5 TVShows (AGE RATING: {age_rating})')
    axes[i].invert_yaxis()
    axes[i].set_xlabel('TV SHOW RATING')
```
6. Menyimpan file hasil chart ke lokal folder serta menampilkannya
```python
plt.tight_layout()
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, 'chart_top_tvshows.png')
plt.savefig(save_path)
plt.show()
```

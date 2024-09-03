import json
import pandas as pd
import matplotlib.pyplot as plt
import os

json_file = 'data_TVSHOWS.json'

with open(json_file, 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)    
df['TV SHOW RATING'] = df['TV SHOW RATING'].astype(float)    
grouped = df.groupby('AGE RATING').apply(lambda x: x.sort_values(by='TV SHOW RATING', ascending=False).head(5))    
grouped = grouped.reset_index(drop=True)

age_ratings = grouped['AGE RATING'].unique()
fig, axes = plt.subplots(len(age_ratings), 1, figsize=(10, 5 * len(age_ratings)), sharex=True)

if len(age_ratings) == 1:
    axes = [axes]

for i, age_rating in enumerate(age_ratings):
    top_movies = grouped[grouped['AGE RATING'] == age_rating]
    axes[i].barh(top_movies['TV SHOW NAME'], top_movies['TV SHOW RATING'], color='orange')
    axes[i].set_title(f'Top 5 Movies (AGE RATING: {age_rating})')
    axes[i].invert_yaxis()
    axes[i].set_xlabel('TV SHOW RATING')

plt.tight_layout()
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, 'chart_top_tvshows.png')
plt.savefig(save_path)
plt.show()
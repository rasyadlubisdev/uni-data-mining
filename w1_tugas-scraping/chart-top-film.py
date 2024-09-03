import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_top_movies_by_age_rating(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    df = pd.DataFrame(data)    
    df['Film Rating'] = df['Film Rating'].astype(float)    
    grouped = df.groupby('Age Rating').apply(lambda x: x.sort_values(by='Film Rating', ascending=False).head(5))    
    grouped = grouped.reset_index(drop=True)
    
    age_ratings = grouped['Age Rating'].unique()
    fig, axes = plt.subplots(len(age_ratings), 1, figsize=(10, 5 * len(age_ratings)), sharex=True)

    if len(age_ratings) == 1:
        axes = [axes]

    for i, age_rating in enumerate(age_ratings):
        top_movies = grouped[grouped['Age Rating'] == age_rating]
        axes[i].barh(top_movies['Movie Name'], top_movies['Film Rating'], color='skyblue')
        axes[i].set_title(f'Top 5 Movies (Age Rating: {age_rating})')
        axes[i].invert_yaxis()
        axes[i].set_xlabel('Film Rating')
    
    plt.tight_layout()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, 'chart.png')
    plt.savefig(save_path)
    plt.show()

plot_top_movies_by_age_rating('data_film.json')

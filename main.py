import requests
import os

# 1. Configuration (Uses the Secrets you just saved)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
MONEY_LINK = os.getenv("UNIVERSAL_LINK")

def fetch_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()
    return response.get('results', [])[:10]  # Get top 10 movies

def generate_html(movies):
    movie_cards = ""
    for movie in movies:
        title = movie.get('title')
        poster = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
        
        # Every movie gets your money-making link
        movie_cards += f'''
        <div class="movie-card">
            <img src="{poster}" alt="{title}">
            <h3>{title}</h3>
            <a href="{MONEY_LINK}" class="btn">Download Now</a>
        </div>
        '''
    
    # The full HTML template
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily Movie Updates</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; background: #141414; color: white; padding: 20px; }}
            .movie-grid {{ display: flex; flex-wrap: wrap; justify-content: center; }}
            .movie-card {{ border: 1px solid #333; margin: 15px; padding: 15px; width: 220px; background: #1f1f1f; border-radius: 10px; }}
            img {{ width: 100%; border-radius: 5px; }}
            .btn {{ display: block; margin-top: 10px; background: #e50914; color: white; padding: 10px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>🔥 Trending Today</h1>
        <div class="movie-grid">
            {movie_cards}
        </div>
    </body>
    </html>
    '''
    return html_content

# Main Execution
if __name__ == "__main__":
    movies = fetch_trending_movies()
    new_html = generate_html(movies)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

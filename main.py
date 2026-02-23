import requests
import os

# 1. Configuration (Uses your GitHub Secrets)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
MONEY_LINK = os.getenv("UNIVERSAL_LINK")

# Create movies directory if it doesn't exist
if not os.path.exists('movies'):
    os.makedirs('movies')

def fetch_trending_movies():
    # Fetching 20 movies for a better looking homepage
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()
    return response.get('results', [])

def generate_header():
    return f'''
    <header style="display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background: #000; border-bottom: 3px solid #e50914; position: sticky; top: 0; z-index: 1000;">
        <div style="font-size: 26px; font-weight: bold; color: #e50914; font-family: 'Arial Black', sans-serif; cursor: pointer;" onclick="window.location.href='/'">FreeMoviesDownload</div>
        <div style="cursor: pointer; font-size: 24px;" onclick="fakeSearch()">🔍</div>
    </header>
    <script>
        function fakeSearch() {{
            let q = prompt("Enter Movie Name to Search:");
            if(q) window.location.href = "{MONEY_LINK}";
        }}
    </script>
    '''

def generate_movie_details_page(movie):
    title = movie.get('title')
    slug = title.replace(" ", "-").replace("/", "-").lower()
    poster = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
    desc = movie.get('overview')
    rating = movie.get('vote_average')
    date = movie.get('release_date')

    detail_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download {title} Full Movie - FreeMoviesDownload</title>
        <style>
            body {{ background: #141414; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }}
            .container {{ padding: 20px; max-width: 800px; margin: auto; }}
            img {{ width: 300px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }}
            .download-box {{ margin-top: 30px; background: #1f1f1f; padding: 20px; border-radius: 10px; }}
            .btn {{ display: block; padding: 15px; margin: 10px 0; border-radius: 5px; text-decoration: none; color: white; font-weight: bold; }}
            .btn-480 {{ background: #2ecc71; }} .btn-720 {{ background: #3498db; }} .btn-1080 {{ background: #e74c3c; }}
        </style>
    </head>
    <body>
        {generate_header()}
        <div class="container">
            <img src="{poster}" alt="{title}">
            <h1>{title}</h1>
            <p><strong>Rating:</strong> ⭐ {rating} | <strong>Release:</strong> {date}</p>
            <p style="line-height: 1.6; color: #ccc;">{desc}</p>
            
            <div class="download-box">
                <h3>Download Options</h3>
                <a href="{MONEY_LINK}" class="btn btn-480">Download 480p [300MB]</a>
                <a href="{MONEY_LINK}" class="btn btn-720">Download 720p [900MB]</a>
                <a href="{MONEY_LINK}" class="btn btn-1080">Download 1080p (BlueRay) [2.1GB]</a>
            </div>
        </div>
    </body>
    </html>
    '''
    filename = f"movies/{slug}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(detail_html)
    return filename

def generate_homepage(movies):
    movie_cards = ""
    for movie in movies:
        title = movie.get('title')
        poster = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
        # This creates the link to the internal info page
        slug = title.replace(" ", "-").replace("/", "-").lower()
        detail_url = f"/movies/{slug}.html"
        
        movie_cards += f'''
        <div class="movie-card" onclick="window.location.href='{detail_url}'" style="cursor:pointer; width: 180px; margin: 10px; background: #1f1f1f; padding: 10px; border-radius: 8px; transition: 0.3s;">
            <img src="{poster}" style="width: 100%; border-radius: 5px;">
            <p style="font-size: 14px; margin-top: 10px; height: 40px; overflow: hidden;">{title}</p>
        </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FreeMoviesDownload - Latest Movie Updates</title>
        <style>
            body {{ background: #141414; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }}
            .grid {{ display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }}
            .movie-card:hover {{ transform: scale(1.05); background: #252525; }}
        </style>
    </head>
    <body>
        {generate_header()}
        <h2 style="text-align: center; margin-top: 20px;">Latest Movies Added Today</h2>
        <div class="grid">
            {movie_cards}
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    trending = fetch_trending_movies()
    # Generate individual pages
    for m in trending:
        generate_movie_details_page(m)
    
    # Generate homepage
    home_html = generate_homepage(trending)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

import requests
import os

# 1. Configuration & Secrets
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
MONEY_LINK = os.getenv("UNIVERSAL_LINK")
DIRECT_AD_LINK = os.getenv("DIRECT_AD_LINK")

# 2. Adsterra Snippets (Paste your actual scripts between the quotes)
AD_POP_UNDER = '''<script src="https://pl28777294.effectivegatecpm.com/2e/dd/f1/2eddf1592034bd9331e15ea6c72c25dc.js"></script>'''
AD_SOCIAL_BAR = '''<script src="https://pl28777303.effectivegatecpm.com/4d/4a/de/4d4ade739c1cbdfebca1a4fb7ef5e6f2.js"></script>'''
AD_BANNER = '''<script async="async" data-cfasync="false" src="https://pl28777299.effectivegatecpm.com/5d00fff41d92a8e44974d9a29ab6a718/invoke.js"></script>
<div id="container-5d00fff41d92a8e44974d9a29ab6a718"></div>'''

# Create directory for detail pages
if not os.path.exists('movies'):
    os.makedirs('movies')

def generate_header():
    return f'''
    <header style="background: #000; padding: 12px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #e50914; position: sticky; top: 0; z-index: 1000; font-family: 'Segoe UI', sans-serif;">
        <div style="font-size: 24px; font-weight: bold; color: #e50914; cursor: pointer; letter-spacing: 1px;" onclick="window.location.href='/'">FreeMoviesDownload</div>
        
        <div style="position: relative; width: 40%; display: flex; align-items: center;">
            <input type="text" id="searchInput" placeholder="Search movies..." 
                style="width: 100%; padding: 10px 45px 10px 15px; border-radius: 25px; border: 1px solid #333; background: #1a1a1a; color: white; outline: none;">
            <span style="position: absolute; right: 15px; color: #e50914; cursor: pointer; font-size: 18px;" onclick="handleSearch()">🔍</span>
        </div>
    </header>

    <script>
        function handleSearch() {{
            const q = document.getElementById('searchInput').value.trim();
            if (q !== "") {{
                // Opens AD in new tab
                window.open("{DIRECT_AD_LINK}", "_blank");
                // Redirects current tab to search results
                window.location.href = "/search.html?q=" + encodeURIComponent(q);
            }}
        }}
        document.getElementById('searchInput')?.addEventListener("keypress", (e) => {{ if (e.key === "Enter") handleSearch(); }});
    </script>
    '''

def generate_movie_details_page(movie):
    title = movie.get('title')
    slug = title.replace(" ", "-").replace("/", "-").replace(":", "").lower()
    poster = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
    desc = movie.get('overview')
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download {title} Full Movie Free</title>
        {AD_POP_UNDER} {AD_SOCIAL_BAR}
        <style>
            body {{ background: #141414; color: white; font-family: sans-serif; margin: 0; text-align: center; }}
            .content {{ padding: 20px; max-width: 800px; margin: auto; }}
            .btn {{ display: block; padding: 15px; margin: 10px 0; border-radius: 5px; text-decoration: none; color: white; font-weight: bold; transition: 0.3s; }}
            .btn:hover {{ opacity: 0.8; transform: scale(1.02); }}
        </style>
    </head>
    <body>
        {generate_header()}
        <div class="content">
            <img src="{poster}" style="width: 280px; border-radius: 15px; margin-top: 20px;">
            <h1>{title}</h1>
            <p style="color: #ccc; line-height: 1.6;">{desc}</p>
            <div style="background: #1f1f1f; padding: 20px; border-radius: 10px; margin-top: 30px;">
                <h3>Fast Download Links</h3>
                {AD_BANNER}
                <a href="{MONEY_LINK}" class="btn" style="background: #2ecc71;">Download 480p (Fast)</a>
                <a href="{MONEY_LINK}" class="btn" style="background: #3498db;">Download 720p (HD)</a>
                <a href="{MONEY_LINK}" class="btn" style="background: #e74c3c;">Download 1080p (4K)</a>
            </div>
        </div>
    </body>
    </html>
    '''
    with open(f"movies/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_search_page():
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Results - FreeMoviesDownload</title>
        {AD_POP_UNDER}
        <style>
            body {{ background: #141414; color: white; font-family: sans-serif; margin: 0; }}
            .grid {{ display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }}
            .card {{ width: 180px; margin: 15px; background: #1f1f1f; padding: 10px; border-radius: 8px; text-align: center; cursor: pointer; }}
        </style>
    </head>
    <body>
        {generate_header()}
        <h2 id="st" style="text-align: center; margin-top: 30px;">Searching...</h2>
        <div id="res" class="grid"></div>
        <script>
            const q = new URLSearchParams(window.location.search).get('q');
            if(q) {{
                fetch(`https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query=${{q}}`)
                .then(r => r.json()).then(d => {{
                    document.getElementById('st').innerText = `Results for "${{q}}"`;
                    const c = document.getElementById('res');
                    d.results.forEach(m => {{
                        if(m.poster_path) {{
                            c.innerHTML += `<div class="card" onclick="window.location.href='{MONEY_LINK}'">
                                <img src="https://image.tmdb.org/t/p/w500${{m.poster_path}}" style="width:100%; border-radius:5px;">
                                <p style="font-size:14px;">${{m.title}}</p>
                                <span style="color:#e50914; font-weight:bold;">Download</span>
                            </div>`;
                        }}
                    }});
                }});
            }}
        </script>
    </body>
    </html>
    '''
    with open("search.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_index(movies):
    cards = ""
    for m in movies:
        title = m.get('title')
        slug = title.replace(" ", "-").replace("/", "-").replace(":", "").lower()
        poster = f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}"
        cards += f'''
        <div class="card" onclick="window.location.href='/movies/{slug}.html'" style="width: 190px; margin: 15px; background: #1f1f1f; padding: 10px; border-radius: 10px; cursor: pointer; transition: 0.3s;">
            <img src="{poster}" style="width: 100%; border-radius: 5px;">
            <p style="font-size: 14px; margin-top: 10px; height: 35px; overflow: hidden;">{title}</p>
        </div>
        '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FreeMoviesDownload - Download Latest Movies</title>
        {AD_POP_UNDER} {AD_SOCIAL_BAR}
        <style>
            body {{ background: #141414; color: white; font-family: sans-serif; margin: 0; }}
            .grid {{ display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }}
            .card:hover {{ transform: translateY(-5px); background: #252525; }}
        </style>
    </head>
    <body>
        {generate_header()}
        <h2 style="text-align: center; margin-top: 30px;">Trending Movies</h2>
        <div class="grid">{cards}</div>
    </body>
    </html>
    '''
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    # 1. Fetch Trending
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    trending = requests.get(url).json().get('results', [])
    
    # 2. Build Pages
    for movie in trending:
        generate_movie_details_page(movie)
    
    generate_search_page()
    generate_index(trending)
    print("Successfully built all pages!")

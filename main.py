import requests
import os

# 1. Configuration & Secrets 
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
MONEY_LINK = os.getenv("UNIVERSAL_LINK")
DIRECT_AD_LINK = os.getenv("DIRECT_AD_LINK")

# 2. Adsterra Snippets (Paste your actual scripts here)
AD_POP_UNDER = '''<script src="https://pl28777294.effectivegatecpm.com/2e/dd/f1/2eddf1592034bd9331e15ea6c72c25dc.js"></script>'''
AD_SOCIAL_BAR = '''<script src="https://pl28777303.effectivegatecpm.com/4d/4a/de/4d4ade739c1cbdfebca1a4fb7ef5e6f2.js"></script>'''
AD_BANNER = '''<script async="async" data-cfasync="false" src="https://pl28777299.effectivegatecpm.com/5d00fff41d92a8e44974d9a29ab6a718/invoke.js"></script>
<div id="container-5d00fff41d92a8e44974d9a29ab6a718"></div>'''

if not os.path.exists('movies'):
    os.makedirs('movies')

def fetch_50_plus_items():
    combined_list = []
    # Loop through first 3 pages (20 items per page = 60 items)
    for i in range(1, 4):
        # Fetch Worldwide Movies
        m_url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&page={i}"
        # Fetch Worldwide TV/Dramas
        t_url = f"https://api.themoviedb.org/3/trending/tv/day?api_key={TMDB_API_KEY}&page={i}"
        
        movies = requests.get(m_url).json().get('results', [])
        tvs = requests.get(t_url).json().get('results', [])
        
        # Standardize names for TV
        for item in tvs:
            item['title'] = item.get('name')
            item['is_tv'] = True
            
        combined_list.extend(movies)
        combined_list.extend(tvs)
    
    return combined_list

def generate_header():
    return f'''
    <header style="background: #000; padding: 12px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #e50914; position: sticky; top: 0; z-index: 1000; font-family: sans-serif;">
        <div style="font-size: 24px; font-weight: bold; color: #e50914; cursor: pointer;" onclick="window.location.href='/'">FreeMoviesDownload</div>
        <div style="position: relative; width: 40%; display: flex; align-items: center;">
            <input type="text" id="searchInput" placeholder="Search Bollywood, Hollywood, Dramas..." 
                style="width: 100%; padding: 10px 45px 10px 15px; border-radius: 25px; border: 1px solid #333; background: #1a1a1a; color: white; outline: none;">
            <span style="position: absolute; right: 15px; color: #e50914; cursor: pointer;" onclick="handleSearch()">🔍</span>
        </div>
    </header>
    <script>
        function handleSearch() {{
            const q = document.getElementById('searchInput').value.trim();
            if (q !== "") {{
                window.open("{DIRECT_AD_LINK}", "_blank");
                window.location.href = "/search.html?q=" + encodeURIComponent(q);
            }}
        }}
        document.getElementById('searchInput').addEventListener("keypress", (e) => {{ if (e.key === "Enter") handleSearch(); }});
    </script>
    '''

def generate_detail_page(item):
    title = item.get('title') or item.get('name')
    if not title: return
    slug = title.replace(" ", "-").replace("/", "-").replace(":", "").lower()
    poster = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}"
    desc = item.get('overview', "No description available.")
    m_type = "TV Series" if item.get('is_tv') else "Movie"
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download {title} {m_type} Free</title>
        {AD_POP_UNDER} {AD_SOCIAL_BAR}
        <style>
            body {{ background: #141414; color: white; font-family: sans-serif; margin: 0; text-align: center; }}
            .btn {{ display: block; padding: 15px; margin: 10px 0; border-radius: 5px; text-decoration: none; color: white; font-weight: bold; }}
        </style>
    <meta name="google-site-verification" content="sr8tV0LhooUc0te1Pr-1kYg-ShKKrqyphiw1dHAguBg" />
    </head>
    <body>
        {generate_header()}
        <div style="padding: 20px; max-width: 800px; margin: auto;">
            <img src="{poster}" style="width: 280px; border-radius: 15px; margin-top: 20px;">
            <h1>{title}</h1>
            <p style="color: #ccc; line-height: 1.6;">{desc}</p>
            <div style="background: #1f1f1f; padding: 20px; border-radius: 10px; margin-top: 30px;">
                <h3>Download {m_type}</h3>
                <a href="{MONEY_LINK}" class="btn" style="background: #2ecc71;">Download 480p</a>
                <a href="{MONEY_LINK}" class="btn" style="background: #3498db;">Download 720p (HD)</a>
                <a href="{MONEY_LINK}" class="btn" style="background: #e74c3c;">Download 1080p (4K)</a>
            </div>
        </div>
    </body>
    </html>
    '''
    with open(f"movies/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_index(items):
    cards = ""
    for m in items:
        title = m.get('title')
        if not title: continue
        slug = title.replace(" ", "-").replace("/", "-").replace(":", "").lower()
        poster = f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}"
        cards += f'''
        <div onclick="window.location.href='movies/{slug}.html'" style="width: 180px; margin: 12px; background: #1f1f1f; padding: 10px; border-radius: 10px; cursor: pointer; text-align:center;">
            <img src="{poster}" style="width: 100%; border-radius: 5px;">
            <p style="font-size: 13px; margin-top: 10px; height: 35px; overflow: hidden;">{title}</p>
        </div>
        '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FreeMoviesDownload - Global Movies & TV</title>
        {AD_POP_UNDER} {AD_SOCIAL_BAR}
        <style>body {{ background: #141414; color: white; font-family: sans-serif; margin: 0; }} .grid {{ display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }}</style>
    <meta name="google-site-verification" content="sr8tV0LhooUc0te1Pr-1kYg-ShKKrqyphiw1dHAguBg" />
    </head>
    <body>
        {generate_header()}
        <h2 style="text-align: center; margin-top: 30px;">Global Trending: Movies & Shows</h2>
        <div class="grid">{cards}</div>
    </body>
    </html>
    '''
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    all_content = fetch_50_plus_items()
    for item in all_content:
        generate_detail_page(item)
    
    # Also reuse the generate_search_page() from previous step here
    generate_index(all_content)
    print(f"Successfully built {len(all_content)} pages!")

from django.shortcuts import render
from . import api
from datetime import datetime
import requests
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.
def index(request):
    upcoming_movies = api.get_upcoming_movies()
    top_movies = api.top_rating()
    years = range(1980, 2026)

    selected_year = request.GET.get("year")

    # Sort & slicing
    upcoming_movies = sorted(
        upcoming_movies,
        key=lambda m: datetime.strptime(m.get("release_date", "2100-01-01"), "%Y-%m-%d")
    )
    

    # Default empty list agar tidak error
    best_movies = []

    # Filter by year jika dipilih
    if selected_year:
        best_movies = [
            m for m in top_movies
            if m.get("release_date", "").startswith(str(selected_year))
        ]
    
    upcoming_movies = upcoming_movies[:5]
    top_movies = top_movies[:6]

    context = {
        'upcoming_movies': upcoming_movies,
        'top_movies': top_movies,
        'best_movies': best_movies,
        'years': years,
    }
    return render(request,'index.html', context)



def detail_movie(request, movie_id):
    
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "append_to_response": "credits,videos,images"
    }
    response = requests.get(url, params=params).json()

    # Jika error / tidak ada film
    if "status_code" in response:
        return render(request, "404.html")

    # Data utama film
    movie = response

    # Director & Producer
    crew = response.get("credits", {}).get("crew", [])
    movie["director"] = next((c["name"] for c in crew if c["job"] == "Director"), "Unknown")
    movie["producer"] = next((c["name"] for c in crew if c["job"] == "Producer"), "Unknown")

    # Cast (ambil 5)
    cast_list = response.get("credits", {}).get("cast", [])[:6]
    movie["cast_full"] = [
        {
            "name": c["name"],
            "photo": f"https://image.tmdb.org/t/p/w300{c['profile_path']}"
            if c.get("profile_path") else None
        }
        for c in cast_list
    ]

    # Trailer YouTube
    videos = response.get("videos", {}).get("results", [])
    trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
    movie["trailer_id"] = trailer["key"] if trailer else None

    # SCENES / BACKDROPS
    scenes = response.get("images", {}).get("backdrops", [])[:8]
    movie["scenes"] = scenes

    # SIMILAR MOVIES
    similar = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/similar",
        params={"api_key": "d8d666fb30f19051784ac3645fdf05da"}
    ).json().get("results", [])[:6]

    # Tambahkan full poster URL
    for sm in similar:
        sm["poster_full"] = (
            f"https://image.tmdb.org/t/p/w342{sm['poster_path']}"
            if sm.get("poster_path") else None
        )

    return render(request, "detail_movie.html", {
        "movie": movie,
        "similar_movies": similar
    })





def search_api(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse({"results": []})

    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "query": q,
        "page": 1,
        "include_adult": False,
    }

    response = requests.get(url, params=params).json()

    results = []
    for movie in response.get("results", [])[:10]:
        results.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie.get("release_date", "")[:4] if movie.get("release_date") else "",
            "poster": (
                f"https://image.tmdb.org/t/p/w92{movie['poster_path']}"
                if movie.get("poster_path") else None
            )
        })

    return JsonResponse({"results": results})


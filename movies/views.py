from django.shortcuts import render
from . import api
from datetime import datetime
import requests

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
    
    upcoming_movies = upcoming_movies[:6]
    top_movies = top_movies[:6]

    context = {
        'upcoming_movies': upcoming_movies,
        'top_movies': top_movies,
        'best_movies': best_movies,
        'years': years,
    }
    return render(request,'index.html', context)



def detail_movie(request, slug):
    movies = api.top_rating() + api.get_upcoming_movies()
    movie = next((m for m in movies if m["slug"] == slug), None)

    if not movie:
        return render(request, "404.html")

    movie_id = movie["id"]

    # Fetch detail lengkap termasuk credits + videos
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "append_to_response": "credits,videos"
    }

    response = requests.get(url, params=params).json()

    # Masukkan data tambahan
    movie["runtime"] = response.get("runtime")
    movie["status"] = response.get("status")
    movie["overview"] = response.get("overview")
    movie["vote_average"] = response.get("vote_average")

    # Ambil trailer
    videos = response.get("videos", {}).get("results", [])
    trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)

    movie["trailer_id"] = trailer["key"] if trailer else None

    # Director
    crew = response.get("credits", {}).get("crew", [])
    director = next((c["name"] for c in crew if c["job"] == "Director"), "Unknown")
    producer = next((c["name"] for c in crew if c["job"] == "Producer"), "Unknown")
    movie["director"] = director
    movie["producer"] = producer

    # Cast 
    cast_list = response.get("credits", {}).get("cast", [])[:5]
    movie["cast_full"] = [
    {
        "name": c["name"],
        "photo": f"https://image.tmdb.org/t/p/w300{c['profile_path']}" if c.get("profile_path") else None
    }
    for c in cast_list]

    context = {"movie": movie}
    return render(request, "detail_movie.html", context)



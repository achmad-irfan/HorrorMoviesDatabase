import requests
from datetime import datetime, timedelta
from django.shortcuts import render
import re

def slugify(text):
    text=text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')
    
def get_upcoming_movies():
    url= 'https://api.themoviedb.org/3/discover/movie'
    release_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "with_genres": "27",
        "primary_release_date.gte": release_date,
        "sort_by": "primary_release_date.asc",
        "language": "en-US"
        }
    response= requests.get(url,params=params)
    upcoming_movies= response.json().get('results',[])
    for movie in upcoming_movies:
        movie['slug']=slugify(movie['title'])
        
    return upcoming_movies

def top_rating():
    url= 'https://api.themoviedb.org/3/discover/movie'
    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "with_genres": "27",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 500, 
        "primary_release_year": 2025
        }
    
    response= requests.get(url,params=params)
    top_movies= response.json().get('results',[])
    for movie in top_movies:
        movie['slug'] = slugify(movie['title'].replace(":", ""))

        
    return top_movies

def best_year():
    url= 'https://api.themoviedb.org/3/discover/movie'
    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "with_genres": "27",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 100, 
        }
    
    response= requests.get(url,params=params)
    top_movies= response.json().get('results',[])
    for movie in top_movies:
        movie['slug'] = slugify(movie['title'].replace(":", ""))

        
    return top_movies
    
def get_similar_movies(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar'

    params = {
        "api_key": "d8d666fb30f19051784ac3645fdf05da",
        "language": "en-US",
        "with_genres": "27",
    }

    response = requests.get(url, params=params)
    movies = response.json().get('results', [])

    return movies

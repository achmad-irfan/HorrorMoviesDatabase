import requests
api_key= "d8d666fb30f19051784ac3645fdf05da"
base_url= "https://api.themoviedb.org/3"


def search_person(name):
    url = f"{base_url}/search/person"
    params = {
        "api_key": api_key,
        'query':name
        }
    response= requests.get(url,params=params)
    return response.json()

def search_person_id(person_id):
    url= f"{base_url}/person/{person_id}"
    params={
        "api_key": api_key,
    }
    
    response= requests.get(url,params=params)
    return response.json()


def filmography(person_id):
    url=f"{base_url}/person/{person_id}/movie_credits"
    params={
        "api_key": api_key,
    }
    
    response=requests.get(url,params=params)
    return response.json()
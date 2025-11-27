from django.shortcuts import render
from django.views.generic.base import TemplateView
import requests
from .api import search_person,search_person_id, filmography
from django.http import JsonResponse

GENDER_MAP = {
    0: "Unknown",
    1: "Female",
    2: "Male",
    3: "Non-binary"
}
HORROR_GENRE_ID =27

# Create your views here.
class ActorView(TemplateView):
    template_name = 'hgraphy/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        person_id = self.request.GET.get("id")
        name = self.request.GET.get("name")

        # Jika ada ID → langsung ambil detailnya
        if person_id:
            person_detail = search_person_id(person_id)
            gender_id = person_detail.get("gender", 0)
            person_detail["gender_text"] = GENDER_MAP.get(gender_id, "Unknown")
            context["person"] = person_detail

            data = filmography(person_id)
            cast_list = data['cast']
            crew_list= data['crew']
            
            as_director = [m for m in crew_list if m.get("job") == "Director"]
            as_producer = [m for m in crew_list if m.get("job") == "Producer"]
            as_writer   = [m for m in crew_list if m.get("job") == "Writer"]
            
            def sort_by_year(list_film):
                return sorted(
                list_film,
                key=lambda x: x.get("release_date", "") or "",
                reverse=True)
            
            context["as_actor"] = sort_by_year(cast_list)
            context["as_director"] = sort_by_year(as_director)
            context["as_producer"] = sort_by_year(as_producer)
            context["as_writer"] = sort_by_year(as_writer)
            # horror_film = [f for f in cast_list if HORROR_GENRE_ID in f.get("genre_ids", [])]
            # context["films"] = horror_film
            
            return context

        # fallback: kalau user submit nama manual tanpa memilih suggestion
        if name:
            result = search_person(name)
            if result.get("results"):
                person_id = result["results"][0]["id"]
                return self.get_context_data(id=person_id)

        return context



def person_suggestion(request):
    q = request.GET.get("query", "")
    if not q:
        return JsonResponse({"results": []})

    data = search_person(q)
    results = data.get("results", [])[:5]  # hanya ambil 5 teratas

    suggestions = [
    {
        "id": p["id"],
        "name": p["name"],
        "image": p["profile_path"] or ""
    }
    for p in results]
    return JsonResponse({"results": suggestions})

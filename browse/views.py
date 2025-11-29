import requests
from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView


# Daftar bahasa tetap dikirim ke template
YEARS = sorted(range(1970, 2026), reverse=True)

LANGUAGES = [
    { "code": "en", "name": "English" },
    { "code": "ja", "name": "Japanese" },
    { "code": "ko", "name": "Korean" },
    { "code": "es", "name": "Spanish" },
    { "code": "fr", "name": "French" },
    { "code": "zh", "name": "Chinese (Mandarin)" },
    { "code": "th", "name": "Thai" },
    { "code": "id", "name": "Indonesian" },
    { "code": "hi", "name": "Hindi" },
    { "code": "ru", "name": "Russian" },
    { "code": "pt", "name": "Portuguese" },
    { "code": "it", "name": "Italian" },
    { "code": "de", "name": "German" },
    { "code": "tr", "name": "Turkish" },
    { "code": "ph", "name": "Filipino (Tagalog)" }
]

class PageMovies(ListView):
    model = Movie
    paginate_by = 15  # jumlah poster per halaman
    template_name = 'browse/index.html'
    context_object_name = 'movies'

    # Filter query berdasarkan GET parameter
    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.GET.get("name")
        lang = self.request.GET.get("lang")
        rating = self.request.GET.get("rating")
        year = self.request.GET.get("year")
        sorted_by= self.request.GET.get("sorted")
        
        if name:
            qs = qs.filter(title__icontains=name)
        if lang:
            qs = qs.filter(language=lang)
        if rating:
            try:
                qs = qs.filter(vote_average__gte=float(rating),
                               vote_count__gte=100)
            except ValueError:
                pass
        if year:
            try:
                qs= qs.filter(release_year=int(year))
            except ValueError:
                pass  
            
        if sorted_by:
            if sorted_by == "release":
                qs = qs.order_by('-release_year')  
            elif sorted_by == "vote":
                qs = qs.order_by('-vote_average')  
            elif sorted_by == "popular":
                qs = qs.order_by('-vote_count')  
            elif sorted_by == "title":
                qs = qs.order_by('title')
            elif sorted_by == "popularity":
                qs=qs.order_by("-popularity")
            
        return qs

    # Kirim languages ke template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = LANGUAGES
        context['years']= YEARS
        return context

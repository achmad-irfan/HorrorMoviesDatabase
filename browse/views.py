import requests
from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView


# def index(request):
#     movies = Movie.objects.all()
   
    
#     name = request.GET.get("name")
#     lang = request.GET.get("lang")
#     rating = request.GET.get("rating")
#     year = request.GET.get("year")
    
#     if name:
#         movies = movies.filter(title__icontains=name)
#     if lang:
#         movies = movies.filter(language=lang)
#     if rating:
#         try:
#             movies = movies.filter(vote_average__gte=float(rating))
#         except ValueError:
#             pass
#     if year:
#         if '-' in year:
#             start, end = year.split('-')
#             try:
#                 movies = movies.filter(release_year__gte=int(start), release_year__lte=int(end))
#             except ValueError:
#                 pass
#         else:
#             try:
#                 movies = movies.filter(release_year=int(year))
#             except ValueError:
#                 pass

#     languages = [
#         { "code": "en", "name": "English" },
#         { "code": "ja", "name": "Japanese" },
#         { "code": "ko", "name": "Korean" },
#         { "code": "es", "name": "Spanish" },
#         { "code": "fr", "name": "French" },
#         { "code": "zh", "name": "Chinese (Mandarin)" },
#         { "code": "th", "name": "Thai" },
#         { "code": "id", "name": "Indonesian" },
#         { "code": "hi", "name": "Hindi" },
#         { "code": "ru", "name": "Russian" },
#         { "code": "pt", "name": "Portuguese" },
#         { "code": "it", "name": "Italian" },
#         { "code": "de", "name": "German" },
#         { "code": "tr", "name": "Turkish" },
#         { "code": "ph", "name": "Filipino (Tagalog)" }
#     ]

#     return render(request, "browse/index.html", {"languages": languages,"movies":movies})

# class page_movies(ListView):
#     model= Movie
#     paginate_by = 10
#     template_name = 'browse/index.html'
#     context_object_name = 'movies'



# Daftar bahasa tetap dikirim ke template
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
                qs = qs.filter(vote_average__gte=float(rating))
            except ValueError:
                pass
        if year:
            if '-' in year:
                start, end = year.split('-')
                try:
                    qs = qs.filter(release_year__gte=int(start), release_year__lte=int(end))
                except ValueError:
                    pass
            else:
                try:
                    qs = qs.filter(release_year=int(year))
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
            
        return qs

    # Kirim languages ke template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = LANGUAGES
        return context

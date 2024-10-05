# from django.shortcuts import render
# from django.http import JsonResponse

# from watchlist_app.models import movies


# def movie_list(request):
    
#     films = movies.objects.all()
    
#     movie_list = list(films.values())
    
#     context = {'film' : movie_list}
    
#     return JsonResponse(context)


# def movie_details(request, pk):
    
#     film = movies.objects.get(pk=pk)  ## this is not a query set set so we cannot do .values() or list of.values() to get a json response
    
#     context = {'name' : film.name, 'description': film.description, 'active' : film.active}
    
#     return JsonResponse(context)
    

    

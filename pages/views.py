from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import InputForm
from metadata.models import Movie, Genre, Movie_Genre

# Create your views here.

def index(req):
    res_data = {}
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    movie_list = []
    
    for i in range(0, 3):
        movie_list.append(movies[i])

    # for i in range(len(movie_list)):
    #     if movie_list[i].title=='Toy Story':
    #         # movie = [
    #         # movie_id = '',
    #         # title = '',
    #         # release_date = '',
    #         # vote_average = '',
    #         # overview = '',
    #         # poster_url = '',
    #         # director = '',
    #         # main_actor = '',
    #         # ]
    #         print(movie_list[i].poster_url)
    #         movie.poster_url = movie_list[i].poster_url


    res_data['movie_list'] = movie_list
    print(res_data['movie_list'][0].poster_url)
    return render(req, 'index.html', res_data)



def input(request):
    form = InputForm()
    if(request.method=='POST'):
        form = InputForm(request.POST)
        if form.is_valid():
            return render(request, 'output.html', {'form':form})
        
    else:
        form=InputForm()

    return render(request, 'input.html', {'form':form})

def output(request):
    #recommended_movie = Movie.objects.get(id='30') 이런식으로
    #recommended_movie = Fcuser.objects.get(id=1)
    #print()
    return render(request, 'output.html')

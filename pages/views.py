from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import InputForm
from metadata.models import Movie, Genre, Movie_Genre
from operator import itemgetter

# Create your views here.

sort_movies = {}

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
    movies = []
    form=InputForm()

    if(request.method=='POST'):
        search = request.POST.get('search', '')
        age = request.POST.get('age', '')
        print('search : ',search)
        print('age : ',age)
        if(len(search)>=2):
            print("======================")
            print('searching keword : ', search)
            print("======================")
            res_data = {}#전송할 res_data 생성

            qs = Movie.objects.filter(title__contains=search)
            if(len(qs)==0):
                res_data['nothing'] = '1'
                return render(request, 'search.html', res_data)
            else:
                for a in qs:
                    print(a.title)
                    info_list = []
                    info_list.append(a.title)
                    info_list.append(a.main_actor)
                    info_list.append(a.director)
                    info_list.append(a.poster_url)
                    info_list.append(a.vote_average)
                    info_list.append(a.overview)
                    info_list.append(a.release_date)
                    info_list.append(a.id)
                    movies.append(info_list)
                    res_data['movies'] = movies#res_data에 넣어주기
                    # print(res_data.keys())
                    sort_movies['movies'] = movies
                # print('res_data : ',res_data)
                return render(request, 'search.html', res_data)#output에 res_data 전송
        elif(len(search)==1):
            print("1 char input!!!")
            return render(request, 'input.html', {'form':form})
        elif(len(search)==0 and len(age)==0):
            print('0 char input!!!')
            return render(request, 'input.html', {'form':form})       
        else:
            form = InputForm(request.POST)
            if form.is_valid():
                return render(request, 'output.html', {'form':form})
            else:
                return render(request, 'input.html', {'form':form})
        
    else:
        form=InputForm()
        return render(request, 'input.html', {'form':form})

def search(req):
    res_data = {}
    m = sort_movies
    sorted_movies = []
    sort = req.POST.get('sort')
    # print(type(m))
    # print(m['movies'][0][0])
    
    
    if(sort=='asc'):
        id_title = {}
        for movie in m['movies']:
            id_title[movie[0]] = movie[7]
        print(id_title)
        id_title = sorted(id_title.items())
        print(id_title)
        print('=========')
        print(id_title[0][1])
        
        # for i in range(0, len(sorted_id)):
        #     if(sorted_id[i] == movie[7]):
        #         sorted_movies.append(movie)
        
        for ids in id_title:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)

        res_data['movies'] = sorted_movies

    # elif(sort=='desc'):
    
    # else:

    return render(req, 'search.html', res_data)

def output(request):
    #recommended_movie = Movie.objects.get(id='30') 이런식으로
    #recommended_movie = Fcuser.objects.get(id=1)
    #print()
    return render(request, 'output.html')

def f1(x):
    return x[0]
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import InputForm
from metadata.models import Movie, Genre, Movie_Genre
from operator import itemgetter
import os
from PIL import Image, ImageDraw, ImageFont 
import textwrap

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
        sex = request.POST.get('sex', '')
        genre = []
        genre = request.POST.getlist('genre', '')

        print('search : ',search)
        print('sex: ', sex, 'type: ',type(sex))
        print('age : ',age, 'type: ',type(age))
        print('genre: ',genre, 'type: ',type(genre))

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
                    # if(a.poster_url==''):
                    #     a.poster_url = 0
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
                res_data = {}
                res_data['age'] = age
                res_data['sex'] = sex
                res_data['genre'] = genre

                request.session['age'] = age
                request.session['sex'] = sex
                request.session['genre'] = genre
                return render(request, 'loading.html', res_data)
            else:
                return render(request, 'input.html', {'form': form})
    else:
        form = InputForm()
        return render(request, 'input.html', {'form': form})

def search(req):
    res_data = {}
    m = sort_movies
    sorted_movies = []
    sort = req.POST.get('sort')
    
    #정렬
    if(sort=='a_asc'):
        id_title = {}
        for movie in m['movies']:
            id_title[movie[0]] = movie[7]
        
        id_title = sorted(id_title.items())
        print('===sorted id_title===')
        print(id_title)
        
        for ids in id_title:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)

        res_data['movies'] = sorted_movies

    elif(sort=='a_desc'):
        id_title = {}
        for movie in m['movies']:
            id_title[movie[0]] = movie[7]
        id_title = sorted(id_title.items(), reverse=True)
        print('===sorted id_title===')
        print(id_title)
        
        for ids in id_title:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)
        res_data['movies'] = sorted_movies
    elif(sort=='rating'):
        id_rating = {}
        for movie in m['movies']:
            id_rating[movie[4]] = movie[7]
        id_rating = sorted(id_rating.items(), reverse=True)
        print('===sorted id_rating===')
        print(id_rating)
        for ids in id_rating:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)
        
        res_data['movies'] = sorted_movies


    elif(sort=='r_asc'):
        id_date = {}
        for movie in m['movies']:
            id_date[movie[6]] = movie[7]
        id_date = sorted(id_date.items())
        print('===sorted id_rating===')
        print(id_date)
        for ids in id_date:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)
        
        res_data['movies'] = sorted_movies

    elif(sort=='r_desc'):
        id_date = {}
        for movie in m['movies']:
            id_date[movie[6]] = movie[7]
        id_date = sorted(id_date.items(), reverse=True)
        print('===sorted id_rating===')
        print(id_date)
        for ids in id_date:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)
        
        res_data['movies'] = sorted_movies

    return render(req, 'search.html', res_data)


def make_image(message):

    # Image size
    W = 640
    H = 640
    bg_color = 'rgb(214, 230, 245)'  # 아이소프트존

    font = ImageFont.truetype("./static/arial.ttf", size=28)
    font_color = 'rgb(0, 0, 0)'  # or just 'black'
    image = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(image)


    # Text wraper to handle long text
# 40자를 넘어갈 경우 여러 줄로 나눔
#    lines = textwrap.wrap(message, width=40)

    # start position for text
#    x_text = 50
#    y_text = 50

    # 각 줄의 내용을 적음
#    for line in lines:
#        width, height = font.getsize(line)
#        draw.multiline_text((x_text, y_text), line, font=font, fill=font_color)
#        y_text += height
        
        # height는 글씨의 높이로, 한 줄 적고 나서 height만큼 아래에 다음 줄을 적음
    draw.multiline_text((10,10),message, font=font, fill=font_color)
    # 안에 적은 내용을 파일 이름으로 저장
    #downloads_dir = glib.get_user_special_dir(glib.USER_DIRECTORY_DOWNLOAD)
    #path="C:/Users/{}/desktop".format(os.getlogin())
    image.save('./static/movie_result.png',format='PNG')

def output(request):
    msg="Recommended Movie List\n1.Get out\n2.Home Alone\n"+"3.What's up"
    make_image(msg)
    age = request.session['age']
    sex = request.session['sex']
    genre = request.session['genre']
    print('here is output')
    print('here is loading')
    return render(req, 'loading.html')
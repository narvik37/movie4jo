from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import InputForm
from metadata.models import Movie, Genre, Movie_Genre, First_Genre
from operator import itemgetter
from PIL import Image, ImageDraw, ImageFont 
from .AImodels.model1_v2 import ModelFirst

import tensorflow as tf
import numpy as np
import textwrap
import operator
import os
import datetime
import random

sort_movies = {}

def index(req):
    res_data = {}
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    movie_list = []
    
    for i in range(0, 3):
        movie_list.append(movies[i])

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

        if(len(search)>=2):
            print("\n\n================================")
            print('searching keword : ', search)
            print("================================")
            res_data = {}#전송할 res_data 생성

            qs = Movie.objects.filter(title__contains=search)
            
            if(len(qs)==0):
                res_data['nothing'] = '1'
                return render(request, 'search.html', res_data)
            else:
                for a in qs:####################
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
                    genre_names = []
                    gen = Movie_Genre.objects.filter(movie_id=a.id)
                    for g in gen:
                        gn = Genre.objects.get(id=g.genre_id)
                        genre_names.append(str(gn))
                    info_list.append(genre_names)
                    movies.append(info_list)
                    res_data['movies'] = movies#res_data에 넣어주기
                    sort_movies['movies'] = movies
                
                return render(request, 'search.html', res_data)#output에 res_data 전송
        elif(len(search)==1):
            print("1 char input!!!")
            return render(request, 'input.html', {'form':form})
        elif(len(search)==0 and len(genre)==0 and len(age)==0):
            print('0 char input!!!')
            return render(request, 'input.html', {'form':form})       
        
        else:
            form = InputForm(request.POST)
            if form.is_valid():
                request.session['age'] = age
                request.session['sex'] = sex
                request.session['genre'] = genre
                print("\n\n>> Input values")
                print("age: ",age)
                print("sex: ",sex)
                print("genre: ",genre)
                return redirect('/loading_')
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
    
    #정렬####################
    if(sort=='a_asc'):
        id_title = {}
        for movie in m['movies']:
            id_title[movie[0]] = movie[7]
        
        id_title = sorted(id_title.items())
        print('\n\n=== sorted id_title(asc) ===')
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
        print('\n\n=== sorted id_title(desc) ===')
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
        print('\n\n=== sorted id_rating ===')
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
        print('\n\n=== sorted date(asc) ===')
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
        print('\n\n=== sorted date(desc) ===')
        print(id_date)
        for ids in id_date:
            for movie in m['movies']:
                if(movie[7] == ids[1]):
                    sorted_movies.append(movie)
        
        res_data['movies'] = sorted_movies

    return render(req, 'search.html', res_data)

def make_image(message):####################
    # Image size
    W = 1000
    H = 700
    bg_color = 'rgb(214, 230, 245)'  # 아이소프트존

    font = ImageFont.truetype("./static/arial.ttf", size=28)
    font_color = 'rgb(0, 0, 0)'  # or just 'black'
    image = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(image)
    draw.multiline_text((10,10),message, font=font, fill=font_color)
    # 안에 적은 내용을 파일 이름으로 저장
    #downloads_dir = glib.get_user_special_dir(glib.USER_DIRECTORY_DOWNLOAD)

    image.save('./static/movie_result.png',format='PNG')

def output(request):
    res_data = {}
    
    age = request.session['age']
    sex = request.session['sex']
    genre = request.session['genre']
    movieId_list = request.session['movie_list']
    movie_score_list = request.session['movie_score_list'] #평점정보
    
    res_data['age'] = age
    res_data['sex'] = sex
    res_data['genre'] = genre

    movie_title_list=[] #사진으로 저장하기 할때 쓸 용도

    movie_list = []

    movies = []
    print('\n\n>> 영화 추천 결과')####################
    for i in range(len(movieId_list)):
        a = Movie.objects.get(id=movieId_list[i])
        info_list = []
        info_list.append(a.title)
        print(a.title)
        movie_title_list.append(a.title) #사진으로 저장하기 할때 쓸 용도
        info_list.append(a.main_actor)
        info_list.append(a.director)
        info_list.append(a.poster_url)
        info_list.append(a.vote_average)
        info_list.append(a.overview)
        info_list.append(a.release_date)
        info_list.append(a.id)
        genre_names = []
        gen = Movie_Genre.objects.filter(movie_id=a.id)
        for g in gen:
            gn = Genre.objects.get(id=g.genre_id)
            genre_names.append(str(gn))
        info_list.append(genre_names)
        info_list.append(movie_score_list[i])
        movies.append(info_list)
        res_data['movies'] = movies#res_data에 넣어주기
        sort_movies['movies'] = movies#sort_movies에 넣어주기(sort용 변수)

    
    msg="Movies for you!\n"
    for i in range(20):
        msg += "\n"+str(i+1)+". "+movie_title_list[i]

    make_image(msg)

    #output 정렬####################

    m = sort_movies
    sorted_movies = []
    sort = request.POST.get('sort')

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


    return render(request, 'output.html', res_data)

def loading(request):
    
    flag=0
    
    age = int(request.session['age'])
    genre = request.session['genre']
    
    if(request.session['sex']=='man'):
        sex=77
    else:
        sex=70

    # model 1####################
    print("\n\n>> Model1 시작: ",datetime.datetime.now())
    mf = ModelFirst()
    result = mf.model1(genre)
    print(">> 추천된 장르(model1): ",result,"\n\n")
    
    #print(">> Model2에 넣을 데이터처리 시작: ",datetime.datetime.now())
    new_result=[]

    # genre_id함수를 통해 장르 이름을 id값으로 반환해주는 반복문
    for idx in range(len(result)):
        result[idx] = genre_id(result[idx])

    
    # 추천된 장르에 해당하는 영화 id들 list로 저장 ->db에서 genre[0,1,2]에 해당하는 영화 id들 select
    # model2에 넣어줄 영화 id목록
    genre1_list=[] 
    genre2_list=[]
    genre3_list=[]

    ####################
    # genre 1 list    
    qs = Movie_Genre.objects.filter(genre_id=result[0])
    if(len(qs)==0):
        print("SELECT error")
    rand_nums = rand(qs)
    for i in range(len(rand_nums)):
        genre1_list.append(int(qs[rand_nums[i]].movie_id))

    # genre 2 list    
    qs = Movie_Genre.objects.filter(genre_id=result[1])
    if(len(qs)==0):
        print("SELECT error")
    rand_nums = rand(qs)
    for i in range(len(rand_nums)):
        genre2_list.append(int(qs[rand_nums[i]].movie_id))

    # genre 3 list    
    qs = Movie_Genre.objects.filter(genre_id=result[2])
    if(len(qs)==0):
        print("SELECT error")
    rand_nums = rand(qs)
    for i in range(len(rand_nums)):
        genre3_list.append(int(qs[rand_nums[i]].movie_id))

   
    # 저장된 list를 for문으로 model2 에 넣어서 돌리기 (랜덤으로 몇개 뽑아서 넣을지 or 다 넣을지 결정)
    # model 2 로드
    model2 = tf.keras.models.load_model('pages/AImodels/model-02')
    id_score_dict = {} # movieID, 선호도 저장할 딕셔너리

    
    print("\n\n>> Model2 시작: ",datetime.datetime.now())

    ####################
    # genre 1 CNN 돌리기
    N = len(genre1_list)
    for i in range(N):
        input_arr = [[[genre1_list[i], age], [sex, result[0]]]] # 영화 id, 나이, 성별, 장르 id // 여자 70, 남자 77
        samples_to_predict = np.array(input_arr)
        predictions = model2.predict(samples_to_predict)
        # print("이 영화에 대한 사용자의 선호도(model2): ",predictions[0][0])
        id_score_dict[genre1_list[i]]=predictions[0][0] #862는 movieID
        # 영화 id랑 선호도값(predictions) 매칭시켜서 저장해놓기 (딕셔너리형태 좋을듯)

    # # genre 2 CNN돌리기
    N = len(genre2_list)
    for i in range(N):
        input_arr = [[[genre2_list[i], age], [sex, result[1]]]]
        samples_to_predict = np.array(input_arr)
        predictions = model2.predict(samples_to_predict)
        id_score_dict[genre2_list[i]]=predictions[0][0]

    # # genre 3 CNN 돌리기
    N = len(genre3_list)
    for i in range(N):
        input_arr = [[[genre3_list[i], age], [sex, result[2]]]]
        samples_to_predict = np.array(input_arr)
        predictions = model2.predict(samples_to_predict)
        id_score_dict[genre3_list[i]]=predictions[0][0]

    #print(">> Model2 끝: ",datetime.datetime.now())


    # 매칭시켜서 저장해놓은 딕셔너리에서 사용자의 선호도 top 10개 영화 id 찾기
    sorted_dict = sorted(id_score_dict.items(), reverse=True, key=operator.itemgetter(1))
    print("\n\n>> 영화id, 예상평점")
    print(sorted_dict)
    
    recommended_movies_id = []
    recommended_movies_score = []

    for i in range(20):#정렬된 영화를 순차적으로 추천 영화에 넣어주기
        recommended_movies_id.append(sorted_dict[i][0])
        recommended_movies_score.append(str(sorted_dict[i][1]))
    
    print("\n\n>> 예상평점 상위 20개 영화의 id, 예상평점")
    for i in range(20):
        print(recommended_movies_id[i],end='')
        print(", ",recommended_movies_score[i])

    request.session['movie_list'] = recommended_movies_id
    request.session['movie_score_list']= recommended_movies_score

    flag=1
    if(flag==1):
        return redirect('/output')

    return render(request, 'loading.html')

def loading_(req):
    return render(req, 'loading_.html')

def rand(q):
    a = random.sample(range(0, len(q)), 50)
    return a

def genre_id(genre):
    genre_list = {
        "Crime" : 9, "Action" : 8, "Drama" : 7, "Romance" : 6, "Fantasy" : 5, "Adventure" : 4, "Family" : 3, "Movie" : 22, "TV" : 21, "Western" : 20, 
        "Comedy" : 2, "War" : 19, "Documentary" : 18, "Music" : 17, "Foreign" : 16, "Mystery" : 15, "Fiction" : 14, "Science" : 13, "History" : 12, "Horror" : 11, 
        "Thriller" : 10, "Animation" : 1 

    }
    result = genre_list.get(genre, '')
    return result
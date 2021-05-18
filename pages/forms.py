from django import forms
from django.core.exceptions import ValidationError
from .variables import input_age, input_genres, input_sex


class InputForm(forms.Form):
    CHOICES_SEX = (
        ('man', '남성'),
        ('woman', '여성'),
    )
    CHOICES_GENRE = (
        ('animation', '애니메이션'),('comedy', '코미디'),('family', '가족'),
        ('adventure', '모험'),('fantasy', '판타지'),('romance', '로맨스'),
        ('drama', '드라마'),('action', '액션'),('crime', '범죄'),
        ('thriller', '스릴러'),('horror', '공포'),('history', '역사'),
        ('science', '과학'),('fiction', '소설'),('mystery', '미스터리'),
        ('foreign', '이국적인'),('music', '음악'),('documentary', '다큐멘터리'),
        ('war', '전쟁'),('western', '서부'),('tv', 'TV'),('movie', 'movie'),
    )
    sex = forms.ChoiceField(choices=CHOICES_SEX, label="성별")
    age = forms.IntegerField(label="나이",widget=forms.TextInput(attrs={'placeholder': '숫자를 입력하세요'}))
    genre = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=CHOICES_GENRE, label="선호 장르")
    
    # genress = []
    def clean(self):
        data = super().clean()
        #sex=data.get('sex')
        #age=data.get('age')
        genres=data.get('genre','')
        print("################################")
        print(genres)
        print("##########################3")
        if (len(genres) != 2):
            
            raise ValidationError("오류: 장르를 2개 선택하세요!!")
        
        #input_age = age
        #input_sex = sex
        #input_genres = genres
        
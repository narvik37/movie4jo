from django import forms
from django.core.exceptions import ValidationError
from .variables import input_age, input_genres, input_sex


class InputForm(forms.Form):
    CHOICES_SEX = (
        ('man', '남성'),
        ('woman', '여성'),
    )
    CHOICES_GENRE = (
        ('Animation', '애니메이션'),('Comedy', '코미디'),('Family', '가족'),
        ('Adventure', '모험'),('Fantasy', '판타지'),('Romance', '로맨스'),
        ('Drama', '드라마'),('Action', '액션'),('Crime', '범죄'),
        ('Thriller', '스릴러'),('Horror', '공포'),('History', '역사'),
        ('Science', '과학'),('Fiction', '소설'),('Mystery', '미스터리'),
        ('Foreign', '이국적인'),('Music', '음악'),('Documentary', '다큐멘터리'),
        ('War', '전쟁'),('Western', '서부'),('TV', 'TV'),('Movie', 'movie'),
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
        if (len(genres) != 2):
            
            raise ValidationError("오류: 장르를 2개 선택하세요!!")
        
        #input_age = age
        #input_sex = sex
        #input_genres = genres
        
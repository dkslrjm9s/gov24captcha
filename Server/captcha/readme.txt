django 프로젝트 생성
django-admin startproject [프로젝트이름]

생성 후 기본 셋팅
settings - Project Interpreter에서 가상환경 생성 및 django 설치
run configurations 설정에서 runserver 0.0.0.0:8000과 Python interfpreter 지정

main app > settings.py > 
ALLOWED_HOSTS = ['*'] # 모든 호스트가 접속가능
TIME_ZONE = 'Asia/Seoul' # 서울로 시간만 변경


restful framework 설정
main app > settings.py > 
INSTALLED_APPS = [
    'rest_framework',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

main app > urls.py > 
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] # 꼭 해야돼...? 


# 구조

request
get

/img/img.png 파일 남아 있는지 확인 후 있으면 지움

정부24 이미지 로드 후 저장 /img/img.png 경로에

해석

/data 폴더에 img(uuid_result값.png) 저장하고


result, time 반환



html 에서는 저 이미지 파일 로드 하고 없으면 뭐 안부르겠징..



소스 작성

# gov24captcha app 생성

python manage.py startapp [app이름]
main app > settings.py > app 추가



app 이름 > models.py
# model 생성

결과값 저장 모델
img : img 파일명(uuid_result.png) imgField
result : 해석 결과
time : 소요 시간
create : 생성시간

python manage.py makemigrations
python manage.py migrate

app 이름 > serializers.py
#model을 json 화 할 수 있는 serializer 필요


app 이름 > views.py
기능 구현

1. AnalysisResult GET

/img/img.png 파일 남아 있는지 확인 후 있으면 지움

정부24 이미지 로드 후 저장 /img/img.png 경로에

해석

/data 폴더에 img(uuid_result값.png) 저장하고


result, time 반환



html 에서는 저 이미지 파일 로드 하고 없으면 뭐 안부르겠징..




utl 생성
main app > urls.py
view와 연결


templat 생성
메인프로젝트 > templates > 앱이름 > ...html




 <img src="{% static "myapp/{{user.first_name}}_{{user.last_name}}.jpg" %}" alt="Profile Picture">

<img src ="{% static 'myapp/' %}{{user.first_name}}_{{user.last_name}}.jpg" alt="Profile Picture">





OSError: SavedModel file does not exist at: locationC\{saved_model.pbtxt|saved_model.pb}


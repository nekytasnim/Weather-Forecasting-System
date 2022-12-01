from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homePage, name='home'),
    path('article_page', views.articlePage, name='articles'),
    path('today_page', views.todayPage, name='today'),
    path('hourly', views.hourlyPage, name='hourly_page'),
    path('daily', views.dailyPage, name='daily_page'),
    path('health&activity', views.healthPage, name='health'),
    path('minute_cast', views.minutePage, name='air_quality_page'),
    path('air_quality', views.airPage, name='air_quality_page')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from .views import *
from django.conf.urls.static import static
from sports.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('', home, name="home"),
    path('match/all/', match, name="match"),
    path('match/create/', matchCreate, name="matchCreate"),
    path('team/', teams, name="teams"),
    path('team/<str:pk>/', team, name="team"),
    path('team-add/', teamAdd, name="teamAdd"),
    path('team-edit/<str:pk>/', teamEdit, name="teamEdit"),
    path('team-delete/<str:pk>/', teamDelete, name="teamDelete"),
    path('players/', players, name="players"),
    path('player-add/', playerAdd, name="playerAdd"),
    path('player-edit/<str:pk>/', playerEdit, name="playerEdit"),
    path('player-delete/<str:pk>/', playerDelete, name="playerDelete"),
    path('match/<str:pk>/team/<str:pk2>/', teamPlayers, name="teamPlayers"),
    path('match/<str:pk>/team/<str:pk2>/Create/<str:pk3>/', teamPlayersCreate, name="teamPlayersCreate"),
    path('match/<str:pk>/team/<str:pk2>/Delete/<str:pk3>/', teamPlayersDelete, name="teamPlayersDelete"),
    path('score/<str:pk>/', score, name="score"),
    path('scoreadd/<str:pk2>/<str:pk>/', scoreAdd, name="scoreAdd"),
    path('signin/', signin, name="signin"),
    path('profile/', profile, name="profile"),
    path('logout/', logout, name="logout"),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
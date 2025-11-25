from django.urls import path
from .views import GameView, GameDetailView 

urlpatterns = [
    path('games/', GameView.as_view(), name='created_game'),
    path('games/<int:id>/', GameDetailView.as_view(), name='game_detail')
    
]

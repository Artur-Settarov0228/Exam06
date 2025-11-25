from django.urls import path
from .views import Players, PlayerDetail

urlpatterns = [
    path('players/',Players.as_view(),name='create_player' ),
    path('players/<int:id>/',PlayerDetail.as_view(), name='player_detail'),
]

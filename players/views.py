from django.shortcuts import render
import json
from django.http import HttpRequest, JsonResponse
from django.db.models import Q
from .models import Player
from django.shortcuts import get_object_or_404
from django.views import View


class Players(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body.decode())
        required_fields = ['nickname', 'country']

        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {'error': f'{field} maydoni majburiy'},
                     status=400
                    )
        player_new = Player(
            nickname = data['nickname'],
            country = data['country'],
            rating = data.get('rating', 0)
        )
        player_new.full_clean()
        player_new.save()

        response_data = {
            'id': player_new.id,
            'nickname' : player_new.nickname,
            'country' : player_new.country,
            'rating': player_new.rating,
            'created_at' : player_new.created_at.isoformat()
        }
        return JsonResponse(response_data, status = 201)
    
    def get(self, request: HttpRequest) -> JsonResponse:
        players = Player.objects.all()

        country = request.GET.get('country')
        min_rating = request.GET.get('min_rating')
        search = request.GET.get('search')

        if country:
            players = players.filter(country__iexact = country)
        if min_rating:
            try:
                min_rating = int(min_rating)
                players = players.filter(rating__gte = min_rating)
            except ValueError:
                return JsonResponse({'error': 'min_rating must be integer'}, status = 400)

        if search:
            players = players.filter(
                 Q(nickname__icontains=search)
            )

        results = []
        for player in players:
            results.append({
               'id': player.id,
                'nickname': player.nickname,
                'country': player.country,
                'rating': player.rating,
                'total_games': 0,   
                'wins': 0,        
                'draws': 0,         
                'losses': 0,      
                'created_at': player.created_at.isoformat()
                })    
            response_data = {
                'count': len(results),
                'next': None,     
                'previous': None, 
                'results': results
            }
            
            return JsonResponse(response_data)
            
         
        return JsonResponse({'error': 'Server error'}, status=500)  

class PlayerDetail(View):
    def get(self, request:HttpRequest, id:int) -> JsonResponse:
        try:
            player = get_object_or_404(Player, id=id)
            response_data = {
                'id': player.id,
                'nickname': player.nickname,
                'country': player.country,
                'rating': player.rating,
                'total_games': player.total_games,
                'wins': player.wins,
                'draws': player.draws,
                'losses': player.losses,
                'created_at': player.created_at.isoformat()
            }
            return JsonResponse(response_data, status = 201)
            
        except Exception as e:
            return JsonResponse({'error': 'Server error'}, status=500)
        


    def patcht(self, request:HttpRequest, id:int) -> JsonResponse:
        player = get_object_or_404(Player, id=id)
        data = json.loads(request.body.decode())

        if 'nickname' in data:
            player.nickname = data['nickname']
        if 'country' in data:
            player.country = data['country']   
        if 'rating' in data:
            player.rating = data['rating']
            try:
                rating = int(data['rating'])  
                player.rating = rating
            except ValueError:
                return JsonResponse(
                    {'error': 'rating must be integer'}, 
                        status=400
                    )
            player.full_clean()
            player.save()

            response_data = {
                'id': player.id,
                'nickname': player.nickname,
                'country': player.country,
                'rating': player.rating,
                'total_games': player.total_games,
                'wins': player.wins,
                'draws': player.draws,
                'losses': player.losses,
                'created_at': player.created_at.isoformat()
            }
            return JsonResponse(response_data, status = 201)
    
    def delete(self, request: HttpRequest, id:int) -> JsonResponse:
        try:
            player = Player.objects.get(id=id)
        except Player.DoesNotExist:
            return JsonResponse({"message": "player topilmadi"}, status=404)

        player.delete()

        return JsonResponse({"error": "Cannot delete player with game history. Player has 45 recorded games."}, status=200)


       



        

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from django.views import View
import json
from .models import Game


class GameView(View):
    def post(self, request:HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body.decode())

            required_fields = ['title', 'location', 'start_date']
            for field in required_fields:
                if field not in data:
                    return JsonResponse(
                        {'error': f'{field} maydoni majburiy'}, status= 400
                    )
                game = Game(
                title=data['title'],
                location=data['location'],
                start_date=data['start_date'],
                description=data.get('description', '')
                )
                game.full_clean()
                game.save()

                response_data = {
                'id': game.id,
                'title': game.title,
                'location': game.location,
                'start_date': game.start_date.isoformat(),
                'description': game.description,
                'created_at': game.created_at.isoformat()
            }
                return JsonResponse(response_data, status = 201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': dict(e.message_dict)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Server error'}, status=500)
    
class GameDetailView(View):
    def get(self, request:HttpRequest, id:int) -> JsonResponse:
        game = get_object_or_404(Game, id=id)
        response_data = {
            'id': game.id,
            'title': game.title,
            'location': game.location,
            'start_date' : game.start_date.isoformat(),
            'description': game.description,
            'created_at' : game.created_at.isoformat()
        }
        return JsonResponse(response_data, status=201)
    
    def patch(self, request:HttpRequest, id:int) -> JsonResponse:
        
        game = get_object_or_404(Game, id=id)
        data = json.loads(request.body.decode())

        if 'title' in data:
            game.title = data['title']
        if 'location' in data['location']:
            game.location = data['location']

        if 'start_date' in data:
            game.start_date = data['start_date']
        if 'description' in data:
            game.description = data['description']

        game.full_clean()
        game.save()  

        response_data = {
            'id' : game.id,
            'title' : game.title,
            'location': game.location,
            'start_date' : game.start_date.isoformat(),
            'created_at' : game.created_at.isoformat()
        }      
        return JsonResponse(response_data, status = 201)    
    
    def delete(self, request:HttpRequest,id:int) -> JsonResponse:
        game = get_object_or_404(Game, id=id)
        game.delete()
        return JsonResponse(
            {
               "error": "Cannot delete game with existing scores. Tournament has active games."
            }
        )





        
import json

from django.http import HttpRequest,JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from games.models import Game
from players.models import Player
from .models import Score


def to_json(score:Score,game:Game,player:Player):
    return {
    "id": score.pk,
    "game": {
        "id": game.pk,
        "title":game.title
    },
    "player": {
        "id": player.pk,
        "nickname": player.nickname
    },
    "result":score.result ,
    "points": score.points,
    "opponent_name": score.opponent_name,
    "created_at": score.created_at.isoformat()
    }

class ScoriesView(View):
    def get(self, request: HttpRequest, id=None) -> JsonResponse:
        if id is not None:  
            get_score = get_object_or_404(Score, pk=id)
            return JsonResponse(to_json(get_score, get_score.game, get_score.player), safe=False)

        scores = Score.objects.all()
        game_id = request.GET.get('game_id')
        player_id = request.GET.get('player_id')
        result = request.GET.get('result')

        if game_id:
            get_game = get_object_or_404(Game, pk=game_id)
            scores = scores.filter(game=get_game)

        if player_id:
            get_player = get_object_or_404(Player, pk=player_id)
            scores = scores.filter(player=get_player)

        if result and result in ['win', 'draw', 'loss']:
            scores = scores.filter(result=result)

    
        return JsonResponse([to_json(score, score.game, score.player) for score in scores], safe=False)

    def post(self,request:HttpRequest)->JsonResponse:
        data = json.loads(request.body.decode())

        game = data.get('game')
        player = data.get('player')
        result = data.get('result')
        opponent_name = data.get('opponent_name')

        if game is None:
            return JsonResponse({'game':'Required'},status = 400)
        if not str(game).isdigit():
            return JsonResponse({"game":'required id'},status = 400)
        if player is None:
            return JsonResponse({'player':'Required'},status = 400)
        if not str(player).isdigit():
            return JsonResponse({"player":'required id'},status = 400)
        if result is None:
            return JsonResponse({'result':'Required'},status = 400)
        if result not in ['win','draw','loss']:
            return JsonResponse({"message":"result reqired in win,draw,loss"})

        if result == 'win':
            points = 10
        elif result == 'draw':
            points = 5
        elif result == 'loss':
            points = 0

        get_game = get_object_or_404(Game,pk=game)
        get_player = get_object_or_404(Player,pk=player)
        get_player.rating += points
        get_player.save()
        new_scories = Score(
                game = get_game,
                player = get_player,
                result = result,
                points = points,
                opponent_name = opponent_name
        )
        new_scories.save()
        return JsonResponse(data=to_json(new_scories,get_game,get_player),status = 201)
   
    def delete(self,request:HttpRequest,id)->JsonResponse:
        get_score = get_object_or_404(Score,pk=id)
        get_player = get_score.player
        get_player.rating -= float(get_score.points)
        get_player.save()
        get_score.delete()
        return JsonResponse({"delete":"succes"},status=204)
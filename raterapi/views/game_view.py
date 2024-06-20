from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Rating, Review, Image, Game
from .category_view import CategorySerializer

class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'estimated_time_to_play', 'age_recommendation', 'categories']



class GameViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            games = Game.objects.get(pk=pk)
            serializer = GameSerializer(games, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

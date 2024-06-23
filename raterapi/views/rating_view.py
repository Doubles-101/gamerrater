from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Rating, Game

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['id', 'game', 'rating_number']

class RatingViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        game_id = request.data.get('game')
        rating_number = request.data.get('rating_number')

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        rating = Rating.objects.create(
            user=request.auth.user,
            game=game,
            rating_number=rating_number
        )

        serializer = RatingSerializer(rating, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Rating, Review, Image, Game
from .category_view import CategorySerializer

class GameSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user
    
    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Game
        fields = ['id', 'user', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'estimated_time_to_play', 'age_recommendation', 'is_owner', 'categories', 'average_rating']



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
        
    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get('title')
        description = request.data.get('description')
        designer = request.data.get('designer')
        year_released = request.data.get('year_released')
        number_of_players = request.data.get('number_of_players')
        estimated_time_to_play = request.data.get('estimated_time_to_play')
        age_recommendation = request.data.get('age_recommendation')

        # Create a book database row first, so you have a
        # primary key to work with
        game = Game.objects.create(
            user=request.auth.user,
            title=title,
            description=description,
            designer=designer,
            year_released=year_released,
            number_of_players=number_of_players,
            estimated_time_to_play=estimated_time_to_play,
            age_recommendation=age_recommendation,
            )

        # Establish the many-to-many relationships
        category_ids = request.data.get('categories', [])
        game.categories.set(category_ids)

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            game.title = request.data.get('title', game.title)
            game.description = request.data.get('description', game.description)
            game.designer = request.data.get('designer', game.designer)
            game.year_released = request.data.get('year_released', game.year_released)
            game.number_of_players = request.data.get('number_of_players', game.number_of_players)
            game.estimated_time_to_play = request.data.get('estimated_time_to_play', game.estimated_time_to_play)
            game.age_recommendation = request.data.get('age_recommendation', game.age_recommendation)

            category_ids = request.data.get('categories', [])
            if category_ids:
                game.categories.set(category_ids)

            game.save()

            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
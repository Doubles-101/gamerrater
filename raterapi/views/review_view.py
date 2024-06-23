from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Review, Game

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'comment', 'game_id', 'user_id']

class ReviewViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        chosen_game = request.query_params.get('gameId', None)

        # Did the client use the `game` query string parameter?
        if chosen_game is not None:

            # First, get the game from the database to see if a valid one was requested
            try:
                game = Game.objects.get(pk=chosen_game)
            except Game.DoesNotExist:
                return Response(
                    {'message': 'You requested reviews for a non-existent game'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Valid game `id` specified. Filter all reviews by that game.
            reviews = Review.objects.filter(game=game)
            serialized = ReviewSerializer(reviews, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)

        # Client did NOT specify `game` query string param, so get all of 'em
        reviews = Review.objects.all()
        serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Get the data from the client's JSON payload
        comment = request.data.get('comment')
        game_id = request.data.get('gameId')

        # Create a book database row first, so you have a
        # primary key to work with
        review = Review.objects.create(
            user=request.auth.user,
            comment=comment,
            game_id=game_id,       
            )


        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
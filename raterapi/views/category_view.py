from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        games = Category.objects.all()
        serializer = CategorySerializer(games, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
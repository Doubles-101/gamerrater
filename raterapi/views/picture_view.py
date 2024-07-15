from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Review, Game, GamePicture
import uuid
import base64
from django.core.files.base import ContentFile

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePicture
        fields = '__all__'

class PictureViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        pass

    def create(self, request):
        try:
            game_picture = GamePicture()
            game_id = request.data.get("game_id")
            game_image = request.data.get("game_image")

            format, imgstr = game_image.split(';base64,')
            imgstr += "=="
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'{game_id}-{uuid.uuid4()}.{ext}')

            game_picture.action_pic = image_data
            game_picture.game_id = request.data.get("game_id")


            game_picture.save()

            serializer = PictureSerializer(game_picture)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
 
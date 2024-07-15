from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from raterapi.views import UserViewSet, GameViewSet, CategoryViewSet, ReviewViewSet, RatingViewSet, PictureViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter(trailing_slash=False)
router.register(r'games', GameViewSet, 'game')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'reviews', ReviewViewSet, 'review')
router.register(r'ratings', RatingViewSet, 'rating')
router.register(r'pictures', PictureViewSet, 'picture')

urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include, reverse
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'blog', BlogViewSet)


app_name = 'blog'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', BlogViews, name='home'),
    path('blog/<slug:slug>/', BlogDetail, name='detail'),
    path('signup/', SignUp, name='signup'),
    path('success/', Success, name='success'),
    path('contact/', Contact, name='contact'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
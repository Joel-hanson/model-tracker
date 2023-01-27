from django.urls import path

from rest_framework.routers import DefaultRouter

from .routes import routes

router = DefaultRouter()

for route in routes:
    router.register(route["regex"], route["viewset"], basename=route["basename"])

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
] + router.urls

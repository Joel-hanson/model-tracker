from common.tasks import hello_world
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# class IndexView(generic.TemplateView):
#     template_name = 'common/index.html'


class RestViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        url_path="rest-check",
    )
    def rest_check(self, request):
        return Response(
            {"result": "If you're seeing this, the REST API is working!"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        url_path="celery-check",
    )
    def celery_check(self, request):
        hello_world.delay()
        return Response(
            {"result": "Triggered by Celery task!"},
            status=status.HTTP_200_OK,
        )

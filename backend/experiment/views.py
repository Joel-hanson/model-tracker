import json

from django.views.generic.base import TemplateView
from django_celery_results.models import TaskResult
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ModelRunSerializer
from .tasks import wine_quality
from .utils import make_task_url


class ModelFlowViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = ModelRunSerializer

    def list(self, request):
        # return a rule for the wine quality api view
        wine_quality_url = request.build_absolute_uri("wine-quality/")
        wine_quality_tasks_url = request.build_absolute_uri("wine-quality/tasks/")
        return Response(
            {
                "wine_quality": wine_quality_url,
                "wine_quality_tasks": wine_quality_tasks_url,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="wine-quality",
        serializer_class=ModelRunSerializer,
    )
    def wine_quality_view(self, request, *args, **kwargs):
        if request.method == "GET":
            return Response(
                {
                    "message": "This is the wine quality api",
                    "example_input": {"alpha": 0.5, "l1_ratio": 0.5},
                },
                status=status.HTTP_200_OK,
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_kwargs = serializer.validated_data["input"]
        task = wine_quality.delay(**task_kwargs)
        task_url = make_task_url(task, request, "modelflow-get-task")
        return Response(
            {
                "task_id": task.id,
                "task": task_url,
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="wine-quality/tasks",
    )
    def get_tasks(self, request, *args, **kwargs):
        tasks = TaskResult.objects.filter(task_name="experiment.tasks.wine_quality")
        return Response(
            [
                {
                    "task_id": task.task_id,
                    "status": task.status,
                    "result": task.result,
                    "url": f"{request.build_absolute_uri()}{task.task_id}",
                }
                for task in tasks
            ],
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get"],
        # url path that point when given wine-quality/task/<task_id> or wine-quality/tasks/<task_id>
        url_path="wine-quality/tasks?/(?P<task_id>[^/.]+)",
    )
    def get_task(self, request, *args, **kwargs):
        task = TaskResult.objects.get(task_id=kwargs["task_id"])
        try:
            result = json.loads(task.result)
        except json.JSONDecodeError:
            result = task.result
        return Response(
            {
                "task_id": task.task_id,
                "status": task.status,
                "result": result,
            },
            status=status.HTTP_200_OK,
        )


# Display a html page with the result of the task
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = TaskResult.objects.all()
        return context


class ModelResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = TaskResult.objects.filter(task_name="experiment.tasks.wine_quality")
        context["results"] = []
        context["keys"] = []
        for task in tasks:
            try:
                task.result = json.loads(task.result)
            except json.JSONDecodeError:
                pass
            context["results"].append(task.result)
            context["keys"] = set(list(task.result.keys()) + list(context["keys"]))
        return context

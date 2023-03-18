from common import urls as common_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from experiment.views import IndexView, ModelResultView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("results/", ModelResultView.as_view(), name="result"),
    path("admin/", admin.site.urls),
    path("common/", include(common_urls), name="common"),
    path("tasks/", include("experiment.urls"), name="tasks"),
    path("experiment/", include("experiment.urls"), name="tasks"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

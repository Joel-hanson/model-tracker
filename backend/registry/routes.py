from .views import ModelFlowViewSet

app_name = "registry"

routes = [
    {"regex": r"", "viewset": ModelFlowViewSet, "basename": "modelflow"},
]

from .views import ModelFlowViewSet

app_name = "experiment"

routes = [
    {"regex": r"", "viewset": ModelFlowViewSet, "basename": "modelflow"},
]

from .views import RestViewSet

app_name = "common"

routes = [
    {"regex": r"", "viewset": RestViewSet, "basename": "Rest"},
]

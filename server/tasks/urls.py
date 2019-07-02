from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, base_name='tasks')
urlpatterns = router.urls
from django.contrib import admin
from django.urls import include, path
from task_manager import views


urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("labels/", include("labels.urls")),
    path("tasks/", include("tasks.urls")),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
]

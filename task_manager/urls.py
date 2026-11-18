from django.contrib import admin
from django.urls import path, include
from task_manager import views
from task_manager.users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('task_manager.users.urls')),
    path('login/', users_views.UserLoginView.as_view(), name='login'),
    path('logout/', users_views.UserLogoutView.as_view(), name='logout'),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('sentry-debug/', lambda request: 1 / 0),
]

from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

# namespace:route_name
app_name='projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='all'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/create',
        views.ProjectCreateView.as_view(success_url=reverse_lazy('projects:all')), name='project_create'),
    path('project/<int:pk>/update',
        views.ProjectUpdateView.as_view(success_url=reverse_lazy('projects:all')), name='project_update'),
    path('project/<int:pk>/delete',
        views.ProjectDeleteView.as_view(success_url=reverse_lazy('projects:all')), name='project_delete'),
    path('project/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='project_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('projects:all')), name='project_comment_delete'),
    path('project/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='project_favorite'),
    path('project/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='project_unfavorite'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined


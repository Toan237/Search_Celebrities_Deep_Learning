from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import AddFamousView, ListFamousView, UpdateFamousView, DeleteFamousView, ListVideoView, FamousVideoView, DeleteVideoView, AcceptDeleteVideoView
from .import views 
# from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('getFile/', views.getFile, name='getFile'),
    path('detail_video/<int:id>', views.DetailVideoView, name='detail-video'),
    path('detail_video_search/<int:id>/<int:id1>/', views.DetailVideoSearchView, name='detail-video-search'),
    path('data_search/<int:id>/', views.DataSearchView, name='data-search'),

    path('add_famous/', AddFamousView.as_view(), name='add-famous'),
    path('list_famous/', ListFamousView.as_view(), name='list-famous'),
    path('edit_famous/<int:pk>', UpdateFamousView.as_view(), name='edit-famous'),
    path('delete_famous/<int:pk>/remove', DeleteFamousView.as_view(), name='delete-famous'),

    
    path('add_video/', views.addVideo, name='add-video'),
    path('process_video/', views.processVideo, name='process-video'),
    path('add_label/', views.addLabel, name='add-label'),



    path('list_famous_video/', ListVideoView.as_view(), name='list-famous-video'),
    path('list_name_video/<str:famous>/', views.FamousVideoView, name='list-name-video'),
    path('list_delete_name_video/<int:id>/<str:famous>/remove/', views.DeleteVideoView, name='delete-name-video'),
    path('list_edit_name_video/<int:id>/<str:famous>/edit/', views.UpdateVideoView, name='update-name-video'),
    path('update_video/', views.UpdateDetailsVideoView, name='update-video'),
    path('accept_delete_video/<int:id>/<str:famous>/', views.AcceptDeleteVideoView, name='accept-delete-video'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
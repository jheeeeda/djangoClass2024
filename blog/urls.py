from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('',views.PostList.as_view()),
    # path('<int:pk>/', views.single_post_page),
    # path('', views.index),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
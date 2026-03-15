from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('search/', views.post_search, name='post_search'),
    path('category/<slug:slug>/', views.post_by_category, name='post_by_category'),
    path('tag/<slug:slug>/', views.post_by_tag, name='post_by_tag'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),
]
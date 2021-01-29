from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:blog_id>/update', views.blog_update, name='blog_update'),
    path('blog/<int:blog_id>/delete', views.blog_delete, name='blog_delete'),
    path('category/<str:cats>/', views.category_view, name='category_url'),
    path('add_category/', login_required(views.AddCategoryView.as_view()), name='add_category')
]

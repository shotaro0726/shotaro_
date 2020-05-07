from django.urls import path
from .views import CategoryList, PostList, PostDetail

app_name = 'blog'

urlpatterns = [
    path('api/posts/', PostList.as_view(), name='post_list'),
    path('api/posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('api/category/', CategoryList.as_view(), name='category_list')
]


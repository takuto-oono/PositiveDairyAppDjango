from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post_dairy_content', views.post_dairy_content, name='post_dairy_content'),
    path('get_dairy_content/', views.get_dairy_content, name='get_dairy_content'),
    path('delete_dairy_content/', views.delete_dairy_content, name='delete_dairy_content'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('edit_category/<int:pk>', views.EditCategoryView.as_view(), name='edit_category'),
    path('show_pictures/<int:category_id>', views.ShowPicturesView.as_view(), name='show_pictures'),
]

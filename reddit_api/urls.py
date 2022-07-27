from django.urls import path

from . import views

urlpatterns = [
    path('list-subreddits/', views.get_list_of_sub_reddits),
    path('get-post/',views.get_post_from_id),
    path('get-video/',views.get_comments_from_post_id)
]

##checking if fokring changes forked content 

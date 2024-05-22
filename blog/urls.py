from django.urls import path

from . import views

urlpatterns = [
    #path('', include(router.urls)),
    path("post/", views.postview.as_view(),name="posts"),
    path("post/<int:post_id>/", views.postupdatedelete.as_view(),name="post_update"),
    path("like/<int:post_id>/", views.LikeView.as_view(),name="like"),
    path("comment/<int:post_id>/", views.commentview.as_view(),name="comment"),
    path("commentadjust/<int:comment_id>/", views.commentupdate.as_view(),name="comment_update"),
    #path("search/", views.searchview.as_view(),name="search"),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('searchpost/', BlogPostSearch.as_view(), name='blog-post-search'),
]


# djaneiro

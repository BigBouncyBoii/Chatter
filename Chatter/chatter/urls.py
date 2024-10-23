from django.urls import path

from . import views





urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("global_message", views.global_message, name="global_message"),
    path("get_global_message/<int:id>", views.get_global_message, name="global_message"),
    path("like_global/<int:id>", views.like_global, name="like_global"),
    path("reply_global", views.reply_global, name="reply_global"),
    path("profile/<str:username>", views.profile, name = "profile"),
    path("profile/<str:username>/update_bio", views.update_bio, name="update_bio"),
    path("profile/<str:username>/friend_request", views.friend_request, name = "friend_request"),
    path("profile/<str:username>/unfriend_request", views.unfriend_request, name = "unfriend_request"),
    path("search", views.search, name = "search"),
    path("search_friends", views.search_friends, name = "search_friends"),
    path("direct_home", views.direct_home, name = "direct_home"),
    path("direct/<int:id>", views.direct, name = "direct"),
    path("direct_message/<int:id>", views.direct_message, name = "direct_message"),
    path("get_direct_message/<int:id>/<int:num>", views.get_direct_message, name = "get_direct_message"),
    path("like_direct/<int:id>", views.like_direct, name="like_direct"),
    path("reply_direct/<int:id>", views.reply_direct, name="reply_direct"),
    path("group_home", views.group_home, name = "group_home"),
    path("group_join/<int:id>", views.group_join, name = "group_join"),
    path("group/<int:id>", views.group, name = "group"),
    path("group_message/<int:id>", views.group_message, name = "group_message"),
    path("get_group_message/<int:id>/<int:num>", views.get_group_message, name = "get_group_message"),
    path("like_group/<int:id>", views.like_group, name="like_group"),
    path("reply_group/<int:id>", views.reply_group, name="reply_group"),
    path("group_invite/<int:id>", views.group_invite, name="group_invite"),
    path("search_groups", views.search_groups, name = "search_groups"),
    path("reject_group/<str:username>", views.reject_group, name = "reject_group"),
    
    


]


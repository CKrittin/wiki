from django.urls import path

from . import views
import encyclopedia

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path('new_page', views.new_page, name="new_page"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("random", views.random, name="random")
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index),
    url(r"^register$", views.register),
    url(r"^login$", views.login),
    url(r"^books$", views.books),
    url(r"^books/add$", views.add),
    url(r"^user/books/add$", views.add),
    url(r"^books/record$", views.record),
    url(r"^logout$", views.logout),
    url(r"^books/(?P<book_id>\d+)$", views.detail),
    url(r"^books/(?P<book_id>\d+)/review$", views.review),
    url(r"^user/(?P<user_id>\d+)$", views.user),
    url(r"^books/delete/(?P<review_id>\d+)$", views.delete),
    
    
]
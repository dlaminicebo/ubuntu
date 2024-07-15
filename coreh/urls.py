
from django.contrib import admin
from django.urls import path
from coreh.views import frontpage, shop

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('shop/', shop, name='shop'),

]
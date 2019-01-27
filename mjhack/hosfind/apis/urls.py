from django.urls import path
from .views import *

app_name='apis'

urlpatterns = [
    path('',index, name='index'),
    path('search_category',category_search_using_symptoms,name='category_search_using_symptoms'),
]


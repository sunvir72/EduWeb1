from django.urls import path
from Link5 import views

urlpatterns = [
    path('', views.Link5, name='Link5'),
    path('rowcol/', views.rowcol, name='rowcol'),
    path('classification/', views.classification, name='classification'),
    path('prec/', views.prec, name='prec'),
    path('prec_/', views.prec_, name='prec_'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('set/<str:prise>/<str:onoff>', views.set),
    path('request/<str:prise>', views.request),
    path('schedule', views.schedule)

]
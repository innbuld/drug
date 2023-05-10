from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('doctor', views.doctor, name='doctor'),
    path('pharma', views.pharma, name='pharma'),
    path('prescription', views.prescription, name='prescription'),
    path('report/<int:id>', views.report, name='report'),
    path('logout', views.logout_view, name='logout'),
    path('dispense/<int:id>', views.dispense, name='dispense')
]
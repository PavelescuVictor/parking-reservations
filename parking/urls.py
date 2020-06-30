"""ISS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from .views import (
    ParkingCreateView,
    ParkingDeleteView,
    ParkingUpdateView,
    ParkingListView,
    ParkingDetailView
)
from reservation.views import ReservationnCreateView, ReservationListView, ReservationDeleteView, ReservationDetailView, NetProfit, ReservationUpdateView

urlpatterns = [
    path('', views.home, name='parking-home'),
    path('home/', views.home, name='parking-home'),
    path('about/', views.about, name='parking-about'),
    path('parkinglist/', ParkingListView.as_view(), name='parking-list'),
    path('registerparking/', ParkingCreateView.as_view(), name='parking-register'),
    path('parkinglist/<int:pk>',  ParkingDetailView.as_view(), name='parking-detail'),
    path('parkinglist/<int:pk>/update/', ParkingUpdateView.as_view(), name='parking-update'),
    path('parkinglist/<int:pk>/delete/', ParkingDeleteView.as_view(), name='parking-delete'),
    path('registerreservation/', ReservationnCreateView.as_view(), name='reservation-register'),
    path('reservationlist/', ReservationListView.as_view(), name='reservation-list'),
    path('reservationlist/<int:pk>',  ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservationlist/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation-delete'),
    path('reservationlist/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('netprofit/', NetProfit.as_view(), name='net-profit')
]

from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from .models import Parking, Company, CarLot
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from reservation.models import Reservation

def home(request):

    return render(request, 'parking/home.html')

def about(request):
    return render(request, 'parking/about.html')

class ParkingListView(ListView):
    model = Parking
    template_name = 'parking/parking-list.html'
    context_object_name = 'parkings'


class ParkingDetailView(DetailView):
    model = Parking
    template_name = 'parking/parking-detail.html'

    def get(self, request, *args, **kwargs):
        reservation_list = []
        self.object = self.get_object()
        empty_lots = self.object.total_car_lots
        filled_lots = 0
        net_profite_day = 0
        net_profite_week = 0
        net_profite_month = 0
        net_profite_day_value = 0
        net_profite_week_value = 0
        net_profite_month_value = 0
        net_profite_day_date = datetime.today() - timedelta(days=1)
        net_profite_week_date = datetime.today() - timedelta(days=7)
        net_profite_month_date = datetime.today() - timedelta(days=30)
        print(net_profite_day_date)
        print(net_profite_week_date)
        print(net_profite_month_date)

        for reservation in Reservation.objects.all():
            if self.object == reservation.car_lot.parking:
                reservation_list.append(reservation)
                empty_lots = empty_lots - 1
                filled_lots += 1
                if reservation.start_date.replace(tzinfo=None) > net_profite_day_date.replace(tzinfo=None) and reservation.start_date.replace(tzinfo=None) < datetime.today():
                    if reservation.regime == 1:
                        net_profite_day += 1
                        net_profite_day_value += 60
                    elif reservation.regime == 2:
                        net_profite_day += 1
                        net_profite_day_value += 120
                if reservation.start_date.replace(tzinfo=None) > net_profite_week_date.replace(tzinfo=None) and reservation.start_date.replace(tzinfo=None) < datetime.today():
                    if reservation.regime == 1:
                        net_profite_week += 1
                        net_profite_week_value += 60
                    elif reservation.regime == 2:
                        net_profite_week += 1
                        net_profite_week_value += 120
                if reservation.start_date.replace(tzinfo=None) > net_profite_month_date.replace(tzinfo=None) and reservation.start_date.replace(tzinfo=None) < datetime.today():
                    if reservation.regime == 1:
                        net_profite_month += 1
                        net_profite_month_value += 60
                    elif reservation.regime == 2:
                        net_profite_month += 1
                        net_profite_month_value += 120


        context = {'reservationlist': reservation_list}
        context['object'] = self.object
        context['filledlots'] = filled_lots
        context['emptylots'] = empty_lots
        context['netprofiteday'] = net_profite_day
        context['netprofiteweek'] = net_profite_week
        context['netprofitemonth'] = net_profite_month
        context['netprofitedayvalue'] = net_profite_day_value
        context['netprofiteweekvalue'] = net_profite_week_value
        context['netprofitemonthvalue'] = net_profite_month_value

        return render(request, "parking/parking-detail.html", context=context)


class ParkingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Parking
    fields = ['company', 'address', 'total_car_lots']
    template_name = 'parking/parking-register.html'
    success_url = '/parking/home'
    success_message = "Your praking have been created succesfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ParkingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Parking
    fields = ['status']
    template_name = 'parking/parking-register.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bug = self.get_object()
        if str(self.request.user.groups.all()[0]) == 'Company':
            return True
        return False


class ParkingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Parking
    success_url = '/'
    template_name = 'parking/parking-confirm-delete.html'

    def test_func(self):
        bug = self.get_object()
        if str(self.request.user.groups.all()[0]) == 'Company':
            return True
        return False

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from reservation.models import Reservation
from parking.models import  CarLot, Parking
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from reservation.utils import date_intervals_overlap
from .forms import ReservationForm
from django import forms
from .forms import NetProfitForm


# class ReservationCreateView(View):
#
#     def get(self, request):
#         reservation = ReservationForm()
#
#         return render(request, 'reservation/index.html', {'form': reservation})
#
#     def post(self, request):
#         print("da")
#         reservation_form = ReservationForm(data=request.POST)
#
#         if reservation_form.is_valid():
#             start_date = reservation_form.cleaned_data['start_date']
#             finish_date = reservation_form.cleaned_data['finish_date']
#             parking_space_number = reservation_form.cleaned_data['parking_space_number']
#
#             if Reservation.objects.filter(Q(parking_space_number=parking_space_number,
#                                             start_date__range=[start_date, finish_date]) |
#                                           Q(parking_space_number=parking_space_number,
#                                             finish_date__range=[start_date, finish_date])).exists():
#                 msg = 'Dates overlaps. Try other dates and / or parking space.'
#             else:
#                 msg = 'Reservation taken.'
#                 reservation_form.save()
#                 reservation_form = ReservationForm()
#
#             return render(request, 'reservation/index.html', {'message': msg,
#                                                               'form': reservation_form})
#
#         return render(request, 'reservation/index.html', {'form': reservation_form})


class ReservationListView(ListView):
        model = Reservation
        template_name = 'reservation/reservation-list.html'

        def get(self, request, *args, **kwargs):
            print(self.request.user)
            reservation_list = Reservation.objects.all().filter(author=self.request.user)
            print(reservation_list)

            context = {'reservationlist': reservation_list}

            return render(request, "reservation/reservation-list.html", context=context)


class ReservationnCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Reservation
    fields = ['car_lot', 'description', 'regime', 'start_date', 'repeat', 'repeat_end']
    template_name = 'reservation/reservation-register.html'
    success_url = '/parking/home'
    success_message = "Your reservation have been created succesfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def is_carlot_available(self, start_date, regime, car_lot):
        signal_save = True
        for reservation in Reservation.objects.all().filter(car_lot = car_lot):
            finish_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=int(regime))
            to_be_created_interval = (datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'), finish_date)
            reservation_interval = (reservation.start_date, reservation.get_end_date())

            if date_intervals_overlap(to_be_created_interval, reservation_interval):
                signal_save = False
        return signal_save

    def post(self, request, *args, **kwargs):
        CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status
        if request.POST['repeat'] == '0':
            if self.is_carlot_available(request.POST['start_date'], request.POST['regime'], request.POST['car_lot']) and CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Open':
                return super().post(request, *args, **kwargs)
            elif self.is_carlot_available(request.POST['start_date'], request.POST['regime'], request.POST['car_lot']) == False:
                messages.add_message(self.request, messages.WARNING, 'The car lot is already taken at that time!')
                return redirect('/parking/registerreservation')
            elif CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Temporarily Closed':
                messages.add_message(self.request, messages.WARNING, 'The parking is closed!')
                return redirect('/parking/registerreservation')
        elif request.POST['repeat'] == '1':
            if CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Open':
                return super().post(request, *args, **kwargs)
            elif CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Temporarily Closed':
                messages.add_message(self.request, messages.WARNING, 'The parking is closed!')
                return redirect('/parking/registerreservation')
        elif request.POST['repeat'] == '2':
            if CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Open':
                return super().post(request, *args, **kwargs)
            elif CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Temporarily Closed':
                messages.add_message(self.request, messages.WARNING, 'The parking is closed!')
                return redirect('/parking/registerreservation')
        elif request.POST['repeat'] == '3':
            if CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Open':
                return super().post(request, *args, **kwargs)
            elif CarLot.objects.all().filter(id=request.POST['car_lot'])[0].parking.status == 'Temporarily Closed':
                messages.add_message(self.request, messages.WARNING, 'The parking is closed!')
                return redirect('/parking/registerreservation')


class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    success_url = '/parking/reservationlist'
    template_name = 'reservation/reservation-confirm-delete.html'

    def test_func(self):
        reservation = self.get_object()
        if str(self.request.user.groups.all()[0]) == 'Clients':
            return True
        return False

class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservation
    fields = ['description', 'regime']
    template_name = 'reservation/reservation-register.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if str(self.request.user.groups.all()[0]) == 'Clients':
            return True
        return False

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **dict(kwargs,update=True))

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation/reservation-detail.html'

class NetProfit(forms.Form, LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'parking/net-profite.html'

    def test_func(self):
        if str(self.request.user.groups.all()[0]) == 'Company':
            return True
        return False

    def get(self, request, *args, **kwargs):
        form = NetProfitForm()
        context = {'form': form}
        return render(request, "reservation/net-profit.html", context=context)

    def post(self, request, *args, **kwargs):
        form = NetProfitForm(request.POST)
        net_profit_list = []
        if form.is_valid():
            data = form.cleaned_data
            parking = data.get('parking')
            net_profit_type = data.get('net_profite_type')
            period = data.get('period')
            for i in range(1, int(period)+1):
                net_profit_count = 0
                net_profit_sum = 0
                start_day = datetime.now()
                start_day = start_day - timedelta(days=i)
                end_day = start_day + timedelta(days=1)
                end_day = end_day - timedelta(seconds=1)
                start_week = datetime.now()
                start_week = start_week - timedelta(weeks=i)
                end_week = start_week + timedelta(weeks=1)
                end_week = end_week - timedelta(seconds=1)
                start_month = datetime.now()
                start_month = start_month - relativedelta(months=i)
                end_month = start_month + relativedelta(months=1)
                end_month = end_month - timedelta(seconds=1)
                for j in Reservation.objects.all():
                    if j.car_lot.parking == parking:
                        if net_profit_type == 'Day':
                            if j.start_date.replace(tzinfo=None) > start_day.replace(tzinfo=None) and j.start_date.replace(tzinfo=None) < end_day.replace(tzinfo=None):
                                if j.regime == 1:
                                    net_profit_count += 1
                                    net_profit_sum += 60
                                elif j.regime == 2:
                                    net_profit_count += 1
                                    net_profit_sum += 120
                        elif net_profit_type == 'Week':
                            if j.start_date.replace(tzinfo=None) > start_week.replace(tzinfo=None) and j.start_date.replace(tzinfo=None) < end_week.replace(tzinfo=None):
                                if j.regime == 1:
                                    net_profit_count += 1
                                    net_profit_sum += 60
                                elif j.regime == 2:
                                    net_profit_count += 1
                                    net_profit_sum += 120
                        elif net_profit_type == 'Month':
                            if j.start_date.replace(tzinfo=None) > start_month.replace(tzinfo=None) and j.start_date.replace(tzinfo=None) < end_month.replace(tzinfo=None):
                                if j.regime == 1:
                                    net_profit_count += 1
                                    net_profit_sum += 60
                                elif j.regime == 2:
                                    net_profit_count += 1
                                    net_profit_sum += 120
                start_day = start_day.strftime("%m/%d/%Y, %H:%M:%S")
                start_week = start_week.strftime("%m/%d/%Y, %H:%M:%S")
                start_month = start_month.strftime("%m/%d/%Y, %H:%M:%S")
                end_day = end_day.strftime("%m/%d/%Y, %H:%M:%S")
                end_week = end_week.strftime("%m/%d/%Y, %H:%M:%S")
                end_month = end_month.strftime("%m/%d/%Y, %H:%M:%S")
                if net_profit_type == 'Day':
                    net_profit_list.append((start_day, end_day, net_profit_count, net_profit_sum))
                elif net_profit_type == 'Week':
                    net_profit_list.append((start_week, end_week, net_profit_count, net_profit_sum))
                elif net_profit_type == 'Month':
                    net_profit_list.append((start_month, end_month, net_profit_count, net_profit_sum))
            context = {}
            context['show'] = 'true'
            context['list'] = net_profit_list
            for i in net_profit_list:
                print(i)
            return render(request, "reservation/net-profit.html", context=context)
        else:
            messages.add_message(self.request, messages.WARNING, 'Not valid form!')
            return redirect('/home')

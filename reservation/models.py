from datetime import timedelta

from django.db import models
from parking.models import CarLot
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from .utils import date_intervals_overlap
from copy import deepcopy
from django.urls import reverse


class Reservation(models.Model):
    ONCE = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3

    FAST_CHARGE = 1
    NORMAL = 2

    repeat_options = (
        (ONCE, 'Once'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    )

    regime_options = (
        (NORMAL, 'Normal (2h)'),
        (FAST_CHARGE, 'Fast-Charge (1h)'),
    )

    car_lot = models.ForeignKey(CarLot, related_name='car_lot', verbose_name='CarLot', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reservation', verbose_name='Author', on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=8, null=False, blank=False, default='')

    description = models.TextField(max_length=255)

    start_date = models.DateTimeField()
    regime = models.IntegerField(choices=regime_options, default=NORMAL)

    repeat = models.IntegerField(choices=repeat_options, default=ONCE)
    repeat_end = models.DateTimeField(null=True)
    #plate_number = models.CharField(max_length=8, null=False)

    def get_end_date(self):
        return self.start_date + relativedelta(hours=self.regime)

    def create_periodic_reservations(self, **kwargs):
        date = self.start_date + relativedelta(**kwargs)
        end_repeat = self.repeat_end
        future_reservations = []

        while date <= end_repeat:
            next_reservation = deepcopy(self)
            next_reservation.id = None
            next_reservation.start_date = date
            if next_reservation.is_carlot_available():
                future_reservations.append(next_reservation)
            date += relativedelta(**kwargs)
        Reservation.objects.bulk_create(future_reservations)

    def is_carlot_available(self):
        signal_save = True
        for reservation in Reservation.objects.all():
            to_be_created_interval = (self.start_date, self.get_end_date(),)
            reservation_interval = (reservation.start_date, reservation.get_end_date(),)

            if date_intervals_overlap(to_be_created_interval, reservation_interval):
                signal_save = False
        return signal_save

    def save(self, *args, **kwargs):
        print("da1")
        print(kwargs.keys())
        if 'update' in kwargs.keys():
            print("da2")
            if kwargs['update'] == True:
                print("da3")
                super(Reservation, self).save(*args, **kwargs)
        else:
            if self.is_carlot_available():
                super(Reservation, self).save(*args, **kwargs)

            if self.repeat in (self.DAILY, self.WEEKLY, self.MONTHLY):
                if self.repeat == self.DAILY:
                    self.create_periodic_reservations(days=1)
                elif self.repeat == self.WEEKLY:
                    self.create_periodic_reservations(weeks=1)
                elif self.repeat == self.MONTHLY:
                    self.create_periodic_reservations(months=1)

    def __str__(self):
        return 'Reservation'

    def get_absolute_url(self):
        return reverse('reservation-detail', kwargs={'pk': self.pk})
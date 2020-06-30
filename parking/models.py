from django.db import models
from django.urls import reverse

class Company(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return '{}'.format(self.name)


class Parking(models.Model):

    status_choices = (
        ('Temporarily Closed', 'Temporarily Closed'),
        ('Open', 'Open')
    )

    company = models.ForeignKey(Company, related_name='parking', verbose_name='Company', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, unique=True, null=False)
    total_car_lots = models.PositiveSmallIntegerField(null=True)
    status = models.CharField(max_length=18, choices=status_choices, default='Open')

    def create_car_lots(self):
        CarLot.objects.bulk_create([
            CarLot(parking=self, order_number=order) for order in range(1, self.total_car_lots + 1)
        ])

    def save(self, *args, **kwargs):
        super(Parking, self).save(*args, **kwargs)
        self.create_car_lots()

    def __str__(self):
        return '{}'.format(self.address)

    def get_absolute_url(self):
        return reverse('parking-detail', kwargs={'pk': self.pk})


class CarLot(models.Model):

    # AVAILABLE = 0
    # TAKEN = 1
    #
    # STATUS = (
    #     (AVAILABLE, 'Available'),
    #     (TAKEN, 'Taken'),
    # )

    active = models.BooleanField(default=True)
    parking = models.ForeignKey(Parking, related_name='car_lot', verbose_name='Parking', on_delete=models.CASCADE)
    # status = models.IntegerField(choices=STATUS, default=AVAILABLE)
    order_number = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return '{} - number: {}'.format(self.parking, self.order_number)


from django.contrib import admin
from .models import Company, Parking, CarLot

admin.site.register(Company)

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    model = Parking
    list_display = ['company', 'address', 'total_car_lots', ]


@admin.register(CarLot)
class CarLotAdmin(admin.ModelAdmin):
    model = CarLot
    list_display = ['id', 'parking', 'order_number', 'get_company_name', ]
    readonly_fields = ['parking', 'order_number', ]

    def get_company_name(self, obj):
        return obj.parking.company.name
    get_company_name.admin_order_field = 'company'
    get_company_name.short_description = 'Company name'

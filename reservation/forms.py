import datetime
from django.forms import ModelForm, DateInput, TextInput, ValidationError
from .models import Reservation
from django import forms
from parking.models import Parking


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['car_lot', 'description', 'regime', 'repeat', 'repeat_end']
        # Validating form fields using widgets
        widgets = {
            'repeat_end': DateInput(attrs={'type': 'date'}),
            'finish_date': DateInput(attrs={'type': 'date'}),
            'parking_space_number': TextInput(attrs={'pattern': '[1-9]+', 'title': 'Enter a valid parking space number'}),
            'phone_number': TextInput(attrs={'pattern': '[0-9]+', 'title': 'Enter digits only '}),
            'name': TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Enter characters only '}),
            'surname': TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Enter characters only '})
        }

# Additional custom validator for start_date / finish_date fields
    def clean(self):
        data = self.cleaned_data
        start_date = data['start_date']
        finish_date = data['finish_date']

        if start_date > finish_date:
            raise ValidationError('Wrong start and finish dates.')

        if start_date < datetime.date.today():
            raise ValidationError('Start date in the past.')

        return data


class NetProfitForm(forms.Form):
    parking = forms.ModelChoiceField(queryset=Parking.objects.all())
    net_profite_type_choices = (
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month'),
    )
    net_profite_type = forms.ChoiceField(choices=net_profite_type_choices)
    period = forms.IntegerField()
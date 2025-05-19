import re

from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[('0', 'False'), ('1', 'True')])
    delivery_city = forms.CharField(required=False)
    delivery_street_house = forms.CharField(required=False)
    delivery_apartment = forms.CharField(required=False)
    delivery_door = forms.CharField(required=False)
    delivery_floor = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[('0', 'False'), ('1', 'True')])
    payment_type = forms.ChoiceField(choices=[('0', 'Stripe',), ('1', 'Yookassa',)])

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if not data.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError('Неверный формат')
        return data
from django import forms

import re

class EstimateForm(forms.Form):
    CATERING_OR_DELIVERY = (
            ('none', 'Choose...'),
            ('catered', 'Catered'),
            ('delivery', 'Delivery'),
            )

    service_option = forms.ChoiceField(
            choices = CATERING_OR_DELIVERY
            )

    head_count = forms.IntegerField(
            min_value = 1
            )

    zip_code = forms.CharField(
            max_length = 10
            )

    def clean_service_option(self):
        data = self.cleaned_data['service_option']
        if data == 'none':
            raise forms.ValidationError('Choose catered or delivery.')
        return data

    def clean_zip_code(self):
        data = self.cleaned_data['zip_code']
        if not re.match("\d{5}(-\d{4})?", data):
            raise forms.ValidationError('Invalid zip code format.')
        return data

class WeeklySpecialForm(forms.Form):
    name = forms.CharField(
            max_length = 100,
            required = True
            )

    email_address = forms.EmailField(
            required = True
            )

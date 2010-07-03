from django import forms

class EstimateForm(forms.Form):
    CATERING_OR_DELIVERY = (
            (None, 'Catered or Delivery...'),
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

class WeeklySpecialForm(forms.Form):
    name = forms.CharField(
            max_length = 100,
            required = True
            )

    email_address = forms.EmailField(
            required = True
            )

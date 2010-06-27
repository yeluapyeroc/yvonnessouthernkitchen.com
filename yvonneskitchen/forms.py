from django import forms

class EstimateForm(forms.Form):
    CATERING_OR_DELIVERY = (
            ('catered', 'Catered'),
            ('delivery', 'Delivery'),
            )

    service_option = forms.ChoiceField(
            choices = CATERING_OR_DELIVERY
            )

    head_count = forms.IntegerField(
            min_value = 1
            )

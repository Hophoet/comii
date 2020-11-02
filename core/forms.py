from django import forms

COUNTRY_CHOICES = (
    ('T', 'Togo'),
    ('G', 'Ghana')
)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'234 lome-TOGO',
            'class':''
        }
    )
    )
    apartment_address = forms.CharField( widget=forms.TextInput(
        attrs={
            'placeholder':'2 Fevier chambre 409',
            'class':''
        }
        )
    )

    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    zip = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'zip',
            'class':''
        }
    ))

    same_billing_address = forms.BooleanField(required=False)

    save_info = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )
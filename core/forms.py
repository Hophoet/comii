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
            'class':'form-control'
        }
    )
    )
    apartment_address = forms.CharField( widget=forms.TextInput(
        attrs={
            'placeholder':'2 Fevier chambre 409',
            'class':'form-control'
        }
        )
    )

    # country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    country = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'your country',
            'class':'form-control',
        }
    ))
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'zip',
            'class':'form-control'
        }
    ))

    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Flooz number',
            'class':'form-control'
        }
    ))
    # same_billing_address = forms.BooleanField(required=False)

    # save_info = forms.BooleanField(required=False)

    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    # )


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Promo code',
        'class':'form-control',
        'aria-label':'Recipient\'s username',
        'aria-describedby':'basic-addon2',
    }))

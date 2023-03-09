from paypal.standard.forms import PayPalPaymentsForm
from django import forms
from django.utils.html import format_html

class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""
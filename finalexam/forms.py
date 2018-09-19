from django import forms


class AddForm(forms.Form):
    fname = forms.CharField(label='First Name:', max_length=100)
    lname = forms.CharField(label='Last Name:', max_length=100)
    contact = forms.CharField(label='Contact:', max_length=100)
    address = forms.CharField(label='Address:', max_length=100)

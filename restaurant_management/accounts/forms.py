from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control bg-transparent text-white border-gold',
        'placeholder': 'Phone Number'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control bg-transparent text-white border-gold',
        'placeholder': 'Email Address'
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'phone_number' and field != 'email':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control bg-transparent text-white border-gold',
                    'placeholder': field.replace('_', ' ').capitalize()
                })

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['address', 'city', 'postal_code']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control bg-transparent text-white border-gold', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control bg-transparent text-white border-gold'}),
        }

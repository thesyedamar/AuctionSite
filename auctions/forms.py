from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Bid, Profile
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    auction_end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=True, label='Auction End Date')
    auction_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), required=True, label='Auction End Time')
    auction_end_ampm = forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')], widget=forms.Select(attrs={'class': 'form-control'}), required=True, label='AM/PM')

    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'starting_bid', 'image', 'condition']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('auction_end_date')
        time = cleaned_data.get('auction_end_time')
        ampm = cleaned_data.get('auction_end_ampm')
        
        if date and time and ampm:
            try:
                # Handle 12-hour format conversion
                hour = time.hour
                if ampm == 'PM' and hour < 12:
                    hour += 12
                elif ampm == 'AM' and hour == 12:
                    hour = 0
                
                # Create the datetime
                from datetime import time as dt_time
                adjusted_time = dt_time(hour=hour, minute=time.minute)
                auction_end = timezone.make_aware(timezone.datetime.combine(date, adjusted_time))
                
                if auction_end <= timezone.now():
                    self.add_error('auction_end_date', 'Auction end time must be in the future.')
                else:
                    cleaned_data['auction_end'] = auction_end
            except Exception as e:
                self.add_error('auction_end_time', f'Invalid time format: {str(e)}')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        auction_end = self.cleaned_data.get('auction_end')
        if auction_end:
            instance.auction_end = auction_end
        if commit:
            instance.save()
        return instance

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'user_type', 'password1', 'password2')

class StoreSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['store_name', 'store_logo', 'store_description', 'store_email', 'store_phone', 'payment_settings']
        labels = {
            'store_logo': _('Store Logo'),
        }
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your store name')}),
            'store_logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': _('Upload your store logo')}),
            'store_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _("Describe your store and the items you'll be selling"), 'rows': 3}),
            'store_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your contact email')}),
            'store_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your contact number')}),
            'payment_settings': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Connect your payment account')}),
        } 
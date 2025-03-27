from django import forms
from .models import CustomUser, CustomerProfile, ShopProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Customer Registration Form
class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)
    email = forms.EmailField()
    # remember_me = forms.BooleanField(required=False, initial=False)  # Added Remember Me


    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'phone', 'address', 'email', 'password1', 'password2',]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.email = self.cleaned_data['email']
        user.user_type = 1  # Set user type to customer
        if commit:
            user.save()
            # Create the customer profile after saving the user
            CustomerProfile.objects.create(user=user, name=user.name, phone=user.phone, address=user.address)
        return user


# sutomer profile edit form 

class CustomerProfileForm(forms.ModelForm):
    # Add fields from CustomUser
    email = forms.EmailField()  # Example of a CustomUser field
    username = forms.CharField()  # Another example

    class Meta:
        model = CustomerProfile
        fields = ['name', 'phone', 'address', 'email', 'username']

    def __init__(self, *args, **kwargs):
        # Accept an instance of CustomUser if provided
        self.user_instance = kwargs.pop('user_instance', None)
        super(CustomerProfileForm, self).__init__(*args, **kwargs)

        if self.user_instance:
            # Populate form fields from CustomUser instance
            self.fields['email'].initial = self.user_instance.email
            self.fields['username'].initial = self.user_instance.username

    def save(self, *args, **kwargs):
        # Save CustomerProfile data
        profile_instance = super(CustomerProfileForm, self).save(*args, **kwargs)
        if self.user_instance:
            # Update and save CustomUser instance fields
            self.user_instance.email = self.cleaned_data['email']
            self.user_instance.username = self.cleaned_data['username']
            self.user_instance.save()
        return profile_instance

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


# Shop Owner Registration Form
class ShopOwnerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)
    email = forms.EmailField()
    owner_name = forms.CharField(max_length=255)
    shop_number = forms.CharField(max_length=20)
    location = forms.CharField(max_length=255)
    shop_proof = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = [
            'username', 'name', 'phone', 'address', 'email', 'password1', 'password2', 'owner_name', 'shop_number','location', 'shop_proof'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.email = self.cleaned_data['email']
        user.user_type = 2  # Set user type to shop owner
        if commit:
            user.save()
            # Create the shop profile after saving the user
            ShopProfile.objects.create(user=user,
                                       name=self.cleaned_data['name'],
                                       phone=self.cleaned_data['phone'],
                                       address=self.cleaned_data['address'],
                                       owner_name=self.cleaned_data['owner_name'],
                                       shop_number=self.cleaned_data['shop_number'],
                                       location=self.cleaned_data['location'],
                                       shop_proof=self.cleaned_data['shop_proof'])
        return user

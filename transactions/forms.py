from django import forms
from django.forms.widgets import DateInput

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime



class inward_Form(forms.ModelForm):
    class Meta:
        model = inward
        fields = '__all__'
        widgets = {
            'godown': forms.Select(attrs={
                'class': 'form-control', 'id': 'godown'
            }),
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'company_goods'
            }),
            'goods_company': forms.Select(attrs={
                'class': 'form-control', 'id': 'category'
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'bag_size'
            }),
           
           
            'bags': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bag_size'
            }),
            'DC_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'total_bag'
            }),

            'DC_date': DateInput(attrs={ 'class': 'form-control', 'type': 'date'}, format = '%Y-%m-%d'),
            
        }



class outward_Form(forms.ModelForm):
    class Meta:
        model = outward
        fields = '__all__'
        widgets = {
            'godown': forms.Select(attrs={
                'class': 'form-control', 'id': 'godown'
            }),
            'dealer': forms.Select(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'company_goods'
            }),
            'goods_company': forms.Select(attrs={
                'class': 'form-control', 'id': 'category'
            }),
            'gate_pass_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'gate_pass_name'
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'employee_name'
            }),
            'bags': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bag_size'
            }),
            'DC_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'total_bag'
            }),
            'name_of_buyer': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'total_bag'
            }),
            'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_bag'
            }),

            'DC_date': DateInput(attrs={ 'class': 'form-control', 'type': 'date'}, format = '%Y-%m-%d'),
            
        }




class goods_company_Form(forms.ModelForm):
    class Meta:
        model = stock
        fields = '__all__'
        widgets = {
         
            'company_goods': forms.Select(attrs={
                'class': 'form-control', 'id': 'company_goods'
            }),
           
            'goods_company_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'total_bag': forms.NumberInput(attrs={
                'class': 'form-control cal', 'id': 'total_bag'
            }),
           
            
        }

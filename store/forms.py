from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

        
class godown_Form(forms.ModelForm):
    class Meta:
        model = godown
        
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
        }


class company_goods_Form(forms.ModelForm):
    class Meta:
        model = company_goods
        fields = '__all__'
        widgets = {
            'godown': forms.Select(attrs={
                'class': 'form-control', 'id': 'godown'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
           
     
            
        }

class dealer_Form(forms.ModelForm):
    class Meta:
        model = dealer
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            
           
     
            
        }




class goods_company_Form(forms.ModelForm):
    class Meta:
        model = goods_company
        fields = '__all__'
        widgets = {
          
          
            'category': forms.Select(attrs={
                'class': 'form-control', 'id': 'categoryyy'
            }),
            'goods_company_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
           
            
        }



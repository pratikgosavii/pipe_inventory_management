import django_filters
from django_filters import DateFilter, CharFilter
from django.forms.widgets import DateInput
from django import forms

from .models import *
from .forms import *




class stock_filter(django_filters.FilterSet):

    company_goods = django_filters.ModelChoiceFilter(
        queryset=company_goods.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )
   
    goods_company = django_filters.ModelChoiceFilter(
        queryset=goods_company.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )
    total_bag = django_filters.NumberFilter(
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company'
            })
    )
    

    class Meta:
        model = stock
        fields = '__all__'
       
   

class outward_filter(django_filters.FilterSet):


    company_goods = django_filters.ModelChoiceFilter(
        queryset=company_goods.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'company_goods'
            })
    )
   
    goods_company = django_filters.ModelChoiceFilter(
        queryset=goods_company.objects.all(),
        widget=forms.Select(
            attrs={
                'class' : 'form-control',
                'id' : 'goods_company'
            })
    )
   
   
    DC_date_start__date = DateFilter(field_name="DC_date", lookup_expr='gte', widget=forms.DateInput(
            attrs={
                'id': 'datepicker1212',
                'type': 'date',
                'class' : 'form-control'
            }
        ))


    DC_date_end__date = DateFilter(field_name="DC_date", lookup_expr='lte', widget=forms.DateInput(
            attrs={
            'id': 'datepicker1212',
            'type': 'date',
                'class' : 'form-control'
            }
        ))
    

    class Meta:
        model = outward
        fields = '__all__'
       
   
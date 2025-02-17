from email import message
from genericpath import samefile
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd

from store.views import numOfDays
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date
from django.core.paginator import Paginator, EmptyPage
from functools import reduce

from django.urls import reverse
import csv
import mimetypes

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')




def demo(request):

    
    
    s = stock.objects.all()




    for ab in s:

        a = inward.objects.filter(company__company_name = ab.company.company_name, company_goods__name = ab.company_goods.name, goods_company__goods_company_name = ab.goods_company.goods_company_name)
        b = outward.objects.filter(company__company_name =  ab.company.company_name, company_goods__name = ab.company_goods.name, goods_company__goods_company_name = ab.goods_company.goods_company_name)

        x = 0
        y = 0
        z = 0

        for i in a:
            x = x + i.bags
            
        for i in b:
            y = y + i.bags

        for i in c:
            z = z + i.bags

        

        st = x - y + z


        ab.total_bag = st
        ab.save()




# Create your views here.

@login_required(login_url='login')
def add_inward(request):



    godown_id = request.session.get('gowdown')
     
    if godown_id == None:
        godown_instance = godown.objects.first()
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id

    else:

        godown_instance = godown.objects.get(id = godown_id)



    if request.method == 'POST':

        forms = inward_Form(request.POST)
        DC_date = request.POST.get('DC_date')


        if DC_date:

            date_time = DC_date
        else:
            date_time = datetime.now(IST)
        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = inward_Form(updated_request)

        if forms.is_valid():
            forms.save()

            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            e = forms.cleaned_data['bags']
            g = forms.cleaned_data['godown']

            try:
                test = stock.objects.get(godown = g, company_goods = b, goods_company = c)

                test.total_bag = test.total_bag + e
                test.save()

                return redirect('add_inward')


            except stock.DoesNotExist:

                test = stock.objects.create(godown = g, company_goods = b, goods_company = c, total_bag = e)
                godown_instance = godown.objects.get(id = godown_id)
                company_goods_data = company_goods.objects.filter(godown = godown_instance)

                context = {
                    'form': forms,
                    'godown_instance' : godown_instance,
                    'company_goods_data' : company_goods_data


                }
               
                return render(request, 'transactions/add_inward.html', context)


        else:

            godown_instance = godown.objects.get(id = godown_id)
            company_goods_data = company_goods.objects.filter(godown = godown_instance)

            context = {
                'form': forms,
                'godown_instance' : godown_instance,
                'company_goods_data' : company_goods_data

            }
            
            return render(request, 'transactions/add_inward.html', context)



    else:

        forms = inward_Form()

        godown_instance = godown.objects.get(id = godown_id)

        company_goods_data = company_goods.objects.filter(godown = godown_instance)
             
        context = {
            'form': forms,
            'godown_instance' : godown_instance,
            'company_goods_data' : company_goods_data

        }
        
        return render(request, 'transactions/add_inward.html', context)


@login_required(login_url='login')
def update_inward(request, inward_id ):


    if request.method == 'POST':

        instance_inward = inward.objects.get(id = inward_id)


        company_goods_id = request.POST.get('company_goods')
        goods_company_id = request.POST.get('goods_company')
        bags = request.POST.get('bags')

        DC_date = request.POST.get('DC_date')

        if DC_date:

            date_time = DC_date

        else:
            date_time = datetime.now(IST)


        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = inward_Form(updated_request, instance=instance_inward)


        if forms.is_valid():

            instance_inward = inward.objects.get(id = inward_id)

            if int(instance_inward.company_goods.id) != int(company_goods_id) or int(instance_inward.goods_company.id) != int(goods_company_id):

                try:

                    company_goods_instance = company_goods.objects.get(id = company_goods_id) 
                    goods_company_instance = goods_company.objects.get(id = goods_company_id) 

                    test = stock.objects.get(company_goods = company_goods_instance, goods_company = goods_company_instance)
                    test.total_bag = test.total_bag + int(bags)
                    test.save()

                except stock.DoesNotExist:
                    stock.objects.create(company_goods = company_goods_instance, goods_company = goods_company_instance, total_bag =  int(bags))


                company_goods_instance = company_goods.objects.get(id = instance_inward.company_goods.id)
                goods_company_instance = goods_company.objects.get(id = instance_inward.goods_company.id)

                stock_before = stock.objects.get(company_goods = company_goods_instance, goods_company = goods_company_instance)
                stock_before.total_bag = stock_before.total_bag - instance_inward.bags
                stock_before.save()

               
                    
               
                    
                forms.save()

                return HttpResponseRedirect(reverse('list_inward'))
            
            else:

                minus_stock = None

                if instance_inward.bags != int(bags):

                    test = stock.objects.get(company_goods = company_goods_id, goods_company = goods_company_id)

                    if instance_inward.bags > int(bags):
                        minus_stock = instance_inward.bags - int(bags)

                    else:
                        add_stock = int(bags) - instance_inward.bags

                    if minus_stock:

                        if test.total_bag >= minus_stock:

                            test.total_bag = test.total_bag - minus_stock
                            test.save()
                            forms.save()
                            return redirect('list_inward')

                        else:
                        
                            messages.error(request, "Outward is more than Stock")
                            return redirect('list_inward')

                    else:

                        test.total_bag = test.total_bag + add_stock
                        test.save()

                        forms.save()

                        return redirect('list_inward')

                else:

                    forms.save()
                    return HttpResponseRedirect(reverse('list_inward'))

        else:
        
            instance = inward.objects.get(id = inward_id)
            company_goods_id = forms.instance.company_goods.id
            category_id = forms.instance.goods_company.id
            print('company_goods_id')
            print(company_goods_id)
            context = {
                'form': forms,
                'company_goods_ID' : company_goods_id,
                'category_ID' : category_id,
            }
            

            return render(request, 'transactions/update_inward.html', context)

            

        

    else:

        instance = inward.objects.get(id = inward_id)
        forms = inward_Form(instance = instance)
        company_goods_id = forms.instance.company_goods.id
        category_id = forms.instance.goods_company.id
        print('company_goods_id')
        print(company_goods_id)
        context = {
            'form': forms,
            'company_goods_ID' : company_goods_id,
            'category_ID' : category_id,
        }
        return render(request, 'transactions/update_inward.html', context)


@login_required(login_url='login')
def delete_inward(request, inward_id):

    try:
        con = inward.objects.filter(id = inward_id).first()

        test = stock.objects.get(godown = con.godown, company_goods = con.company_goods, goods_company = con.goods_company)
        if test.total_bag >= con.bags:
            test.total_bag = test.total_bag - con.bags
            test.save()
            con.delete()

        else:

            messages.error(request, 'cant delete stock is less')

            return HttpResponseRedirect(reverse('list_inward_delete'))



        return HttpResponseRedirect(reverse('list_inward_delete'))


    except:
        return HttpResponseRedirect(reverse('list_inward_delete'))



def delete_selected_inward(request):
    
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')  # Get the list of selected outward IDs

        print(selected_items)
        
        try:
            for inward_id in selected_items:
                con = inward.objects.get(id=inward_id)
                test = stock.objects.get(godown=con.godown, company_goods=con.company_goods, goods_company=con.goods_company)
                
                # Adjust stock total before deleting inward
                test.total_bag = test.total_bag - con.bags
                test.save()
                
                # Delete the outward record
                con.delete()
            
            return redirect(reverse('list_inward_delete'))  # Redirect after successful deletion
        
        except Exception as e:
            return HttpResponse(f"Error occurred: {e}", status=400)
    
    return HttpResponse("Invalid request", status=400)


@login_required(login_url='login')
def list_inward(request):

    year = request.GET.get('year')
    godown_id = request.session['gowdown']

    if godown_id == None:
        godown_instance = godown.objects.first()
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id


    if year:

        date1 = str(int(year) - 1) + '-04-01'
        date2 = year + '-03-31'
    
        data = inward.objects.filter(DC_date__range=[date1, date2], godown__id = godown_id).order_by("-id")
    
    else:

        data = inward.objects.filter(godown__id = godown_id).order_by("-id")

    outward_filter_data = outward_filter(request.GET, queryset = data)
    
    data1 = []
    data2 = []


    data1.append('Godown')
    data1.append('Category')
    data1.append('Size')
    data1.append('DC number')
    data1.append('Quantity')
    data1.append('Date')
    data2.append(data1)


    if outward_filter_data.qs:

        for i in outward_filter_data.qs:

            data1 = []

            data1.append(i.godown.name)
            data1.append(i.company_goods.name)
            data1.append(i.goods_company.goods_company_name)
            data1.append(i.DC_number)
            data1.append(i.bags)
            data1.append(i.DC_date) 

            data2.append(data1)


            data1 = []



    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 50)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    company_goods_data = company_goods.objects.filter(godown__id = godown_id)

    context = {
        'data': outward_filter_data.qs,
        'year' : year,
        'company_goods_data' : company_goods_data,
        'outward_filter' : outward_filter(),
        'link' : link,
        
    }

    return render(request, 'transactions/list_inward.html', context)


import json

@login_required(login_url='login')
def add_outward(request):
    godown_id = request.session.get('gowdown')

    if godown_id is None:
        godown_instance = godown.objects.first()
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id
    else:
        godown_instance = godown.objects.get(id=godown_id)

    if request.method == 'POST':
        forms = outward_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        if DC_date:
            date_time = DC_date
        else:
            date_time = datetime.now(IST)

        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = outward_Form(updated_request)

        if forms.is_valid():
            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            e = forms.cleaned_data['bags']
            g = forms.cleaned_data['godown']

            try:
                test = stock.objects.get(godown=g, company_goods=b, goods_company=c)

                if test.total_bag >= e:
                    test.total_bag -= e
                    test.save()
                    forms.save()
                    return JsonResponse({'status': 'Success'})
                else:
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Outward is more than stock'
                    })

            except stock.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'No stock in inventory'
                })

        else:
            # Capture and return form errors
            form_errors = forms.errors.as_json()
            return JsonResponse({
                'status': 'error', 
                'message': 'Form validation failed',
                'errors': form_errors
            })

    

    else:

        forms = outward_Form()

        godown_instance = godown.objects.get(id = godown_id)
        company_goods_data = company_goods.objects.filter(godown = godown_instance)


        context = {
            'form': forms,
            'godown_instance': godown_instance,
            'company_goods_data': company_goods_data

        }
        return render(request, 'transactions/add_outward.html', context)


@login_required(login_url='login')
def report_dashbord(request):

    inward_filter_data = inward_filter()
    outward_filter_data = outward_filter()



    context = {
            'filter_inward': inward_filter_data,
            'filter_outward': outward_filter_data,
        }

    return render(request, 'transactions/report_dashbord.html', context)



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='login')
def list_outward(request):


    year = request.GET.get('year')
    godown_id = request.session['gowdown']

    if godown_id == None:
        godown_instance = godown.objects.first()
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id


    if year:

        date1 = str(int(year) - 1) + '-04-01'
        date2 = year + '-03-31'

        data = outward.objects.filter(DC_date__range=[date1, date2], godown__id = godown_id).order_by("-id")
    
    else:

        data = outward.objects.filter(godown__id = godown_id).order_by('-id')


    outward_filter_data = outward_filter(request.GET, queryset = data)
    
    data1 = []
    data2 = []


    data1.append('Godown')
    data1.append('Category')
    data1.append('Size')
    data1.append('Dealer')
    data1.append('DC number')
    data1.append('Quantity')
    data1.append('Employee name')
    data1.append('Buyer name')
    data1.append('Date')
    data2.append(data1)


    if outward_filter_data.qs:

        for i in outward_filter_data.qs:

            data1 = []

            data1.append(i.godown.name)
            data1.append(i.company_goods.name)
            data1.append(i.goods_company.goods_company_name)
            data1.append(i.dealer)
            data1.append(i.DC_number)
            data1.append(i.bags)
            data1.append(i.employee_name) 
            data1.append(i.gate_pass_name) 
            data1.append(i.DC_date) 

            data2.append(data1)


            data1 = []



    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    agent_name = request.GET.get('agent_name')

    if agent_name:

        data = data.filter(agent__name__icontains=agent_name)

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 50)
    company_goods_data = company_goods.objects.filter(godown__id = godown_id)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        'data': outward_filter_data.qs,
        'year' : year,
        'link' : link,
        'company_goods_data' : company_goods_data,
        'outward_filter' : outward_filter


    }

    return render(request, 'transactions/list_outward.html', context)

@login_required(login_url='login')
def update_outward(request, outward_id):


    if request.method == 'POST':

        instance = outward.objects.get(id = outward_id)
      
        
        company_goods_id = request.POST.get('company_goods')
        goods_company_id = request.POST.get('goods_company')

        company_goods_instance = company_goods.objects.get(id = company_goods_id) 
        goods_company_instance = goods_company.objects.get(id = goods_company_id) 

        bags = request.POST.get('bags')

        DC_date = request.POST.get('DC_date')

        print(DC_date)

        

        if DC_date:

            date_time = DC_date

        else:
            date_time = datetime.now(IST)


        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = outward_Form(updated_request, instance=instance)

        if forms.is_valid():

            instance = outward.objects.get(id = outward_id)

            try:
                
                if int(instance.company_goods.id) != int(company_goods_id) or int(instance.goods_company.id) != int(goods_company_id):


                    
                    try:
                      
                        test = stock.objects.get(company_goods = company_goods_instance, goods_company = goods_company_instance)
                      

                    except stock.DoesNotExist:
                        test = None
                        stock.objects.create(company_goods = company_goods_instance, goods_company = goods_company_instance, total_bag =  int(bags))


                    if test.total_bag >= int(bags):
                        
                        test.total_bag = test.total_bag - int(bags)
                        test.save()

                        stock_before = stock.objects.get(company_goods = instance.company_goods.id, goods_company = instance.goods_company.id)
                        
                        stock_before.total_bag = stock_before.total_bag + instance.bags
                        stock_before.save()
                        forms.save()

                     
                        return redirect('list_outward')

                    else:
                        messages.error(request, "Outward is more than Stock")
                        return redirect('list_outward')
                    
                else:

                    if instance.bags != int(bags):
                        
                        test = stock.objects.get(company_goods = company_goods_instance, goods_company = goods_company_instance)
                        
                        add_stock = None
                        minus_stock = None

                        if instance.bags > int(bags):
                            add_stock = instance.bags - int(bags)
                        else:
                            minus_stock = int(bags) - instance.bags

                        if minus_stock:

                            if test.total_bag >= minus_stock:

                                test.total_bag = test.total_bag - minus_stock
                                test.save()

                                forms.save()
                            else:

                                messages.error(request, "Outward is more than Stock")
                                return redirect('list_outward')

                        
                        else:

                            test.total_bag = test.total_bag + add_stock
                            test.save()

                            forms.save()

                        return redirect('list_outward')

                    else:
                        forms.save()
                        return HttpResponseRedirect(reverse('list_outward'))

                    

            except stock.DoesNotExist:

                messages.error(request, 'no stock in inventory for outward')
                return redirect('list_outward')

           

        else:
           
            comapny_goods_ID = forms.instance.company_goods.id
            category_id = forms.instance.goods_company.id
          
            context = {
                'form':  forms,
                'comapny_goods_ID' : comapny_goods_ID,
                'category_ID' : category_id,
            }

            return render(request, 'transactions/update_outward.html', context)



    else:

        instance = outward.objects.get(id = outward_id)
        forms = outward_Form(instance = instance)
        comapny_goods_ID = forms.instance.company_goods.id
        category_id = forms.instance.goods_company.id
          
        context = {
            'form':  forms,
            'comapny_goods_ID' : comapny_goods_ID,
            'category_ID' : category_id,
        }

        return render(request, 'transactions/update_outward.html', context)


@login_required(login_url='login')
def delete_outward(request, outward_id):

    a = stock.objects.all()

    try:
        con = outward.objects.get(id = outward_id)

        test = stock.objects.get(godown = con.godown, company_goods = con.company_goods, goods_company = con.goods_company)
        test.total_bag = test.total_bag + con.bags
        test.save()
        con.delete()

        return HttpResponseRedirect(reverse('list_outward_delete'))


    except Exception as e:
        return HttpResponseRedirect(reverse('list_outward_delete'))

@login_required(login_url='login')
def delete_selected_outward(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')  # Get the list of selected outward IDs
        
        try:
            for outward_id in selected_items:
                con = outward.objects.get(id=outward_id)
                test = stock.objects.get(godown=con.godown, company_goods=con.company_goods, goods_company=con.goods_company)
                
                # Adjust stock total before deleting outward
                test.total_bag = test.total_bag + con.bags
                test.save()
                
                # Delete the outward record
                con.delete()
            
            return redirect(reverse('list_outward_delete'))  # Redirect after successful deletion
        
        except Exception as e:
            return HttpResponse(f"Error occurred: {e}", status=400)
    
    return HttpResponse("Invalid request", status=400)


from .filters import *

@login_required(login_url='login')
def list_stock(request):

    godown_id = request.session.get('gowdown')
     
    if godown_id == None:
        godown_instance = godown.objects.first()
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id



    data = stock.objects.filter(godown__id = godown_id)
    stock_filter_data = stock_filter(request.GET, queryset = data)


    company_goods_data = company_goods.objects.filter(godown__id = godown_id)

    context = {
        'data': stock_filter_data.qs,
        'stock_filter_data' : stock_filter_data,
        'company_goods_data' : company_goods_data
    }

    return render(request, 'transactions/list_stock.html', context)


@login_required(login_url='login')
def add_return(request):


    if request.method == 'POST':

        forms = supply_return_Form(request.POST)
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)

        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)


        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = supply_return_Form(updated_request)

        print(DC_date)

        if forms.is_valid():

            forms.save()

            a = forms.cleaned_data['company']
            b = forms.cleaned_data['company_goods']
            c = forms.cleaned_data['goods_company']
            d = forms.cleaned_data['agent']
            e = forms.cleaned_data['bags']

            try:

                test = stock.objects.get(company = a, company_goods = b, goods_company = c)

                test.total_bag = test.total_bag + e
                test.save()

                return JsonResponse({'status' : 'done'}, safe=False)


            except stock.DoesNotExist:

                test = stock.objects.create(company = a, company_goods = b, goods_company = c, total_bag = e)
                return JsonResponse({'status' : 'done'}, safe=False)


        else:
            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)


    else:

        forms = supply_return_Form()

        context = {
            'form': forms
        }
        return render(request, 'transactions/add_return.html', context)



@login_required(login_url='login')
def list_return(request):

    year = request.GET.get('year')

    if year:

        date1 = str(int(year) - 1) + '-04-01'
        date2 = year + '-03-31'

        data = inward.objects.filter(DC_date__range=[date1, date2])
    
    else:

        data = supply_return.objects.all().order_by("DC_date")

    supply_return_filter_data = supply_return_filter()

    # inward_filter_data = inward_filter()

    print(data)

    agent_name = request.GET.get('agent_name')

    if agent_name:

        data = data.filter(agent__name__icontains=agent_name)



    page = request.GET.get('page', 1)
    paginator = Paginator(data, 50)

    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)



    company_data = company.objects.all()

    context = {
        'data': data,
        'company_data': company_data,
        'filter_return_supply' : supply_return_filter_data,
        'year' : year

    }

    return render(request, 'transactions/list_return.html', context)


@login_required(login_url='login')
def update_return(request, return_id):

    if request.method == 'POST':

        instance = supply_return.objects.get(id = return_id)

        company = request.POST.get('company')
        company_goods = request.POST.get('company_goods')
        goods_company = request.POST.get('goods_company')
        bags = request.POST.get('bags')
        
        DC_date = request.POST.get('DC_date')

        date_time = numOfDays(DC_date)

        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)


        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = supply_return_Form(updated_request, instance=instance)

        if forms.is_valid():

            instance = supply_return.objects.get(id = return_id)


            try:

                test = stock.objects.get(company = company, company_goods = company_goods, goods_company = goods_company)

                if int(instance.company.id) != int(company) or int(instance.company_goods.id) != int(company_goods) or int(instance.goods_company.id) != int(goods_company):
                
                    
                    test = stock.objects.get(company = company, company_goods = company_goods, goods_company = goods_company)
                    test.total_bag = test.total_bag - int(bags)
                    test.save()
                    stock_before = stock.objects.get(company = instance.company.id, company_goods = instance.company_goods.id, goods_company = instance.goods_company.id)
                    stock_before.total_bag = stock_before.total_bag + instance.bags
                    stock_before.save()

                    forms.save()

                    return redirect('list_return')

                 
                else:


                    if instance.bags != int(bags):
                        
                        test = stock.objects.get(company = company, company_goods = company_goods, goods_company = goods_company)

                        if instance.bags > int(bags):
                            minus_stock = instance.bags - int(bags)
                        else:
                            add_stock = int(bags) - instance.bags
                            minus_stock = None

                        if minus_stock:

                            if test.total_bag >= minus_stock:

                                test.total_bag = test.total_bag - minus_stock
                                test.save()
                                forms.save()

                                return redirect('list_return')

                            else:
                                
                                messages.error(request, "Outward is more than Stock")
                                return redirect('list_return')

                    
                        else:

                            test.total_bag = test.total_bag + add_stock
                            test.save()
                            forms.save()

                            return redirect('list_return')


                    else:
                        forms.save()
                        return HttpResponseRedirect(reverse('list_return'))

            except stock.DoesNotExist:

                messages.error(request, 'no stock in inventory for outward')
                return redirect('list_return')


        else:

            print(forms.errors)

    else:

        instance = supply_return.objects.get(id = return_id)
        forms = supply_return_Form(instance = instance)
        comapnyID = forms.instance.company.id
        comapny_goods_ID = forms.instance.company_goods.id
        goods_company_ID = forms.instance.goods_company.id
        agent_ID = forms.instance.agent.id

        context = {
            'form': forms,
            'comapnyID' : comapnyID,
            'comapny_goods_ID' : comapny_goods_ID,
            'goods_company_ID' : goods_company_ID,
            'agent_ID' : agent_ID       
        }
        return render(request, 'transactions/update_return.html', context)


@login_required(login_url='login')
def delete_return(request, return_id):

    try:
        con = supply_return.objects.get(id = return_id)
        test = stock.objects.get(company = con.company, company_goods = con.company_goods, goods_company = con.goods_company)
        if test.total_bag >= con.bags:
            test.total_bag = test.total_bag - con.bags
            test.save()
            con.delete()
        else:

            messages.error(request, 'cant delete stock is less')
            return HttpResponseRedirect(reverse('list_return'))


        return HttpResponseRedirect(reverse('list_return'))


    except:
        return HttpResponseRedirect(reverse('list_return'))
 
        


@login_required(login_url='login')
def report_inward(request):

    counteer = 1


    data = inward.objects.all().order_by("DC_number")

    filterd_data = inward_filter(request.GET, data)
    filtered_data = filterd_data.qs



    vals = []

    filterd_data = inward_filter(request.GET, data)
    filtered_data = filterd_data.qs
    # print(out)


    
    filtered_data = list(filtered_data.values_list('DC_number', 'company', 'company_goods__name', 'goods_company__goods_company_name', 'bags', 'DC_date'))

    vals1 = []
    vals1.append('Serial')
    vals1.append("DC Number")
    vals1.append("Company")
    vals1.append("Category")
    vals1.append("Size")
    vals1.append('Quantity')
    vals1.append('Date')

    vals.append(vals1)


    for i in filtered_data:
        vals1 = []
        vals1.append(counteer)
        counteer = counteer + 1
        vals1.append(i[0])
        vals1.append(i[1])
        vals1.append(i[2])
        vals1.append(i[3])
        vals1.append(i[4])
        vals1.append(i[5])

        vals.append(vals1)



       

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)


    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = vals
    vals_list.pop(0)


    print(vals_list)

    context = {
        'data': vals_list,
        'link' : link


    }

    return render(request, 'report/inward_report.html', context)



@login_required(login_url='login')
def report_outward(request):


    counteer = 1

   

    vals = []

    outward_data = outward.objects.all().order_by("DC_number")
    outward_filterd_data = outward_filter(request.GET, outward_data)
    outward_filterd_data = outward_filterd_data.qs

    outward_filterd_data = list(outward_filterd_data.values_list('DC_number', 'company', 'company_goods__name', 'goods_company__goods_company_name', 'dealer__bane', 'bags', 'DC_date'))
    # print(out)

    outward_filterd_data = list(map(list, outward_filterd_data))


    vals1 = []
    vals1.append('Serial')
    vals1.append("DC Number")
    vals1.append("Company")
    vals1.append("Category")
    vals1.append("Size")
    vals1.append("Dealer")
    vals1.append('Quantity')
    vals1.append('Date')
    vals.append(vals1)


    for i in outward_filterd_data:
        vals1 = []
        vals1.append(counteer)
        counteer = counteer + 1
        vals1.append(i[0])
        vals1.append(i[1])
        vals1.append(i[2])
        vals1.append(i[3])
        vals1.append(i[4])
        vals1.append(i[5])
        vals1.append(i[6])
        vals.append(vals1)

   

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    print(vals)


    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = vals
    vals_list.pop(0)


    context = {
        'data': vals_list,
        'link' : link


    }

    return render(request, 'report/outward_report.html', context)




@login_required(login_url='login')
def report_supply_return(request):

    data = supply_return.objects.all().order_by("DC_number")

    filterd_data = supply_return_filter(request.GET, data)
    data = filterd_data.qs

    vals = []


    filtered_data = list(data.values_list('DC_number', 'agent__name', 'agent__place', 'agent__taluka', 'agent__district', 'company_goods__name', 'goods_company__goods_company_name', 'bags', 'DC_date', 'transport__name', 'LR_number', 'freight'))


    vals1 = []
    vals1.append('Serial')
    vals1.append("DC Number")
    vals1.append("Party Name")
    vals1.append("Party Place")
    vals1.append("Party Taluka")
    vals1.append("Party District")
    vals1.append("Crop")
    vals1.append("Variety")
    vals1.append('Packet')
    vals1.append('Date')
    vals1.append('Transport')
    vals1.append('LR Number')
    vals1.append('Freight')
    vals.append(vals1)

    counteer = 1

    
    for i in filtered_data:
        vals1 = []
        vals1.append(counteer)
        counteer = counteer + 1
        vals1.append(i[0])
        vals1.append(i[1])
        vals1.append(i[2])
        vals1.append(i[3])
        vals1.append(i[4])
        vals1.append(i[5])
        vals1.append(i[6])
        vals1.append(i[7])
        vals1.append(i[8])
        vals1.append(i[9])
        vals1.append(i[10])
        vals1.append(i[11])
        vals.append(vals1)


    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')


    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = vals
    vals_list.pop(0)


    context = {
        'data': vals_list,
        'link' : link,

    }

    return render(request, 'report/outward_report.html', context)


@login_required(login_url='login')
def generate_report_stock(request):

    godown_id = request.session.get('gowdown')
     
    if godown_id == None:
        godown_instance = godown.objects.first()
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id


    data_stock = stock.objects.filter(godown__id = godown_id).order_by('updated_at')

    stock_filter_data = stock_filter(request.GET, queryset = data_stock)
    
    data1 = []
    data2 = []


    data1.append('Godown')
    data1.append('Category')
    data1.append('Size')
    data1.append('Quantity')
    data2.append(data1)


    if stock_filter_data.qs:

        for i in stock_filter_data.qs:

            data1 = []

            data1.append(i.godown)
            data1.append(i.company_goods)
            data1.append(i.goods_company)
            data1.append(i.total_bag)

            data2.append(data1)

            data1 = []



    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data2)

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name
    company_goods_data = company_goods.objects.filter(godown__id = godown_id)

    context = {
        'data': stock_filter_data.qs,
        'stock_filter_data' : stock_filter_data,
        'company_goods_data' : company_goods_data,
        'link' : link
    }

    return render(request, 'report/stock_report.html', context)


@login_required(login_url='login')
def generate_report_main(request):

    company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
    company_data = dict(company_data.values)

    company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
    company_goods_data = dict(company_goods_data.values)

    goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
    goods_company_data = dict(goods_company_data.values)

    agent_data = pd.DataFrame(list(agent.objects.all().values('id', 'name')))
    agent_data = dict(agent_data.values)
    
    agent_data2 = pd.DataFrame(list(agent.objects.all().values('id', 'name', 'place', 'taluka', 'district')))

    # return_data = supply_return.objects.all()

    outward_data = outward.objects.all()
    supply_return_data = supply_return.objects.all()
    outward_filterd_data = outward_filter(request.GET, outward_data)
    supply_return_filterd_data = outward_filter(request.GET, supply_return_data)

    if outward_data and not supply_return_data:
        
        # outward sum
        df2 = pd.DataFrame(list(outward_filterd_data.qs.values()))
        sum__ = df2.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

        sum__['bags_x'] = sum__['bags']
        sum__['bags_y'] = None
        sum__['bags_z'] = sum__['bags']
        sum__['company_id'] = sum__['company_id'].map(company_data)
        sum__['company_goods_id'] = sum__['company_goods_id'].map(company_goods_data)
        sum__['goods_company_id'] = sum__['goods_company_id'].map(goods_company_data)
        sum__['agent_id'] = sum__['agent_id'].map(agent_data)
        

        out = (sum__.merge(agent_data2, left_on='agent_id', right_on='name').reindex(columns=['agent_id', 'place', 'taluka', 'district', 'company_id', 'company_goods_id', 'goods_company_id', 'bags_x', 'bags_y', 'bags_z']))



    elif supply_return_data and not outward_data:
        #return sum
        df3 = pd.DataFrame(list(supply_return_filterd_data.qs.values()))

        sum__2 = df3.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()

        sum__2['bags_x'] = None
        sum__2['bags_y'] = sum__2['bags']
        sum__2['bags_z'] = sum__2['bags']
        sum__2['company_id'] = sum__2['company_id'].map(company_data)
        sum__2['company_goods_id'] = sum__2['company_goods_id'].map(company_goods_data)
        sum__2['goods_company_id'] = sum__2['goods_company_id'].map(goods_company_data)
        sum__2['agent_id'] = sum__2['agent_id'].map(agent_data)
        

        out = (sum__2.merge(agent_data2, left_on='agent_id', right_on='name').reindex(columns=['agent_id', 'place', 'taluka', 'district', 'company_id', 'company_goods_id', 'goods_company_id', 'bags_x', 'bags_y', 'bags_z']))




    else:

        df2 = pd.DataFrame(list(outward_filterd_data.qs.values()))

        df3 = pd.DataFrame(list(supply_return_filterd_data.qs.values()))


        sum__ = df2.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()
        sum__2 = df3.groupby(['company_id', 'company_goods_id', 'goods_company_id', 'agent_id']).sum().reset_index()


        final_ou = pd.merge(sum__, sum__2, on=['company_id', 'company_goods_id', 'goods_company_id', 'agent_id'], how="outer")[['company_id', 'company_goods_id', 'goods_company_id', 'agent_id', 'bags_x', 'bags_y']]
        final_ou['bags_z'] = final_ou.fillna(0)['bags_x'] - final_ou.fillna(0)['bags_y']

        
        final_ou['company_id'] = final_ou['company_id'].map(company_data)
        final_ou['company_goods_id'] = final_ou['company_goods_id'].map(company_goods_data)
        final_ou['goods_company_id'] = final_ou['goods_company_id'].map(goods_company_data)
        final_ou['agent_id'] = final_ou['agent_id'].map(agent_data)

        out = (final_ou.merge(agent_data2, left_on='agent_id', right_on='name').reindex(columns=['company_id', 'agent_id', 'place', 'taluka', 'district', 'company_goods_id', 'goods_company_id', 'bags_x', 'bags_y', 'bags_z']))

        print(out)

        # print(out)

    vals = out.values

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')
        


    
    vals_list = (vals.tolist())
    vals1 = []
    vals1.append("Party Name")
    vals1.append("Party Place")
    vals1.append("Party Taluka")
    vals1.append("Party District")
    vals1.append("Company")
    vals1.append("Crop")
    vals1.append("Variety")
    vals1.append('Supply Packet')
    vals1.append('Return Packet')
    vals1.append('Net Packet')

    vals_list.insert(0, vals1)

    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')


    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals_list)


    link = os.path.join(BASE_DIR) + '\static\csv\\' + name


    outward_filter_data = outward_filter()

    vals_list = (vals.tolist())

    company_data = company.objects.all()

    context = {
        'data' : vals_list,
        'filter_outward' : outward_filter_data,
        'link' : link,
        'company_data' : company_data

    }

    return render(request, 'report/main_report.html', context)
    

@login_required(login_url='login')
def generate_report_daily(request):

    pd.set_option('display.float_format', '{:.2f}'.format)

    #DC_date_start__date=2022-02-28&DC_date_end__date=2022-02-28

    company_data = pd.DataFrame(list(company.objects.all().values('id', 'company_name')))
    company_data = dict(company_data.values)

    company_goods_data = pd.DataFrame(list(company_goods.objects.all().values('id', 'name')))
    company_goods_data = dict(company_goods_data.values)

    goods_company_data = pd.DataFrame(list(goods_company.objects.all().values('id', 'goods_company_name')))
    goods_company_data = dict(goods_company_data.values)

    inward_data = inward.objects.filter(DC_date = datetime.now())
    outward_data = outward.objects.filter(DC_date = datetime.now())
    supply_return_data = outward.objects.filter(DC_date = datetime.now())
    inward_filterd_data = inward_filter(request.GET, inward_data)
    outward_data_filterd_data = outward_filter(request.GET, outward_data)
    if inward_data:
        # inward sum
        df = pd.DataFrame(list(inward_filterd_data.qs.values()))
        sum__ = df.groupby(['company_id', 'company_goods_id', 'goods_company_id']).sum().reset_index()
    else:
        sum__ = pd.DataFrame(columns=['company_id', 'company_goods_id', 'goods_company_id', 'id', 'agent_id', 'bags', 'DC_number'])

    if outward_data:
        # outward sum
        df2 = pd.DataFrame(list(outward_data_filterd_data.qs.values()))
        sum__2 = df2.groupby(['company_id', 'company_goods_id', 'goods_company_id']).sum().reset_index()
        
    else:
        sum__2 = pd.DataFrame(columns=['company_id', 'company_goods_id', 'goods_company_id', 'id', 'agent_id', 'bags', 'DC_number'])

    if supply_return_data:
        
        #return sum
        df3 = pd.DataFrame(list(supply_return_data.values()))
        sum__3 = df3.groupby(['company_id', 'company_goods_id', 'goods_company_id']).sum().reset_index()

    else:
        sum__3 = pd.DataFrame(columns=['company_id', 'company_goods_id', 'goods_company_id', 'id', 'agent_id', 'bags', 'DC_number'])

    #stock
    sum__4 = pd.DataFrame(list(stock.objects.all().values()))

    data_frames = [sum__, sum__2, sum__3, sum__4]

    ada = reduce(lambda  left,right: pd.merge(left,right,on=['company_id', 'company_goods_id', 'goods_company_id'], how='outer'), data_frames)[['company_id', 'company_goods_id', 'goods_company_id', 'bags_x', 'bags_y', 'bags', 'total_bag']]
    print('final')

   

    # m = pd.merge(sum__, sum__2, on=['company_id', 'company_goods_id', 'goods_company_id'], how="outer")[['company_id', 'company_goods_id', 'goods_company_id',  'bags_x', 'bags_y']]
    
    # print('m')
    # print(m)
    # m1 = pd.merge(m, sum__3, on=['company_id', 'company_goods_id', 'goods_company_id'], how="outer")[['company_id', 'company_goods_id', 'goods_company_id',  'bags_x', 'bags_y', 'bags']]
   
    # print('m1')
    # print(m1)
    # m2 = pd.merge(m1, sum__4, on=['company_id', 'company_goods_id', 'goods_company_id'], how="outer")[['company_id', 'company_goods_id', 'goods_company_id',  'bags_x', 'bags_y', 'bags', 'total_bag']]

    # print('m2')
    # print(m2)

    final_out = ada

    final_out['company_id'] = final_out['company_id'].map(company_data)
    final_out['company_goods_id'] = final_out['company_goods_id'].map(company_goods_data)
    final_out['goods_company_id'] = final_out['goods_company_id'].map(goods_company_data)

    vals = final_out.values
    
    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')

    name = "Report.csv"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    with open(path,  'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vals)

    outward_filter_data = outward_filter()

    link = os.path.join(BASE_DIR) + '\static\csv\\' + name

    vals_list = (vals.tolist())


    context = {
        'data': vals_list,
        'filter_outward' : outward_filter_data,
        'link' : link

    }

    return render(request, 'report/daily_report.html', context)




@login_required(login_url='login')
def download(request):
    # fill these variables with real values


    if request.method == 'POST':

        fl_path =  request.POST.get('link')



        if os.path.exists(fl_path):

            with open(fl_path, 'r' ) as fh:
                mime_type  = mimetypes.guess_type(fl_path)
                print('--------------------')
                print(mime_type)
                response = HttpResponse(fh.read(), content_type=mime_type)
                response['Content-Disposition'] = 'attachment;filename=' + str(fl_path)

                return response



        else:
            messages.error(request, 'path does not exist')


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

       return 'abc'

@login_required(login_url='login')
def delete_dashboard(request):

    return render(request, 'delete/dashbaord.html')


# delete view


def list_inward_delete(request):

    data = inward.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 50)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        'data': data,
    }


    return render(request, 'delete/list_inward_delete.html', context)


def list_outward_delete(request):

    data = outward.objects.all()


    page = request.GET.get('page', 1)
    paginator = Paginator(data, 50)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        'data': data,
    }

    return render(request, 'delete/list_outward_delete.html', context)



def list_return_delete(request):

    data = supply_return.objects.all()

    # inward_filter_data = inward_filter()

    print(data)

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'delete/list_return_delete.html', context)






from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pdf_status = pisa.CreatePDF(html, dest=response)

    if pdf_status.err:
        return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')

    return response


def ResultList(request, outward_id):
    template_name = "transactions/gate_pass.html"
    records = outward.objects.get(id = outward_id)

    return render_to_pdf(
        template_name,
        {
            "record": records,
        },
    )
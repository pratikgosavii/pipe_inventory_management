from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *


from store.models import *


@login_required(login_url='login')
def dashboard(request):


    godown_id = request.GET.get('godown_id')
    godown_instance = godown.objects.first()

    session_godown = request.session["gowdown"]

    if godown_id:
        print('--------------------------------')
        request.session["gowdown"] = godown_id
        godown_id = request.session["gowdown"] 

        print(godown_id)

        godown_instance = godown.objects.get(id = godown_id)
    elif session_godown != None:
        godown_instance = godown.objects.get(id = session_godown)
        
    else:
        godown_id = godown_instance.id
        request.session["gowdown"] = godown_id

    godown_data = godown.objects.all()
    godiwn_count = godown_data.count()
    stock_count = stock.objects.all().count()

    context = {
        'godown' : godiwn_count,
        'godown_instance' : godown_instance,
        'godown_data' : godown_data,
        'stock' : stock_count
    }
    
    return render(request, 'dashboard.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *


from store.models import *


@login_required(login_url='login')
def dashboard(request):

    godiwn_count = godown.objects.all().count()
    stock_count = stock.objects.all().count()

    context = {
        'godown' : godiwn_count,
        'stock' : stock_count
    }
    
    return render(request, 'dashboard.html', context)

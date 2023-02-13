from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *


from store.models import *


@login_required(login_url='login')
def dashboard(request):
    
    return render(request, 'dashboard.html')

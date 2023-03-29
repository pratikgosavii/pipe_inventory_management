from django.db import models

from users.models import User
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')






class godown(models.Model):

    name = models.CharField(max_length=120, unique=False)
    
    
    def __str__(self):
        return self.name


class company_goods(models.Model):

    godown = models.ForeignKey(godown, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False)
    
    
    def __str__(self):
        return self.name


class goods_company(models.Model):
    
    category = models.ForeignKey(company_goods, on_delete=models.CASCADE)
    goods_company_name = models.CharField(max_length=120, unique=False)

    def __str__(self):
        return self.goods_company_name



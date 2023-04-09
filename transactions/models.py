from django.db import models

# Create your models here.



from users.models import User
from datetime import datetime, timezone
from store.models import *



class inward(models.Model):

    godown = models.ForeignKey(godown , on_delete=models.CASCADE, related_name='sdwe')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='wfgv')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='xvc')
    employee_name = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.CharField(max_length=50)
    DC_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.godown.name

   

class outward(models.Model):

    godown = models.ForeignKey(godown , on_delete=models.CASCADE, related_name='fgv')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='cvg')
    employee_name = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.CharField(max_length=50)
    mobile_no = models.IntegerField( null = True, blank = True)
    DC_date = models.DateField(auto_now_add=False)


    gate_pass_no = models.BigIntegerField(default=1111, null = True, blank = True)
    gate_pass_name = models.CharField(max_length=100, null = True, blank = True)

    



class stock(models.Model):

    godown = models.ForeignKey(godown , on_delete=models.CASCADE, related_name='sfwwfddfds')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fsdsdd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='csdsvg')
    total_bag = models.BigIntegerField()
    

    



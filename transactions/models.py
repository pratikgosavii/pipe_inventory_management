from django.db import models

# Create your models here.



from users.models import User
from datetime import datetime, timezone
from store.models import *



class inward(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='sdwe')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='wfgv')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='xvc')
    agent = models.ForeignKey(agent , on_delete=models.CASCADE, related_name='sdv', null = True, blank = True)
    transport = models.ForeignKey(transport , on_delete=models.CASCADE, related_name='sdsxc', null=True, blank=True)
    LR_number = models.CharField(max_length=50, null = True, blank = True)
    freight = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.BigIntegerField()
    bill_no = models.BigIntegerField()
    DC_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.company.company_name

   

class outward(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='fgv')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='cvg')
    agent = models.ForeignKey(agent , on_delete=models.CASCADE, related_name='df', null = True, blank = True)
    transport = models.ForeignKey(transport , on_delete=models.CASCADE, related_name='ddssszc', null=True, blank=True)
    LR_number = models.CharField(max_length=50, null = True, blank = True)
    freight = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.BigIntegerField()
    bill_no = models.BigIntegerField()
    DC_date = models.DateTimeField(auto_now_add=False)

    


class supply_return(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='we')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='tr')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='wegvge')
    agent = models.ForeignKey(agent , on_delete=models.CASCADE, related_name='fgrrt')
    transport = models.ForeignKey(transport , on_delete=models.CASCADE, related_name='scxsesdf', null=True, blank=True)
    LR_number = models.CharField(max_length=50, null = True, blank = True)
    freight = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.CharField(max_length=566)
    DC_date = models.DateTimeField(auto_now_add=False)



class stock(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='fsdsdgv')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fsdsdd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='csdsvg')
    total_bag = models.BigIntegerField()

    



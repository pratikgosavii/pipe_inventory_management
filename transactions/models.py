from django.db import models

# Create your models here.



from users.models import User
from datetime import datetime, timezone
from store.models import *



class inward(models.Model):

    godown = models.ForeignKey(godown , on_delete=models.CASCADE, related_name='sdwe')
    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='sdwe')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='wfgv')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='xvc')
    transport = models.ForeignKey(transport , on_delete=models.CASCADE, related_name='sdsxc', null=True, blank=True)
    LR_number = models.CharField(max_length=50, null = True, blank = True)
    freight = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.BigIntegerField()
    DC_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.company.company_name

   

class outward(models.Model):

    godown = models.ForeignKey(godown , on_delete=models.CASCADE, related_name='fgv')
    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='fgv')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='cvg')
    agent = models.ForeignKey(agent , on_delete=models.CASCADE, related_name='df', null = True, blank = True)
    transport = models.ForeignKey(transport , on_delete=models.CASCADE, related_name='ddssszc', null=True, blank=True)
    LR_number = models.CharField(max_length=50, null = True, blank = True)
    freight = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.BigIntegerField()
    DC_date = models.DateField(auto_now_add=False)


    gate_pass_no = models.BigIntegerField(default=1111, null = True, blank = True)
    gate_pass_name = models.CharField(max_length=100, null = True, blank = True)

    


class supply_return(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='we')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='tr')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='wegvge')
    transport = models.ForeignKey(transport , on_delete=models.CASCADE, related_name='scxsesdf', null=True, blank=True)
    LR_number = models.CharField(max_length=50, null = True, blank = True)
    freight = models.CharField(max_length=50, null = True, blank = True)
    bags = models.BigIntegerField()
    DC_number = models.CharField(max_length=566)
    DC_date = models.DateField(auto_now_add=False)




class stock(models.Model):

    company = models.ForeignKey(company , on_delete=models.CASCADE, related_name='fsdsdgv')
    company_goods = models.ForeignKey(company_goods , on_delete=models.CASCADE, related_name='fsdsdd')
    goods_company = models.ForeignKey(goods_company , on_delete=models.CASCADE, related_name='csdsvg')
    total_bag = models.BigIntegerField()

    



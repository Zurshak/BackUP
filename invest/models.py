from django.db import models

class Paper(models.Model):
    name = models.CharField(max_length=30)
    nn = models.FloatField()
    paper_price = models.FloatField(null=True,blank=True)
    broker_pay = models.FloatField(null=True, blank=True)
    dollar_price = models.FloatField(null=True, blank=True)



    def __str__(self):
        return self.name


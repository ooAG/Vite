from django.db import models

class Sale(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} {self.product} {self.amount}"

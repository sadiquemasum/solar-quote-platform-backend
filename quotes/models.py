from django.db import models

class Quote(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    monthly_bill = models.IntegerField()
    monthly_savings = models.IntegerField(
    null=True,
    blank=True,
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

from django.db import models
from ..users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Item(models.Model):
	name = models.CharField(max_length=200)
	quantity = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(100)])
	price = models.DecimalField(max_digits= 5, decimal_places=2, validators= [MaxValueValidator(500)])
	user = models.ForeignKey(User)
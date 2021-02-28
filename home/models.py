from django.db import models

# Create your models here.
STATUS = (('In','In Stock'),('Out','Out of Stock'))
class category(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 200,unique = True)
    image = models.CharField(max_length = 200,blank = True)
    def __str__(self):
        return self.name

class slider(models.Model):
    name = models.CharField(max_length = 300)
    image = models.TextField()
    description = models.TextField()
    url = models.TextField(blank = True)

    def __str__(self):
        return self.name

class ad(models.Model):
    name = models.CharField(max_length = 300)
    rank = models.IntegerField(unique = True)
    image = models.TextField()
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name
class brand(models.Model):
    name = models.CharField(max_length = 300)
    image = models.TextField()
    rank = models.IntegerField()

    def __str__(self):
        return self.name

class item(models.Model):
    title = models.CharField(max_length = 300)
    price = models.IntegerField()
    slug = models.CharField(max_length = 300,unique = True)
    discounted_price = models.IntegerField(default = 0)
    description = models.TextField()
    category = models.ForeignKey(category,on_delete = models.CASCADE)
    brand = models.ForeignKey(brand,on_delete = models.CASCADE)
    status = models.CharField(max_length = 50,choices = STATUS)

    def __str__(self):
        return self.title


from django.urls import reverse
from django.db import models


# Create your models here.
STATUS = (('In','In Stock'),('Out','Out of Stock'))
LABEL = (('new','New Product'),('hot','Hot Product'),('sale','Sale Product'))
class category(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 200,unique = True)
    image = models.ImageField(upload_to = 'media')
    def __str__(self):
        return self.name
    def get_category_url(self):
        return reverse("home:category",kwargs = {'slug':self.slug})

class slider(models.Model):
    name = models.CharField(max_length = 300)
    image = models.ImageField(upload_to = 'media')
    description = models.TextField()
    url = models.TextField(blank = True)

    def __str__(self):
        return self.name

class ad(models.Model):
    name = models.CharField(max_length = 300)
    rank = models.IntegerField(unique = True)
    image = models.ImageField(upload_to = 'media')
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name
class brand(models.Model):
    name = models.CharField(max_length = 300)
    image = models.ImageField(upload_to = 'media')
    rank = models.IntegerField()

    def __str__(self):
        return self.name

    def get_category_url(self):
        return reverse("home:brand", kwargs={'name': self.name})


class item(models.Model):
    title = models.CharField(max_length = 300)
    price = models.IntegerField()
    slug = models.CharField(max_length = 300,unique = True)
    discounted_price = models.IntegerField(default = 0)
    description = models.TextField()
    category = models.ForeignKey(category,on_delete = models.CASCADE)
    brand = models.ForeignKey(brand,on_delete = models.CASCADE)
    status = models.CharField(max_length = 50,choices = STATUS)
    label = models.CharField(max_length = 60,choices = LABEL,default = 'new')
    image = models.ImageField(upload_to = 'media')

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("home:product",kwargs = {'slug':self.slug})

    def get_cart_url(self):
        return reverse("home:add-to-cart",kwargs = {'slug':self.slug})

class cart(models.Model):
    item = models.ForeignKey(item,on_delete = models.CASCADE)
    slug = models.CharField(max_length = 200)
    quantity = models.IntegerField(default = 1)
    user = models.CharField(max_length = 200)
    date = models.DateTimeField(auto_now = True)
    total = models.IntegerField(null = True)
    def __str__(self):
        return self.user

    def delete_get_cart_url(self):
        return reverse("home:delete-cart", kwargs={'slug': self.slug})

    def delete_single_cart_url(self):
        return reverse("home:delete-single-cart", kwargs={'slug': self.slug})

class contact(models.Model):
    name = models.CharField(max_length = 300)
    email = models.CharField(max_length=300)
    subject =  models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.name
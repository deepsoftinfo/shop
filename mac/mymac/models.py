from django.db import models


class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    old_price=models.IntegerField()
    price=models.IntegerField()
    desc=models.CharField(max_length=4000)
    pub_data=models.DateField()
    image=models.ImageField(upload_to="shop/images")

    def __str__(self):
    	return self.product_name

class Contact(models.Model):
    query_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=70,default="")
    phone=models.CharField(max_length=70,default="")
    msg=models.CharField(max_length=500,default="")
    

    def __str__(self):
        return self.name


class SignUp(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    username=models.CharField(max_length=70,default="")
    password=models.CharField(max_length=70,default="")
    phone=models.IntegerField(default="")
    

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    item_json=models.CharField(max_length=5000)
    name=models.CharField(max_length=100)
    amount=models.CharField(max_length=10,default=0)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+"..."
    

    












from django.db import models
import datetime

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name

class Remedy(models.Model):
    name = models.CharField(max_length=250)

    @staticmethod
    def get_all_remedies():
        return Remedy.objects.all()
  
    def __str__(self):
        return self.name

#product
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=5, decimal_places=2)
    on_sale = models.BooleanField(default=False)
    product_description = models.TextField()
    product_image = models.ImageField(
        default = 'product_images/default_product_image.jpg', #TODO check if this works
        upload_to = 'product_images'
        )
    
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    #category = models.ManyToManyField(Category, default="Non Categorized") TODO this old category is manytomanyfield and changes things
    remedy = models.ManyToManyField(Remedy, default="None")


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Product.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
        
    @staticmethod
    def get_all_products_by_remedyid(remedy_id):
        if remedy_id:
            return Product.objects.filter(remedy=remedy_id)
        else:
            return Product.get_all_products()

    #Future Feature
    #product_id = models.IntegerField()
    #product_category = models.CharField()
    #product_remedies = models.CharField()

    #below are other tables that have a relation to this table
    #product_rating
    #product_review


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)
  
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
  
        return False
    


class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    
    

"""
TODO for now commenting out shipment and review for later versions, product should be all that is needed for MVP
#shipment
class Shipment(models.Model):
    shipment_id = models.IntegerField()
    shipment_date = models.DateField()
    
    #below are other tables that have a relation to this table
    #order_id

#review
class Review(models.Model):
    review_id = models.IntegerField()
    product_review = models.CharField()
    product_rating = models.IntegerField()

    #below are other tables that have a relation to this table
    #customer_id
    #product_id
    #product_name

"""
from django.db import models

# Create your models here.

#product
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=5, decimal_places=2)
    product_description = models.TextField()
    product_image = models.ImageField(
        default = 'product_images/default_product_image.jpg', #TODO check if this works
        upload_to = 'product_images'
        )

    #Future Feature
    #product_id = models.IntegerField()
    #product_category = models.CharField()
    #product_remedies = models.CharField()

    #below are other tables that have a relation to this table
    #product_rating
    #product_review

"""
TODO for now commenting out order, shipment, customer and thensome for later versions, product should be all that is needed for MVP
#order
class Order(models.Model):
    order_id = models.IntegerField()
    order_date = models.DateField()

    #below are other tables that have a relation to this table
    #customer_id
    #product_id

#shipment
class Shipment(models.Model):
    shipment_id = models.IntegerField()
    shipment_date = models.DateField()
    
    #below are other tables that have a relation to this table
    #order_id

#customer
class Customer(models.Model):
    customer_id = models.IntegerField()
    customer_name = models.CharField()
    customer_email = models.CharField()
    customer_address = models.CharField()
    customer_phone_number = models.IntegerField()

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
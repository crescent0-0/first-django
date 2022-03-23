from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    
    # 필드 추가 : default, null속성 필수(기존 삽입된 데이터와 충돌이 생기는 것을 방지하기 위해)
    password = models.CharField(max_length=20, default=None, null=True)
    image = models.CharField(max_length=500, default=None, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Review(models.Model):
    point = models.IntegerField()
    comment = models.CharField(max_length=500)
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
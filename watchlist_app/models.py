from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator

class StreamPlatform(models.Model):
    
    name = models.CharField(max_length=30)
    
    about = models.CharField(max_length=150)
    
    website = models.URLField(max_length=100)
    
    def __str__(self) -> str:
        
        return self.name
    


class WatchList(models.Model):
    
    title = models.CharField(max_length=50)
    
    average_rating = models.FloatField(default=0)
    
    total_rating = models.IntegerField(default=0)
    
    sum_of_rating = models.FloatField(default=0)  ## Just used it for ease of calculation purposes, bascially to easily calculate the average rating

    description = models.CharField(max_length= 200)
    
    active = models.BooleanField(default = True) 
    
    created = models.DateTimeField(auto_now=True)
    
    ott_platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist', default=1)  ## Many to one relation, i.e Each Movie has one StreamPlatform (indicated by the foreign key), but a StreamPlatform can have many Movies associated with it.
                                                                                ## e.g Tarzan movie is only in youtube( only connected to youtube stream platform), but Youtube can have many movies(so connected to many)
    
     
#field_name = models.ForeignKey(TargetModel, on_delete=models.CASCADE)    

    def __str__(self) -> str:
        
        return self.title
    

class Review(models.Model):
    
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    description = models.CharField(max_length=200, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    update = models.DateTimeField(auto_now=True)
    
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    
    def __str__(self):
        
        return str(self.rating) + ' star  '  + self.watchlist.title
    
    

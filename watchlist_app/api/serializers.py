from rest_framework import serializers

from watchlist_app.models import WatchList, StreamPlatform, Review, User




class ReviewSerializer(serializers.ModelSerializer):
    
    review_user = serializers.StringRelatedField(read_only=True)  ## WE DONT WRITE MANY = TRUE, BECAUSE A SPECIFIC REVIEW(which is queried) CAN BE WRITTEN BY ONE USER ONLY, A USER CAN HAVE MANY REVIEWS, BUT A REVIEW WILL HAVE ONLY ONE USER 
    
    class Meta:
        model = Review
        fields= '__all__'
    


class WatchListSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        
        model = WatchList
     #   fields= '__all__'
        exclude = ['sum_of_rating']
        
        
 
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        
        model = StreamPlatform
        fields= '__all__'
        
        

    
        

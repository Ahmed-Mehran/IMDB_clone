from rest_framework import serializers

from watchlist_app.models import WatchList, StreamPlatform, Review

from database import session  # Importing the SQLAlchemy session




class ReviewSerializer(serializers.ModelSerializer):
    
    review_user = serializers.StringRelatedField(read_only=True)  ## WE DONT WRITE MANY = TRUE, BECAUSE A SPECIFIC REVIEW(which is queried) CAN BE WRITTEN BY ONE USER ONLY, A USER CAN HAVE MANY REVIEWS, BUT A REVIEW WILL HAVE ONLY ONE USER 
    
    class Meta:
        model = Review
        fields= '__all__'
    


# class WatchListSerializer(serializers.ModelSerializer):

#     reviews = ReviewSerializer(many=True, read_only=True)
    
#     class Meta:
        
#         model = WatchList
#      #   fields= '__all__'
#         exclude = ['sum_of_rating']


## Modifying the WatchListSerializer to work with SQLAlchemy
class WatchListSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=50)
    average_rating = serializers.FloatField(required=False)
    total_rating = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=200)
    active = serializers.BooleanField(default=True)
    created = serializers.DateTimeField(read_only=True)
    ott_platform_id = serializers.UUIDField()
    
    # reviews = ReviewSerializer(many=True, read_only=True)

    def create(self, validated_data):

        new_watchlist = WatchList(
            title=validated_data['title'],
            average_rating=validated_data.get('average_rating', 0),
            total_rating=validated_data.get('total_rating', 0),
            description=validated_data['description'],
            active=validated_data.get('active', True),
            ott_platform_id=validated_data['ott_platform_id']
        )
        session.add(new_watchlist)
        session.commit()
        session.refresh(new_watchlist)
        return new_watchlist

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.average_rating = validated_data.get('average_rating', instance.average_rating)
        instance.total_rating = validated_data.get('total_rating', instance.total_rating)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.ott_platform_id = validated_data.get('ott_platform_id', instance.ott_platform_id)

        session.commit()
        session.refresh(instance)
        return instance
        
        
 
# class StreamPlatformSerializer(serializers.ModelSerializer):
    
#     watchlist = WatchListSerializer(many=True, read_only=True)
    
#     class Meta:
        
#         model = StreamPlatform
#         fields= '__all__'

## Cant use the above serializer because we are using SQLAlchemy and SQLAlchemy does not work with serializer.ModelSerializer.
##  So we have to write the serializer manually below
class StreamPlatformSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=30)
    about = serializers.CharField(max_length=150)
    website = serializers.CharField(max_length=100)
    watchlist = WatchListSerializer(many=True, read_only=True)


    def create(self, validated_data):
        new_platform = StreamPlatform(
            name=validated_data['name'],
            about=validated_data['about'],
            website=validated_data['website']
        )
        session.add(new_platform)
        session.commit()
        session.refresh(new_platform)
        return new_platform

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.about = validated_data.get('about', instance.about)
        instance.website = validated_data.get('website', instance.website)
        session.commit()
        session.refresh(instance)
        return instance
        

    
        

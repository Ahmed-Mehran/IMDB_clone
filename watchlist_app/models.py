# from django.db import models
# from django.contrib.auth.models import User

# from django.core.validators import MinValueValidator, MaxValueValidator

# class StreamPlatform(models.Model):
    
#     name = models.CharField(max_length=30)
    
#     about = models.CharField(max_length=150)
    
#     website = models.URLField(max_length=100)
    
#     def __str__(self) -> str:
        
#         return self.name
    


# class WatchList(models.Model):
    
#     title = models.CharField(max_length=50)
    
#     average_rating = models.FloatField(default=0)
    
#     total_rating = models.IntegerField(default=0)
    
#     sum_of_rating = models.FloatField(default=0)  ## Just used it for ease of calculation purposes, bascially to easily calculate the average rating

#     description = models.CharField(max_length= 200)
    
#     active = models.BooleanField(default = True) 
    
#     created = models.DateTimeField(auto_now=True)
    
# #     ott_platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist', default=1)  ## Many to one relation, i.e Each Movie has one StreamPlatform (indicated by the foreign key), but a StreamPlatform can have many Movies associated with it.
# #                                                                                 ## e.g Tarzan movie is only in youtube( only connected to youtube stream platform), but Youtube can have many movies(so connected to many)
    
     
# #field_name = models.ForeignKey(TargetModel, on_delete=models.CASCADE)    

#     def __str__(self) -> str:
        
#         return self.title
    

# class Review(models.Model):
    
#     review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    
#     description = models.CharField(max_length=200, null=True)
    
#     created = models.DateTimeField(auto_now_add=True)
    
#     update = models.DateTimeField(auto_now=True)
    
#     watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    
#     def __str__(self):
        
#         return str(self.rating) + ' star  '  + self.watchlist.title

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class StreamPlatform(Base):
    __tablename__ = "stream_platform"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(30), nullable=False)
    about = Column(String(150), nullable=False)
    website = Column(String(100), nullable=False)

    # One-to-many relationship with WatchList
    watchlist = relationship("WatchList", back_populates="ott_platform", cascade="all, delete")

    def __repr__(self):
        return f"<StreamPlatform(name='{self.name}')>"
    


class WatchList(Base):
    __tablename__ = "watch_list"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    average_rating = Column(Float, default=0)
    total_rating = Column(Integer, default=0)
    sum_of_rating = Column(Float, default=0)
    description = Column(String(200), nullable=False)
    active = Column(Boolean, default=True)
    created = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign key to StreamPlatform
    ott_platform_id = Column(UUID(as_uuid=True), ForeignKey("stream_platform.id", ondelete="CASCADE"), nullable=False)

    # One-to-many relationship with Review
    reviews = relationship("Review", back_populates="watchlist", cascade="all, delete")

    # Reverse relation for StreamPlatform
    ott_platform = relationship("StreamPlatform", back_populates="watchlist")

    def __repr__(self):
        return f"<WatchList(title='{self.title}')>"


class Review(Base):
    __tablename__ = "review"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    review_user_id = Column(Integer, nullable=False)  # Mapping Django User manually
    rating = Column(Integer, nullable=False)
    description = Column(String(200))
    created = Column(DateTime(timezone=True), server_default=func.now())
    update = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign key to WatchList
    watchlist_id = Column(UUID(as_uuid=True), ForeignKey("watch_list.id", ondelete="CASCADE"), nullable=False)

    # Relationship
    watchlist = relationship("WatchList", back_populates="reviews")

    def __repr__(self):
        return f"<Review(rating='{self.rating} star')>"

    
    

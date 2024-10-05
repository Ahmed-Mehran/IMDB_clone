from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.views import APIView

from watchlist_app.models import WatchList,StreamPlatform, Review

from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

from watchlist_app.api.permissions import AdminOrReadOnly, IsUserOrAdminOnly

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from watchlist_app.api.throttling import ReviewDetailsThrottle, ReviewListThrottle



class StreamPlatformAV(APIView):   ## View for accesing all stream platform like netflix, prime vids
    
    permission_classes = [AdminOrReadOnly] 
    
    def get(self, request):
        
        platform = StreamPlatform.objects.all()
        
        serializer = StreamPlatformSerializer(platform, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        
        serializer = StreamPlatformSerializer(data=request.data, )
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response(serializer.errors)
        
        
        
class StreamPlatformDetailsAV(APIView):   ## View for accesing stream platform individually
    
    permission_classes = [AdminOrReadOnly] 
    
    def get(self, request, pk):
        
        platform_detail = StreamPlatform.objects.get(pk=pk)
        
        serializer = StreamPlatformSerializer(platform_detail)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        
        platform_detail = StreamPlatform.objects.get(pk=pk)
        
        serializer = StreamPlatformSerializer(platform_detail, data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, pk):
        
        platform_detail = StreamPlatform.objects.get(pk=pk)
        
        platform_detail.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
        
        


class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly] 
    
    def get(self, request):
        
        films = WatchList.objects.all()
        
        serializer = WatchListSerializer(films, many=True)
        
        return Response(serializer.data)
    
    
    def post(self, request):
        
        serializer = WatchListSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response(serializer.errors)
        
        
        
class WatchDetailAV(APIView):
    
    permission_classes = [AdminOrReadOnly] 
    
    def get(self, request, pk):
        
        film = WatchList.objects.get(pk=pk)  
                
        serializer = WatchListSerializer(film)

        return Response(serializer.data)
    
    
    def put(self, request, pk):
        
        film = WatchList.objects.get(pk=pk)  
        
        serializer = WatchListSerializer(film, data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, pk):
    
        film = WatchList.objects.get(pk=pk)
        
        film.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class ReviewListAV(APIView):  
    
    permission_classes = [IsAuthenticated] 
  
 #   throttle_classes = [ReviewListThrottle]
    
    def get(self, request, pk):
        
        reviews = Review.objects.filter(watchlist_id=pk)
        
        serializer = ReviewSerializer(reviews, many=True)
        
        return Response(serializer.data)
    
    
    def post(self, request, pk):
        
        user = request.user
        
        watchlist = get_object_or_404(WatchList, pk=pk)
        
        # Check if the user has already reviewed this movie
        if Review.objects.filter(watchlist=watchlist, review_user=user).exists():
            
            return Response({"error": "You have already reviewed this movie."}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            
            
            review = serializer.save(review_user=user, watchlist=watchlist) ## or serializer.save(watchlist_id=pk)  # so what it is saying is that if serializer is valid, then save the pk value(of the movie) with watchlist_id(which is a foreign key field) of Review Model
            
            watchlist.total_rating += 1  
            watchlist.sum_of_rating = watchlist.sum_of_rating + review.rating
            
            watchlist.average_rating  = (watchlist.sum_of_rating) / (watchlist.total_rating)
                
            
            
            watchlist.save()
            
            serializer.save(review_user=user, watchlist=watchlist)
            
            return Response(serializer.data)
        
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
  


class ReviewDetailsAV(APIView):

    permission_classes = [IsUserOrAdminOnly, IsAuthenticated]
    
   # throttle_classes = [ReviewDetailsThrottle]
    
    def get(self, request, pk):
        
        review_item = Review.objects.get(pk=pk)  
                
        serializer = ReviewSerializer(review_item)

        return Response(serializer.data)
    
    
    def put(self, request, pk):
        
        review_item = Review.objects.get(pk=pk) 
        
        self.check_object_permissions(request, review_item) 
        
        serializer = ReviewSerializer(review_item, data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data)
        
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, pk):
    
        review_item = Review.objects.get(pk=pk)
        
        review_item.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
        
        




    

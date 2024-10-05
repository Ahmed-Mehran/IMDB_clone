from rest_framework.throttling import UserRateThrottle



class ReviewListThrottle(UserRateThrottle):
    
    scope = 'review-list'
    
    
    
class ReviewDetailsThrottle(UserRateThrottle):
    
    scope = 'review-details'
    
    
    
    

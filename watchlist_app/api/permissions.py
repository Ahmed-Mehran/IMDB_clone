from rest_framework import permissions

from rest_framework.permissions import IsAdminUser, IsAuthenticated



class AdminOrReadOnly(IsAdminUser):
    
    def has_permission(self, request, view):
    
        admin_permission = bool(request.user and request.user.is_staff)
        
        not_admin = request.method =='GET'
        
        if admin_permission ==True:
            
            return True
        
        return not_admin
    
    
class IsUserOrAdminOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:  ## see as this permission was used for only logged in user to edit/delete their review, but we also want Admin user to edit/delete any review, thus adding this line
            return True
         
            
        return obj.review_user == request.user 
    

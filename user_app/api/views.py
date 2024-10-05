from rest_framework.views import APIView
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token



class RegistrationAPI(APIView):
    
    def post(self, request):
        
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            
            account = serializer.save()  # Saving the user account
            
            # Get or create token for the user and saving the token against the user created
            token, created = Token.objects.get_or_create(user=account)
            
            # Return the user data and token in the response
            response_data = {
                
                'username': account.username,
                
                'email': account.email,
                
                'token': token.key
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
    
class LogoutAPI(APIView):
    
    def delete(self, request,):
        
        request.user.auth_token.delete()
        
        return  Response(status=status.HTTP_200_OK)
    
    



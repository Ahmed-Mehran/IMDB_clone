from django.contrib.auth.models import User

from rest_framework import serializers

from rest_framework.authtoken.models import Token



class RegistrationSerializer(serializers.ModelSerializer):
    
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password1', 'password2']
            


    def save(self):
        
        password1  = self.validated_data['password1']
        password2  = self.validated_data['password2']
        
        if password1 != password2:
            
            raise serializers.ValidationError({"Error: Password1 and Password2 doesn't match"})
        
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            
            raise serializers.ValidationError({'Error' : 'Email already in use!'})
        
        
        
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(password1)
        account.save()
    

        return account
        
  

   
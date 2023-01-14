from rest_framework.authentication import TokenAuthentication

class TokenAuthenticationSafe(TokenAuthentication):
    def authenticate(self,request):
        try:
            return super().authenticate(request=request)
        except:
            return None
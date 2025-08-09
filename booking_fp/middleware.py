# booking_fp/middleware.py

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken,BlacklistedToken
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import resolve
from rest_framework.permissions import AllowAny

class JWTAuthenticationMiddleware(MiddlewareMixin):

    permission_classes = [AllowAny]

    def process_request(self, request):
        # Здесь указаны эндпоинты по которым НЕ нужно проверять наличие токена:
        excluded_paths = [
            # '/api/v1/users/registration',
            # '/api/v1/users/login/',
            '/api/v1/users/logout/',
            '/api/token/',
            '/api/token/refresh/',
        ]

        if any(request.path_info.startswith(path) for path in excluded_paths):
            return
        # if request.path_info in ['/api/v1/users/registration', '/api/v1/users/login', '/api/v1/users/logout']:
        #     return
        access_token_cookie = request.COOKIES.get('access_token')

        if access_token_cookie:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token_cookie}'


    def process_response(self, request, response):

        if response.status_code == 401 and b'Token is expired' in response.content:
            refresh_token_cookie = request.COOKIES.get('refresh_token')

            if refresh_token_cookie:
                try:
                    if OutstandingToken.objects.filter(token=refresh_token_cookie).exists():
                        if BlacklistedToken.objects.filter(token__token=refresh_token_cookie).exists():
                            response.delete_cookie('access_token')
                            response.delete_cookie('refresh_token')
                            response.render()
                            return response
                    refresh = RefreshToken(refresh_token_cookie)
                    new_access_token = str(refresh.access_token)

                    if hasattr(refresh,'access_token'):
                        new_refresh_token = str(refresh)
                        response.set_cookie('refresh_token',new_refresh_token,httponly=True,samesite='Lax',secure=False)

                        response.set_cookie('access_token',new_access_token,httponly=True,samesite='Lax',secure=False)

                        view,args,kwargs = resolve(request.path_info)
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                        kwargs['request'] = request
                        new_response = view(request, *args, *kwargs)
                        new_response.set_cookie('access_token',new_access_token,httponly=True,samesite='Lax',secure=False)

                        if hasattr(refresh,'access_token'):
                            new_response.set_cookie('refresh_token', new_refresh_token,httponly=True,samesite='Lax',secure=False)
                        new_response.render()
                        return new_response


                except TokenError:

                    refresh = RefreshToken(refresh_token_cookie)
                    refresh.blacklist()
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token')
                    response.render()
                    return response

        return response
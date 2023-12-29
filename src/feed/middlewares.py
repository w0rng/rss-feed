from random import choices
from string import ascii_letters, digits


class UserIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        new_cookie = ''.join(choices(ascii_letters + digits, k=8))
        request.user_id = request.COOKIES.get('userID', new_cookie)
        response = self.get_response(request)
        response.set_cookie('userID', request.user_id, max_age=60 * 60 * 24 * 365 * 2)
        return response

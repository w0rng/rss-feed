from random import choices
from string import ascii_letters, digits
from django.core.signing import Signer, BadSignature


class UserIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.signer = Signer()

    def __call__(self, request):
        new_cookie = "".join(choices(ascii_letters + digits, k=8))

        if request.user.is_authenticated:
            request.user_id = request.user.id
        elif "userID" in request.COOKIES:
            try:
                request.user_id = self.signer.unsign(request.COOKIES["userID"])
            except BadSignature:
                request.user_id = new_cookie
        else:
            request.user_id = new_cookie

        response = self.get_response(request)

        signed_cookie = self.signer.sign(request.user_id)
        response.set_cookie("userID", signed_cookie, max_age=60 * 60 * 24 * 365 * 2)

        return response

# middleware.py
class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user has accepted cookies
        cookies_accepted = request.COOKIES.get('cookies_accepted', False)
        if not cookies_accepted:
            # If not accepted, handle accordingly (e.g., redirect to a consent page or display a banner)
            pass

        response = self.get_response(request)
        return response

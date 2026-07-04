class ThemePreferenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set default theme to 'dark' for the Marriott/Taj luxury vibe
        if 'theme' not in request.session:
            request.session['theme'] = 'dark'

        response = self.get_response(request)
        return response

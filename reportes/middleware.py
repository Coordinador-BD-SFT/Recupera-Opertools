class GlobalDataMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Añadimos datos globales a la solicitud
        request.vicidial_links = {
            'trans_link': 'https://192.227.120.75/vicidial/admin.php',
            'ivrs_link': 'https://192.227.124.58/vicidial/admin.php',
        }
        response = self.get_response(request)
        return response

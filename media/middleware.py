from media.models import User

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # carrega a informação do model
        my_data = User.objects.filter(username=request.user.username)
        # adiciona a informação no contexto global
        request.my_data = my_data
        # chama a view
        response = self.get_response(request)
        return response

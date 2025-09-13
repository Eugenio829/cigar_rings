from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # No proteger la vista de login para evitar bucles de redirección
        login_url = reverse('login')
        # No proteger el sitio de administración de Django
        admin_url_prefix = '/admin/'

        # Si el usuario no está autenticado
        if not request.user.is_authenticated:
            # Y la ruta solicitada no es la de login ni la de admin
            if request.path_info != login_url and not request.path.startswith(admin_url_prefix):
                # Redirigir al usuario a la página de login
                return redirect(login_url)

        response = self.get_response(request)
        return response

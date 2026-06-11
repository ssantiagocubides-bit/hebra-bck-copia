from django.shortcuts import render

def home_view(request):
    return render(request, 'usuarios/home.html')

# Vista para el Login (ya la tenías, asegúrate de que apunte al nombre exacto de tu archivo)
def login_view(request):
    return render(request, 'usuarios/login.html')

# Nueva Vista para Recuperar Contraseña
def recuperar_view(request):
    return render(request, 'usuarios/recuperar.html')
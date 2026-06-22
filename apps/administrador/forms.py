from django import forms
from .models import Usuario, Tarea, Orden

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'rol']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carlos'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Martínez'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'carlos@ejemplo.com'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['operario', 'descripcion', 'linea', 'fecha_inicio', 'fecha_limite', 'prioridad', 'observaciones']
        widgets = {
            'operario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del operario'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Corte de tela Oxford'}),
            'linea': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Línea 1 — Costura'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instrucciones adicionales...'}),
        }

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'nit', 'telefono', 'correo', 'producto', 'cantidad', 'fecha_entrega', 'estado_pago', 'especificaciones']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT o Documento'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'cliente@correo.com'}),
            'producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de prenda'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_pago': forms.Select(attrs={'class': 'form-select'}),
            'especificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Color, tallas, logos...'}),
        }
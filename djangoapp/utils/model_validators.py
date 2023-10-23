from django.core.exceptions import ValidationError

def validate_png(img):
    if not img.name.lower().endswith('.png'):
        raise ValidationError('A imagem deve ser um png.')
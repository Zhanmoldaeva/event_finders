from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    """
    Возвращает элемент последовательности по заданному индексу.
    """
    try:
        return sequence[int(position)]
    except (IndexError, ValueError, TypeError):
        return None
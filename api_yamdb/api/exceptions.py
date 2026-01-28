from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        view = context.get('view')
        model_name = "Объект"

        if view and hasattr(view, 'queryset') and view.queryset is not None:
            model_name = view.queryset.model._meta.verbose_name.capitalize()

        if response.status_code == 404:
            response.data = {'detail': f'{model_name} не найден(а)'}

        elif response.status_code == 403:
            response.data = {'detail': 'Нет прав доступа'}

        elif response.status_code == 401:
            response.data = {'detail': 'Необходим JWT-токен'}

    return response
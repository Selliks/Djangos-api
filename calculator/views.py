from django.http import JsonResponse
from .models import Todo


def add_action(request):
    name = request.GET.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    todo = Todo.objects.create(name=name)
    return JsonResponse({'message': 'Action added', 'id': todo.id})


def delete_action(request):
    todo_id = request.GET.get('id')
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return JsonResponse({'message': 'Action deleted'})
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Action not found'}, status=404)


def rename_action(request):
    todo_id = request.GET.get('id')
    new_name = request.GET.get('new_name', '').strip()
    if not new_name:
        return JsonResponse({'error': 'New name is required'}, status=400)
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.name = new_name
        todo.save()
        return JsonResponse({'message': 'Action renamed'})
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Action not found'}, status=404)


def get_all_action(request):
    todos = Todo.objects.all().values('id', 'name', 'created_at')
    return JsonResponse({'actions': list(todos)})


def calculate(request):
    expression = request.GET.get('expression', '')
    if not expression:
        return JsonResponse({'error': 'No expression provided'}, status=400)

    try:
        result = eval(expression)
        return JsonResponse({'expression': expression, 'result': result})
    except ZeroDivisionError:
        return JsonResponse({'error': 'Division by zero is not allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Invalid expression: {str(e)}'}, status=400)

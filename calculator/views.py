import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Todo


@csrf_exempt
def add_action(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        print(f"Name: {name}")
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        todo = Todo.objects.create(name=name)
        return JsonResponse({'message': 'Action added', 'id': todo.id})
    else:
        return HttpResponse("Method is not allowed. Only POST", status=405)


@csrf_exempt
def delete_action(request):
    if request.method == 'DELETE':
        todo_id = request.DELETE.get('id')
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            return JsonResponse({'message': 'Action deleted'})
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Action not found'}, status=404)
    else:
        return HttpResponse("Method is not allowed. Only DELETE", status=405)


@csrf_exempt
def rename_action(request):
    if request.method() == 'PUT':
        todo_id = request.PUT.get('id')
        new_name = request.PUT.get('new_name', '').strip()
        if not new_name:
            return JsonResponse({'error': 'New name is required'}, status=400)
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.name = new_name
            todo.save()
            return JsonResponse({'message': 'Action renamed'})
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Action not found'}, status=404)
    else:
        return HttpResponse("Method is not allowed. Only PUT", status=405)


@csrf_exempt
def get_all_action(request):
    if request.method() == 'GET':
        todos = Todo.objects.all().values('id', 'name', 'created_at')
        return JsonResponse({'actions': list(todos)})
    else:
        return HttpResponse("Method is not allowed. Only GET", status=405)


@csrf_exempt
def calculate(request):
    if request.method() == 'POST':
        expression = request.POST.get('expression', '')
        if not expression:
            return JsonResponse({'error': 'No expression provided'}, status=400)

        try:
            result = eval(expression)
            return JsonResponse({'expression': expression, 'result': result})
        except ZeroDivisionError:
            return JsonResponse({'error': 'Division by zero is not allowed'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Invalid expression: {str(e)}'}, status=400)
    else:
        return HttpResponse("Method is not allowed. Only POST", status=405)

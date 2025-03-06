def add_saved_account(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Перевіряємо чи існує користувач і чи правильний пароль
            User = get_user_model()
            account_to_add = get_object_or_404(User, username=username)
            
            if not account_to_add.check_password(password):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Неправильний пароль'
                })
            
            # Зберігаємо пароль
            SavedAccount.objects.update_or_create(
                user=request.user,
                username=username,
                defaults={
                    'password': password
                }
            )
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Метод не дозволений'})
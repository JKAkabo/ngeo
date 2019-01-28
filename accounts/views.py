from django.contrib import messages
from django.contrib.auth import authenticate, login as lin
from django.shortcuts import redirect, render

from .forms import LoginForm


def login(request):
    template_name = 'accounts/login.html'
    login_form = LoginForm

    if request.method == 'POST':
        login_form = login_form(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    lin(request, user)
                    messages.success(request, f'Successfully logged in as {user.username}', 'alert-success')
                    return redirect('product:index')
                else:
                    messages.success(request, 'Your account is inactive. Please contact your system administrator.')
            else:
                messages.error(request, 'Incorrect username or password. Please try again.', 'alert-danger')
                context = {
                    'login_form': login_form,
                }
                return render(request, template_name, context)
        else:
            messages.error(request, 'The form contains some errors. Please try again.' 'alert-danger')
            context = {
                'login_form': login_form,
            }
            return render(request, template_name, context)
    else:
        context = {
            'login_form': login_form,
        }
        return render(request, template_name, context)
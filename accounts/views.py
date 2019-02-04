from django.contrib import messages
from django.contrib.auth import authenticate, login as lin, logout as lout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ConfirmStaffRegistrationForm, LoginForm, StaffRegistrationForm


def login(request):
    template_name = 'accounts/login.html'
    form = LoginForm

    if request.method == 'POST':
        form = form(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
                    'form': form,
                }
                return render(request, template_name, context)
        else:
            messages.error(request, 'The form contains some errors. Please try again.' 'alert-danger')
            context = {
                'form': form,
            }
            return render(request, template_name, context)
    else:
        context = {
            'form': form,
        }
        return render(request, template_name, context)


# under construction
@login_required()
def register_staff(request):
    template_name = 'accounts/register_staff.html'
    form = StaffRegistrationForm

    if request.method == 'POST':
        form = form(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
    else:
        context = {
            'form': form,
        }
        return render(request, template_name, context)


# under construction
@login_required()
def confirm_staff_registration(request):
    template_name = 'accounts/confirm_staff_registration.html'


@login_required(redirect_field_name=None)
def logout(request):
    lout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('accounts:login')

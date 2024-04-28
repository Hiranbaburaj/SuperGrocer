from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import RegistrationForm , LoginForm

def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_supplier:
                    return redirect('supplier_dashboard')
                elif user.is_buyer:
                    return redirect('shop')
    context = {'form': forms}
    return render(request, 'users/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'users/registration.html', context)



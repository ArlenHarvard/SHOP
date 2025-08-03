from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import *
from .forms import  *
from .services import generate_otp_code
from django.conf import settings
from django.contrib.auth.decorators import login_required


def user_register_view(request):

    if request.method == 'POST':
        form = MyUserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали аккаунт')
            return redirect('index')
    else:
        form = MyUserRegisterForm()

    return render(
        request=request,
        template_name='authentication/register.html',
        context={
            "form": form
        }
    )


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import MyUserLoginForm

def user_login_view(request):
    if request.method == 'POST':
        form = MyUserLoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']

            # Аутентификация
            user = authenticate(request, username=user_email, password=user_password)

            if user:
                # Проверяем, включена ли 2FA
                if user.is_2fa_enabled:
                    # Генерируем и отправляем OTP-код
                    otp_code = generate_otp_code()
                    OTP.objects.create(
                        user=user,
                        code=otp_code
                    )

                    send_mail(
                        "Одноразовый код",
                        f"{otp_code}",
                        settings.DEFAULT_FROM_EMAIL,
                        [user_email],
                        fail_silently=False,
                    )
                    messages.success(request, "Одноразовый код отправлен на вашу почту")
                    return redirect('otp_verify', user.id)
                else:
                    # Если 2FA выключена, сразу логиним пользователя
                    login(request, user)
                    messages.success(request, "Вы успешно вошли в систему")
                    return redirect('index')

            else:
                messages.error(request, 'Неправильный логин или пароль')
    else:
        form = MyUserLoginForm()

    return render(
        request,
        'authentication/login.html',
        {'form': form}
    )

def logout_view(request):
    logout(request)
    return redirect('index')



def otp_verify_view(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)

    if request.method == "POST":
        if "resend" in request.POST:  # если нажата кнопка "Выслать повторно"
            otp_code = generate_otp_code()
            OTP.objects.create(user=user, code=otp_code)

            send_mail(
                "Одноразовый код (новый)",
                f"{otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Новый код отправлен на почту")
            return redirect("otp_verify", user.id)

        otp_code = request.POST.get("otp")

        otp = OTP.objects.filter(user=user, code=otp_code).last()
        if otp and otp.is_valid():
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему")
            otp.delete()
            return redirect("index")
        else:
            messages.error(request, "Неверный или просроченный код")

    return render(
        request,
        "authentication/otp_verify.html",
        {"user_id": user.id}
    )



@login_required
def user_profile(request):
    return render(request, 'authentication/profile.html')


@login_required
def manage_2fa(request):
    user = request.user

    if request.method == 'POST':
        user.is_2fa_enabled = not user.is_2fa_enabled
        user.save()
        if user.is_2fa_enabled:
            messages.success(request, "✅ Двухэтапная аутентификация включена")
        else:
            messages.warning(request, "❌ Двухэтапная аутентификация выключена")
        return redirect('manage_2fa')

    return render(request, 'authentication/manage_2fa.html', {'user': user})


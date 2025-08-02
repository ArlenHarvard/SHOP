from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Estate, Favorite, Category
from itertools import chain
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail



def index_view(request):
    user = request.user

    # Все категории и только родительские
    categories = Category.objects.all()
    parent_categories = Category.objects.filter(parent_category__isnull=True)

    # Получаем выбранную категорию из GET
    category_id = request.GET.get('category')
    current_category = None
    estates = Estate.objects.filter(is_active=True)

    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            current_category = category.id
            # Фильтр: если выбрали родительскую — показать и подкатегории
            if category.parent_category is None:
                subcategories = Category.objects.filter(parent_category=category)
                estates = estates.filter(category__in=list(chain([category], subcategories)))

            else:
                estates = estates.filter(category=category)
        except Category.DoesNotExist:
            pass

    estates = estates[:8]  # ограничение

    if user.is_authenticated:
        liked_ids = set(Favorite.objects.filter(user=user, estate__in=estates).values_list('estate_id', flat=True))
    else:
        liked_ids = set()

    estates_with_likes = [
        {'estate': estate, 'liked': estate.id in liked_ids}
        for estate in estates
    ]



    return render(request, 'main/index.html', {
        'categories': categories,
        'parent_categories': parent_categories,
        'current_category': current_category,
        'estates_with_likes': estates_with_likes,
    })


from django.shortcuts import render, get_object_or_404
from .models import Estate

def detail_view(request, estate_pk):
    estate = get_object_or_404(Estate, pk=estate_pk)
    user = request.user if request.user.is_authenticated else None
    return render(request, 'main/estate_detail.html', {
        'estate': estate,
        'user': user,
    })



@login_required
def toggle_like(request):
    if request.method == 'POST':
        estate_id = request.POST.get('estate_id')
        estate = get_object_or_404(Estate, id=estate_id)

        favorite, created = Favorite.objects.get_or_create(user=request.user, estate=estate)
        if not created:  # уже лайкал — удаляем
            favorite.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)




def favorite_list_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Войдите в систему')
        return redirect('index')


    favorite_estates = Favorite.objects.filter(user=request.user).order_by('-id')

    return render(request=request,
                  template_name='main/favorite_list.html',
                  context={'favorite_estates': favorite_estates

                  }
            )
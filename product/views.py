from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from unicodedata import category

from .models import Estate, Favorite, Category, Feedback
from itertools import chain
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from itertools import chain
from .models import Estate, Favorite, Category
from .models import Estate, Category, Favorite, City




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
    recommended_estates = Estate.objects.filter(
        category=estate.category,
        city=estate.city
    ).exclude(id=estate.id)
    estates_like = Favorite.objects.filter(estate=estate).count()

    # Берём только верхние комментарии (без parent)
    feedbacks = estate.feedbacks.filter(parent__isnull=True).order_by('-created_at')

    user = request.user if request.user.is_authenticated else None
    return render(request, 'main/estate_detail.html', {
        'estate': estate,
        'user': user,
        'recommended_estates': recommended_estates,
        'estates_like': estates_like,
        'feedbacks': feedbacks,  # ✅ добавили сюда
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




@login_required
def user_estate_feedback(request, estate_id):
    estate = get_object_or_404(Estate, id=estate_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')  # берем id родительского комментария, если есть

        parent = None
        if parent_id:
            parent = Feedback.objects.get(id=parent_id)

        Feedback.objects.create(
            user=request.user,
            estate=estate,
            comment=comment,
            parent=parent
        )

        messages.success(request, 'Комментарий успешно отправлен')
        return redirect('detail', estate_pk=estate.id)
# Редирект на страницу с деталями
    else:
        # Если GET — показать страницу с формой (если нужно)
        return render(request, 'estate.detail.html', {'estate': estate})




# product/views.py


def estate_list_view(request):
    user = request.user
    categories = Category.objects.all()
    parent_categories = Category.objects.filter(parent_category__isnull=True)

    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    city_id = request.GET.get('city')  # Здесь ID города

    current_category = None
    estates = Estate.objects.filter(is_active=True)

    # Фильтр по категории
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            current_category = category
            if category.parent_category is None:
                subcategories = Category.objects.filter(parent_category=category)
                estates = estates.filter(category__in=list(chain([category], subcategories)))
            else:
                estates = estates.filter(category=category)
        except Category.DoesNotExist:
            pass

    # Фильтр по цене
    if min_price:
        estates = estates.filter(price__gte=min_price)
    if max_price:
        estates = estates.filter(price__lte=max_price)

    # Фильтр по городу (по ID)
    if city_id:
        try:
            city_obj = City.objects.get(id=city_id)
            estates = estates.filter(city=city_obj)
        except City.DoesNotExist:
            city_obj = None
    else:
        city_obj = None

    # Пагинация
    paginator = Paginator(estates.order_by('-created_at'), 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if user.is_authenticated:
        liked_ids = set(Favorite.objects.filter(user=user, estate__in=page_obj).values_list('estate_id', flat=True))
    else:
        liked_ids = set()

    estates_with_likes = [
        {'estate': estate, 'liked': estate.id in liked_ids}
        for estate in page_obj
    ]

    # Получаем список городов для фильтра (уникальные объекты City)
    cities = City.objects.all()

    return render(request, 'main/estate_list.html', {
        'categories': categories,
        'parent_categories': parent_categories,
        'current_category': current_category,
        'page_obj': page_obj,
        'estates_with_likes': estates_with_likes,
        'cities': cities,
        'min_price': min_price,
        'max_price': max_price,
        'selected_city': city_id,
    })
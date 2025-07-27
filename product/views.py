from django.shortcuts import render
from .models import Category, Estate


from django.shortcuts import render
from .models import Category

def index_view(request):
    parent_categories = Category.objects.filter(parent_category__isnull=True)
    estates = Estate.objects.filter(is_active=True) [:8]
    category_id = request.GET.get('category')
    if category_id:
        estates = Estate.objects.filter(category_id=category_id, is_active=True)
    else:
        estates = Estate.objects.all() # Показываем первые 8
    categories = Category.objects.all()

    return render(
        request,
        'main/index.html',
        {
            "parent_categories": parent_categories,
            "estates": estates,
            'categories': categories,
            'current_category': category_id,

        }
    )

def detail_view(request):
    return render(
        request=request,
        template_name='main/estate_detail.html'
    )
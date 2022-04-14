from django.shortcuts import render

from apps.menu.models import Category

def design_screen(request, rest_id):
    categories = Category.objects.filter(restaurant = rest_id).first()
    menuItems = categories.menuitem_set.all()

    context_dict = {'rest_id': rest_id,
                        'categories': categories,
                        'menuItems': menuItems}

    return render(request, 'display/design_screen.html', context_dict)
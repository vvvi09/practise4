from django.shortcuts import render


def book_detail(request):
    # Пример данных о книге
    book = {
        'title': 'Гарри Поттер и философский камень',
        'author': 'Дж. К. Роулинг',
        'year': 1997,
        'description': 'История мальчика Гарри Поттера, который узнаёт, что он волшебник, и поступает в школу магии Хогвартс.'
    }

    # Рендерим шаблон и передаем данные
    return render(request, 'book_detail.html', {'book': book})


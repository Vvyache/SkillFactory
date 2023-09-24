from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import News

# Создаем свой набор фильтров для модели News.
# FilterSet, который мы наследуем, должен чем-то напомнить знакомые
# вам Django дженерики.


class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи
        model = News
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'name': ['icontains'],
            # поиск по категории
            'category': ['exact'],
            }
from django import template
# если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются
register = template.Library()
# # Теперь каждый раз, когда мы захотим пользоваться нашими фильтрами, в шаблоне нужно будет прописывать следующий тег:
# # {% load custom_filters %}
stop_words = [
     'плохое_слово1',
     'плохое_слово2',
     'плохое_слово3',
]


class StrException(Exception):
    def __str__(self):
        return 'Фильтр censor принимает только текст'

# Регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
# # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра,
# # т. е. в шаблоне будет примерно следующее - value|censor:arg


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise StrException
    else:
        t = text.split(" ")
        for i, b in enumerate(t):
            if b in stop_words:
                t[i] = b[0] + '*' * int(len(b)-1)
        return ' '.join(t)

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


# @register.filter()
# def censor(text):
#     if not isinstance(text, str):
#         raise StrException
#     else:
#         t = text.split(" ")
#         for i, b in enumerate(t):
#             if b in stop_words:
#                 t[i] = b[0] + '*' * int(len(b)-1)
#         return ' '.join(t)


# Задание 13.2.6
# Реализуйте фильтр, который заменяет все буквы кроме первой и последней на «*» у слов из списка «нежелательных».
# Предполагается, что в качестве аргумента гарантированно передается текст, и слова разделены пробелами. Можно считать,
# что запрещенные слова находятся в списке stop_words.

@register.filter
def censor(value):
    words = value.split()
    result = []
    for word in words:
        if word in stop_words:
            result.append(word[0] + "*" * (len(word) - 2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

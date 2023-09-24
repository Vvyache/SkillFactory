# D 11.4 Доработайте свой интернет-сервис. Напишите команду для manage.py, которая будет удалять все новости из
# какой-либо категории, но только при подтверждении действия в консоли при выполнении команды.

from django.core.management.base import BaseCommand, CommandError
from newapp.models import News, CategoryNews


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = CategoryNews.objects.get(name=options['category'])
            News.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}')) # в случае неправильного подтверждения говорим, что в доступе отказано
        except News.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.name}'))
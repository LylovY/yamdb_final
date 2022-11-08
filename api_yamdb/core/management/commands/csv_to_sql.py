import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

MODELS = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Импорт csv файлов в базу данных'

    def handle(self, *args, **kwargs):

        for model, name_csv in MODELS.items():
            model.objects.all().delete()
            with open(
                f'{settings.CSV_FILE_PATH}{name_csv}', 'r', encoding='utf8'
            ) as file_csv:
                if model == Title:
                    reader = csv.reader(file_csv, delimiter=',')
                    Title.objects.bulk_create(
                        Title(
                            id=int(row[0]),
                            name=row[1],
                            year=row[2],
                            category=Category.objects.get(id=int(row[3])),
                        )
                        for row in list(reader)[1:]
                    )
                elif model == Review:
                    reader = csv.reader(file_csv, delimiter=',')
                    Review.objects.bulk_create(
                        Review(
                            id=int(row[0]),
                            title=Title.objects.get(id=int(row[1])),
                            text=row[2],
                            author=User.objects.get(id=int(row[3])),
                            score=int(row[4]),
                            pub_date=row[5],
                        )
                        for row in list(reader)[1:]
                    )
                elif model == Comment:
                    reader = csv.reader(file_csv, delimiter=',')
                    Comment.objects.bulk_create(
                        Comment(
                            id=int(row[0]),
                            review=Review.objects.get(id=int(row[1])),
                            text=row[2],
                            author=User.objects.get(id=int(row[3])),
                            pub_date=row[4],
                        )
                        for row in list(reader)[1:]
                    )
                elif model == Title.genre.through:
                    reader = csv.reader(file_csv, delimiter=',')
                    Title.genre.through.objects.bulk_create(
                        Title.genre.through(
                            id=int(row[0]),
                            title=Title.objects.get(id=int(row[1])),
                            genre=Genre.objects.get(id=int(row[2])),
                        )
                        for row in list(reader)[1:]
                    )
                else:
                    dict_reader = csv.DictReader(file_csv)
                    model.objects.bulk_create(model(**i) for i in dict_reader)

            self.stdout.write(
                f'Файл {name_csv} импортирован в БД {model.__name__}'
            )
        self.stdout.write('Загрузка в базу данных выполнена успешно!')

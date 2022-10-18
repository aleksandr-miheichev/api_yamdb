import csv

from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, CustomUser)

TABLES = {
    CustomUser: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = "Loads data from csv files"

    def handle(self, *args, **kwargs):
        for model, csv_file in TABLES.items():
            file_path = f'./static/data/{csv_file}'
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=',')
                    for data in reader:
                        model.objects.get_or_create(**data)
                        self.stdout.write(
                            self.style.SUCCESS('Database successfully loaded '
                                               'into models!')
                        )
            except FileNotFoundError:
                print(f'Sorry, the file "{csv_file}" does not exist.')

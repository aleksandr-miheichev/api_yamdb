from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.validators import validate_year, validate_username


class CreatedModel(models.Model):
    """Абстрактная модель для моделей Категория и Жанр."""

    name = models.CharField(
        max_length=256,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Короткая метка'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя',
        validators=[validate_username]
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Фамилия пользователя'
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[EmailValidator]
    )
    confirmation_code = models.BigIntegerField(null=True)
    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль пользователя'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография пользователя'
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='email_user_unique',
                fields=['email', 'username'],
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-username',)

    def __str__(self):
        return self.username[:15]

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        return super().save(*args, **kwargs)


User = CustomUser


class Category(CreatedModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CreatedModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Дата выхода'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles',
    )
    rating = models.IntegerField(
        null=True,
        default=None,
        verbose_name='Рейтинг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр произведения'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'Жанр у произведения "{self.title}": {self.genre}'


class CommonInfo(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Review(CommonInfo):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        default=1,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'invalid': 'Please rate from 1 to 10'},
        verbose_name='Оценка'
    )

    class Meta(CommonInfo.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(CommonInfo):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(CommonInfo.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

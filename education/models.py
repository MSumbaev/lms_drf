from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='education/course/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='education/lesson/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    link = models.URLField(max_length=250, verbose_name='Ссылка на видео', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    METHOD = (
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    date_of_payment = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)

    amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=METHOD, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user} - {self.amount} / {self.date_of_payment}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

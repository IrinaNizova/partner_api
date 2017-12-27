from django.db import models
from django.utils.timezone import now


class CreditOrganization(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Offering(models.Model):
    TYPES = (('CONS', 'Потребительский'),
             ('MORT', 'Ипотека'),
             ('CARL', 'Автокредит'),
             ('CSME', 'Бизнес кредит'))

    create_date = models.DateTimeField(default=now(), verbose_name='Дата создания')
    update_date = models.DateTimeField(default=now(), verbose_name='Дата отправки')
    start_rotation_date = models.DateTimeField(verbose_name='Дата старта ротации')
    end_rotation_date = models.DateTimeField(blank=True, verbose_name='Дата конца ротации')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    type = models.CharField(max_length=4, choices=TYPES, verbose_name='Тип заявки')
    min_score = models.IntegerField(default=0, verbose_name='Минимальный скоринг')
    max_score = models.IntegerField(verbose_name='Максимальный скоринг')
    credit_organization = models.ForeignKey(CreditOrganization, verbose_name='Кредитная организация')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('credit_organization', 'title',)
        verbose_name = 'предложение'
        verbose_name_plural = 'предложения'



class CustomerProfile(models.Model):
    create_date = models.DateTimeField(default=now(), verbose_name='Дата создания')
    update_date = models.DateTimeField(default=now(), verbose_name='Дата отправки')
    surname = models.CharField(max_length=25, verbose_name='Фамилия')
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    middle_name = models.CharField(max_length=20, verbose_name='Отчество')
    birthday_date = models.DateField()
    phone = models.CharField(max_length=10, verbose_name='Мобильный телефон')
    passport_number = models.CharField(max_length=10, unique=True, verbose_name='Паспорт')
    score = models.IntegerField(default=0)


    def __str__(self):
        return " ".join((self.first_name, self.middle_name, self.surname))

    class Meta:
        verbose_name = 'анкету клиента'
        verbose_name_plural = 'анкеты клиентов'

class ReuqestToCredit(models.Model):
    STATUSES = (('N', 'Новая'), ('S', 'Отправлена'))

    create_date = models.DateTimeField(default=now(), verbose_name='Дата создания')
    send_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата отправки')
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name='Анкета клиента')
    offering = models.ForeignKey('Offering', verbose_name='Предложение')
    status = models.CharField(max_length=4, choices=STATUSES, default='N', verbose_name='Статус')

    class Meta:
        verbose_name = 'заявку в кредитную организацию'
        verbose_name_plural = 'заявки в кредитную организацию'



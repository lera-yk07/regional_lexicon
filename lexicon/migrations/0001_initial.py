from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название города')),
                ('population', models.IntegerField(blank=True, null=True, verbose_name='Население')),
                ('founded_year', models.IntegerField(blank=True, null=True, verbose_name='Год основания')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название региона')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='Слово или выражение')),
                ('meaning', models.TextField(verbose_name='Значение')),
                ('example', models.TextField(blank=True, verbose_name='Пример использования')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('views_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='lexicon.city', verbose_name='Город')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Слово',
                'verbose_name_plural': 'Слова',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compared_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата сравнения')),
                ('common_words_count', models.IntegerField(default=0, verbose_name='Количество общих слов')),
                ('city1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparisons_as_city1', to='lexicon.city', verbose_name='Первый город')),
                ('city2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparisons_as_city2', to='lexicon.city', verbose_name='Второй город')),
            ],
            options={
                'verbose_name': 'Сравнение',
                'verbose_name_plural': 'Сравнения',
                'ordering': ['-compared_at'],
            },
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='lexicon.region', verbose_name='Регион'),
        ),
    ]

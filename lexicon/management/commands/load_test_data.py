from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lexicon.models import Region, City, Word
import random

class Command(BaseCommand):
    help = 'Загружает тестовые данные в базу данных'

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com', 'password': 'testpass123'}
        )
        if created:
            user.set_password('testpass123')
            user.save()

        regions_data = [
            {'name': 'Московская область', 'description': 'Центральный регион России'},
            {'name': 'Санкт-Петербург и Ленинградская область', 'description': 'Северо-Западный регион'},
            {'name': 'Краснодарский край', 'description': 'Южный регион России'},
            {'name': 'Свердловская область', 'description': 'Уральский регион'},
            {'name': 'Новосибирская область', 'description': 'Сибирский регион'},
            {'name': 'Республика Татарстан', 'description': 'Поволжский регион'},
        ]
        
        regions = []
        for data in regions_data:
            region, created = Region.objects.get_or_create(name=data['name'], defaults=data)
            regions.append(region)
            self.stdout.write(f'Создан регион: {region.name}')

        cities_data = [
            {'name': 'Москва', 'region': regions[0], 'population': 13000000, 'founded_year': 1147},
            {'name': 'Подольск', 'region': regions[0], 'population': 300000, 'founded_year': 1559},
            {'name': 'Санкт-Петербург', 'region': regions[1], 'population': 5600000, 'founded_year': 1703},
            {'name': 'Краснодар', 'region': regions[2], 'population': 1100000, 'founded_year': 1793},
            {'name': 'Сочи', 'region': regions[2], 'population': 500000, 'founded_year': 1838},
            {'name': 'Екатеринбург', 'region': regions[3], 'population': 1500000, 'founded_year': 1723},
            {'name': 'Новосибирск', 'region': regions[4], 'population': 1600000, 'founded_year': 1893},
            {'name': 'Казань', 'region': regions[5], 'population': 1300000, 'founded_year': 1005},
        ]
        
        cities = []
        for data in cities_data:
            city, created = City.objects.get_or_create(name=data['name'], defaults=data)
            cities.append(city)
            self.stdout.write(f'Создан город: {city.name}')

        words_data = [
            # Москва
            {'word': 'Тормозок', 'meaning': 'Еда, которую берут с собой на работу', 
             'example': 'Возьми тормозок, на работе поешь', 'city': cities[0]},
            {'word': 'Буханка', 'meaning': 'Автомобиль ВАЗ-2109', 
             'example': 'Приехал на своей буханке', 'city': cities[0]},
            {'word': 'Пакет', 'meaning': 'Полиэтиленовый мешок для продуктов', 
             'example': 'Купи пакет в магазине', 'city': cities[0]},
            
            # Подольск
            {'word': 'Курва', 'meaning': 'Непослушный ребенок', 
             'example': 'Эй ты, курва, иди сюда!', 'city': cities[1]},
            
            # Санкт-Петербург
            {'word': 'Поребрик', 'meaning': 'Бордюр, край тротуара', 
             'example': 'Не наступай на поребрик', 'city': cities[2]},
            {'word': 'Батон', 'meaning': 'Белый хлеб', 
             'example': 'Купи батон к ужину', 'city': cities[2]},
            {'word': 'Парадная', 'meaning': 'Подъезд дома', 
             'example': 'Встретимся в парадной', 'city': cities[2]},
            
            # Краснодар
            {'word': 'Шаньга', 'meaning': 'Пирожок с картошкой', 
             'example': 'Мама испекла шаньги', 'city': cities[3]},
            {'word': 'Кубанец', 'meaning': 'Житель Краснодарского края', 
             'example': 'Он настоящий кубанец', 'city': cities[3]},
            
            # Сочи
            {'word': 'Городошник', 'meaning': 'Любитель игры в городки', 
             'example': 'Дедушка был заядлым городошником', 'city': cities[4]},
            
            # Екатеринбург
            {'word': 'Уралец', 'meaning': 'Житель Урала', 
             'example': 'Суровый уралец не боится морозов', 'city': cities[5]},
            
            # Новосибирск
            {'word': 'Сибарь', 'meaning': 'Житель Сибири', 
             'example': 'Настоящий сибарь не боится морозов', 'city': cities[6]},
            {'word': 'Чё', 'meaning': 'Что', 
             'example': 'Чё сказал?', 'city': cities[6]},
            
            # Казань
            {'word': 'Эшләпә', 'meaning': 'Шапка-ушанка', 
             'example': 'Надень эшләпә, на улице холодно', 'city': cities[7]},
            {'word': 'Әйдә', 'meaning': 'Пойдем, давай', 
             'example': 'Әйдә в кино!', 'city': cities[7]},
        ]
        
        for data in words_data:
            word, created = Word.objects.get_or_create(
                word=data['word'],
                city=data['city'],
                defaults={
                    'meaning': data['meaning'],
                    'example': data.get('example', ''),
                    'user': user,
                    'views_count': random.randint(0, 100)
                }
            )
            if created:
                self.stdout.write(f'Добавлено слово: {word.word}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
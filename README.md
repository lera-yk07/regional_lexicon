# Региональная лексика России

Веб-сервис для сбора, анализа и сравнения уникальных слов и выражений из разных городов России. Платформа позволяет изучать языковое разнообразие регионов страны.

## Технологии
* **Python 3.10**
* **Django 4.2**
* **Pandas 2.0** - для анализа данных
* **Bootstrap 5.3** - для интерфейса
* **MySQL** - база данных на хостинге
* **SQLite** - база данных для разработки

## Инструкция
* На главной странице сайта есть форма "Добавить новое слово", в ней заполняем все поля: Слово или выражение, Значение, Пример использования, Город
* Для добавления слова нажимаем кнопку "Добавить слово"
* На сайте есть вкладки "Сравнить города" и "Статистика"

## Скриншоты
![Главная страница с каталогом слов](https://github.com/lera-yk07/regional_lexicon/blob/master/main.png)
![Страница сравнения лексики двух городов](https://github.com/lera-yk07/regional_lexicon/blob/master/comparison.png)
![Страница статистики с использованием Pandas](https://github.com/lera-yk07/regional_lexicon/blob/master/statistics.png)

## Архитектура проекта ✓
regional_lexicon/
├── lexicon/ 
│ ├── models.py
│ ├── views.py 
│ ├── forms.py 
│ └── urls.py 
├── templates/ 
├── static/ 
└── requirements.txt


## Как запустить проект локально

1. git clone https://github.com/ваш-юзернейм/regional-lexicon.git
2. python -m venv venv
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver

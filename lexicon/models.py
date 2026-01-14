from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Region(models.Model):
    """Регион (область, край, республика)"""
    name = models.CharField(max_length=100, verbose_name="Название региона")
    description = models.TextField(verbose_name="Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('region_detail', args=[str(self.id)])
    
    def word_count(self):
        return Word.objects.filter(city__region=self).count()

class City(models.Model):
    """Город в регионе"""
    name = models.CharField(max_length=100, verbose_name="Название города")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион", related_name='cities')
    population = models.IntegerField(verbose_name="Население", blank=True, null=True)
    founded_year = models.IntegerField(verbose_name="Год основания", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('city_detail', args=[str(self.id)])
    
    def word_count(self):
        return self.words.count()

class Word(models.Model):
    """Региональное слово или выражение"""
    word = models.CharField(max_length=100, verbose_name="Слово или выражение")
    meaning = models.TextField(verbose_name="Значение")
    example = models.TextField(verbose_name="Пример использования", blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name='words')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='words')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    
    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.word} ({self.city.name})"
    
    def get_absolute_url(self):
        return reverse('word_detail', args=[str(self.id)])

class Comparison(models.Model):
    """Сравнение лексики двух городов"""
    city1 = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Первый город", related_name='comparisons_as_city1')
    city2 = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Второй город", related_name='comparisons_as_city2')
    compared_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата сравнения")
    common_words_count = models.IntegerField(default=0, verbose_name="Количество общих слов")
    
    class Meta:
        verbose_name = "Сравнение"
        verbose_name_plural = "Сравнения"
        ordering = ['-compared_at']
    
    def __str__(self):
        return f"Сравнение {self.city1.name} и {self.city2.name}"
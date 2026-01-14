from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib import messages
import pandas as pd
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from .models import Word, City, Region
from .forms import WordForm, CustomUserCreationForm

def home(request):
    words_list = Word.objects.all().select_related('city', 'city__region', 'user')
    
    search_query = request.GET.get('search', '')
    if search_query:
        words_list = words_list.filter(
            Q(word__icontains=search_query) |
            Q(meaning__icontains=search_query) |
            Q(city__name__icontains=search_query) |
            Q(city__region__name__icontains=search_query)
        )
    
    city_filter = request.GET.get('city', '')
    if city_filter:
        words_list = words_list.filter(city_id=city_filter)
    
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['word', '-word', '-created_at', 'views_count', '-views_count']:
        words_list = words_list.order_by(sort_by)
    
    paginator = Paginator(words_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = WordForm() if request.user.is_authenticated else None
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
            word.save()
            messages.success(request, 'Слово успешно добавлено!')
            return redirect('home')
    
    regions_count = Region.objects.count()
    cities_count = City.objects.count()
    words_count = Word.objects.count()
    all_cities = City.objects.all()
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'regions_count': regions_count,
        'cities_count': cities_count,
        'words_count': words_count,
        'all_cities': all_cities,
        'search_query': search_query,
        'city_filter': city_filter,
        'sort_by': sort_by,
    }
    return render(request, 'lexicon/home.html', context)

def compare_cities(request):
    cities = City.objects.all().order_by('name')
    city1_id = request.GET.get('city1')
    city2_id = request.GET.get('city2')
    
    city1 = None
    city2 = None
    common_words = []
    unique_to_city1 = []
    unique_to_city2 = []
    
    if city1_id and city2_id and city1_id != city2_id:
        city1 = get_object_or_404(City, id=city1_id)
        city2 = get_object_or_404(City, id=city2_id)
        
        words_city1 = Word.objects.filter(city=city1)
        words_city2 = Word.objects.filter(city=city2)
        
        for word1 in words_city1:
            for word2 in words_city2:
                if word1.word.lower() == word2.word.lower():
                    common_words.append({
                        'word': word1.word,
                        'meaning1': word1.meaning,
                        'meaning2': word2.meaning,
                    })
        
        unique_to_city1 = words_city1.exclude(
            word__in=[w['word'] for w in common_words]
        )
        unique_to_city2 = words_city2.exclude(
            word__in=[w['word'] for w in common_words]
        )
    
    context = {
        'cities': cities,
        'city1': city1,
        'city2': city2,
        'common_words': common_words,
        'unique_to_city1': unique_to_city1,
        'unique_to_city2': unique_to_city2,
    }
    return render(request, 'lexicon/compare.html', context)

def statistics(request):
    words = Word.objects.all().values('word', 'city__name', 'city__region__name', 'views_count')
    df = pd.DataFrame(list(words))
    
    if df.empty:
        context = {'empty': True}
        return render(request, 'lexicon/statistics.html', context)
    
    region_stats = df.groupby('city__region__name').agg(
        words_count=('word', 'count'),
        total_views=('views_count', 'sum')
    ).reset_index()
    region_stats.columns = ['Регион', 'Количество слов', 'Всего просмотров']
    
    city_stats = df.groupby('city__name').agg(
        words_count=('word', 'count'),
        total_views=('views_count', 'sum')
    ).reset_index()
    city_stats.columns = ['Город', 'Количество слов', 'Всего просмотров']
    
    popular_words = df.nlargest(10, 'views_count')[['word', 'city__name', 'views_count']]
    popular_words.columns = ['Слово', 'Город', 'Просмотры']

    region_table = region_stats.to_html(
        index=False, 
        classes='table table-striped table-bordered',
        border=0
    )
    
    city_table = city_stats.to_html(
        index=False,
        classes='table table-striped table-bordered',
        border=0
    )
    
    popular_table = popular_words.to_html(
        index=False,
        classes='table table-striped table-bordered',
        border=0
    )
    
    context = {
        'empty': False,
        'region_table': region_table,
        'city_table': city_table,
        'popular_table': popular_table,
        'total_words': len(df),
        'total_regions': df['city__region__name'].nunique(),
        'total_cities': df['city__name'].nunique(),
    }
    return render(request, 'lexicon/statistics.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'lexicon/register.html', {'form': form})

def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    word.views_count += 1
    word.save()
    return render(request, 'lexicon/word_detail.html', {'word': word})

def city_detail(request, pk):
    city = get_object_or_404(City, pk=pk)
    words = city.words.all()
    return render(request, 'lexicon/city_detail.html', {
        'city': city,
        'words': words
    })

    def logout_view(request):
        auth_logout(request)
        return redirect('home')
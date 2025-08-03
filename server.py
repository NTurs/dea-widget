from flask import Flask, Response
import json
import random
from datetime import datetime
import os

app = Flask(__name__)

# Загружаем фразы из JSON файла
def load_phrases():
    """Загружает фразы из файла phrases.json"""
    try:
        # Проверяем, существует ли файл
        phrases_path = 'assets/phrases.json'
        if not os.path.exists(phrases_path):
            # Создаем файл с дефолтными фразами
            create_default_phrases(phrases_path)
        
        # Читаем файл с обработкой ошибок
        try:
            with open(phrases_path, 'r', encoding='utf-8') as file:
                phrases_dict = json.load(file)
        except FileNotFoundError:
            print(f"Файл {phrases_path} не найден")
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON в файле {phrases_path}: {e}")
            return None
        except UnicodeDecodeError as e:
            print(f"Ошибка кодировки в файле {phrases_path}: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при чтении файла {phrases_path}: {e}")
            return None
        
        # Проверяем структуру словаря
        if not isinstance(phrases_dict, dict):
            print(f"Файл {phrases_path} не содержит словарь")
            return None
        
        # Проверяем наличие необходимых ключей
        required_keys = ['утро', 'день', 'вечер', 'ночь', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье', 'общие']
        missing_keys = [key for key in required_keys if key not in phrases_dict]
        
        if missing_keys:
            print(f"В файле {phrases_path} отсутствуют ключи: {missing_keys}")
            # Возвращаем None, чтобы использовать fallback
            return None
        
        return phrases_dict
        
    except Exception as e:
        print(f"Критическая ошибка в load_phrases(): {e}")
        return None

def create_default_phrases(file_path):
    """Создает файл phrases.json с дефолтными фразами"""
    default_phrases = {
        "утро": ["Доброе утро ☀", "Начни с улыбки — и всё получится", "Утренняя энергия поможет справиться с задачами"],
        "день": ["Ты на правильном пути", "Обед — тоже успех", "Середина дня — время для новых достижений"],
        "вечер": ["Отдых — это тоже дело", "Сегодня ты была героиней", "Вечер — время для себя"],
        "ночь": ["Ночь — время для восстановления", "Хороший сон — залог успеха", "Отдыхай и набирайся сил"],
        "понедельник": ["Понедельник — день новых возможностей", "Начинаем неделю с позитивом"],
        "вторник": ["Вторник — время для продуктивной работы", "Впереди интересный день"],
        "среда": ["Среда — середина недели, но не середина жизни", "Середина недели — время подвести итоги"],
        "четверг": ["Четверг — почти выходные", "Завершаем рабочие дела"],
        "пятница": ["Пятница — день принятия себя", "Ты заслужила вечер с пледом и мечтой"],
        "суббота": ["Суббота — день отдыха и новых планов", "Выходной день для себя"],
        "воскресенье": ["Воскресенье — день для подготовки к новой неделе", "Последний день выходных"],
        "общие": [
            "Ты справляешься. Даже если кажется, что нет.",
            "Маленький шаг — тоже шаг.",
            "Ты важна. Просто потому что ты есть.",
            "Сделай глоток воды. Продолжим.",
            "Иногда вдох — уже победа.",
            "Ты не обязана быть сильной всё время.",
            "Смотри, сколько уже пройдено. Ты можешь ещё.",
            "Ты — не ошибка. Ты — возможность.",
            "Сейчас трудно, но ты не одна.",
            "Пусть мир подождёт. Сейчас ты."
        ]
    }
    
    # Создаем директорию, если её нет
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(default_phrases, file, ensure_ascii=False, indent=2)
    
    print(f"Создан файл с дефолтными фразами: {file_path}")

def get_time_of_day():
    """Определяет время суток по текущему часу"""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return 'утро'
    elif 12 <= hour < 18:
        return 'день'
    elif 18 <= hour < 23:
        return 'вечер'
    else:
        return 'ночь'

def get_day_of_week():
    """Определяет день недели по номеру (1-7)"""
    weekday = datetime.now().weekday()  # 0-6 (понедельник = 0)
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return days[weekday]

def get_time_context():
    """Возвращает контекст времени: время суток и день недели"""
    hour = datetime.now().hour
    weekday = datetime.now().weekday()  # 0-6 (понедельник = 0)
    
    # Определяем время суток
    if 6 <= hour < 12:
        time_of_day = 'утро'
    elif 12 <= hour < 18:
        time_of_day = 'день'
    elif 18 <= hour < 22:
        time_of_day = 'вечер'
    else:
        time_of_day = 'ночь'
    
    # Определяем день недели
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    weekday_name = days[weekday]
    
    return time_of_day, weekday_name

def get_random_phrase():
    """Получает случайную фразу на основе текущего времени и дня недели"""
    phrases = load_phrases()
    if not phrases:
        return "Ты справляешься. Я рядом."
    
    # Определяем текущее время суток и день недели
    time_of_day = get_time_of_day()
    day_of_week = get_day_of_week()
    
    try:
        # Проверяем, есть ли раздел "общие" и выбираем с вероятностью 30%
        if ("общие" in phrases and 
            isinstance(phrases["общие"], list) and 
            phrases["общие"] and
            random.random() < 0.3):  # 30% вероятность
            
            # Выбираем только универсальную фразу
            return random.choice(phrases["общие"])
            
        else:
            # Выбираем фразы по времени суток и дню недели
            time_phrase = ""
            day_phrase = ""
            
            # Получаем фразу по времени суток
            if time_of_day in phrases and phrases[time_of_day]:
                time_phrase = random.choice(phrases[time_of_day])
            
            # Получаем фразу по дню недели
            if day_of_week in phrases and phrases[day_of_week]:
                day_phrase = random.choice(phrases[day_of_week])
            
            # Объединяем фразы
            if time_phrase and day_phrase:
                return f"{time_phrase} {day_phrase}"
            elif time_phrase:
                return time_phrase
            elif day_phrase:
                return day_phrase
            else:
                return "Ты справляешься. Я рядом."
            
    except Exception as e:
        print(f"Ошибка получения фраз: {e}")
        return "Ты справляешься. Я рядом."

@app.route('/get_phrase', methods=['GET'])
def get_phrase():
    """API endpoint для получения случайной фразы"""
    # 1. Загружаем словарь фраз
    phrases_dict = load_phrases()
    
    # 2. Определяем время суток и день недели
    time_of_day, weekday = get_time_context()
    
    try:
        # Проверяем, есть ли раздел "общие" и выбираем с вероятностью 30%
        if (phrases_dict and 
            "общие" in phrases_dict and 
            isinstance(phrases_dict["общие"], list) and 
            phrases_dict["общие"] and
            random.random() < 0.3):  # 30% вероятность
            
            # Выбираем только универсальную фразу
            final_phrase = random.choice(phrases_dict["общие"])
            
        else:
            # Выбираем фразы по времени суток и дню недели
            time_phrase = ""
            day_phrase = ""
            
            # Выбираем фразу по времени суток
            if (phrases_dict and 
                time_of_day in phrases_dict and 
                isinstance(phrases_dict[time_of_day], list) and 
                phrases_dict[time_of_day]):
                time_phrase = random.choice(phrases_dict[time_of_day])
            
            # Выбираем фразу по дню недели
            if (phrases_dict and 
                weekday in phrases_dict and 
                isinstance(phrases_dict[weekday], list) and 
                phrases_dict[weekday]):
                day_phrase = random.choice(phrases_dict[weekday])
            
            # Объединяем фразы
            if time_phrase and day_phrase:
                final_phrase = f"{time_phrase} {day_phrase}"
            elif time_phrase:
                final_phrase = time_phrase
            elif day_phrase:
                final_phrase = day_phrase
            else:
                # Fallback если фразы не найдены
                final_phrase = "Ты справляешься. Я рядом."
            
    except Exception as e:
        print(f"Ошибка получения фраз: {e}")
        final_phrase = "Ты справляешься. Я рядом."
    
    # 3. Возвращаем результат как JSON
    return Response(json.dumps({"phrase": final_phrase}, ensure_ascii=False), content_type="application/json")

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return Response(json.dumps({"status": "ok", "message": "Сервер работает"}, ensure_ascii=False), content_type="application/json")

if __name__ == '__main__':
    print("Запуск Flask-сервера для DeA Widget...")
    print("API доступен по адресу: http://localhost:5000/get_phrase")
    print("Для остановки сервера нажмите Ctrl+C")
    
    # Запускаем сервер в режиме разработки
    app.run(
        host='0.0.0.0',  # Доступен для всех интерфейсов
        port=5000,       # Порт 5000
        debug=True,      # Режим отладки
        threaded=True    # Поддержка многопоточности
    ) 
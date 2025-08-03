#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from server import load_phrases, get_time_context

def test_error_handling():
    """Тестирует обработку ошибок в load_phrases()"""
    
    print("🧪 Тестирование обработки ошибок...")
    
    # Тест 1: Нормальная загрузка
    print("\n1. Тест нормальной загрузки:")
    phrases = load_phrases()
    if phrases:
        print("✅ Файл загружен успешно")
        print(f"   Ключи: {list(phrases.keys())}")
    else:
        print("❌ Ошибка загрузки файла")
    
    # Тест 2: Проверка get_time_context
    print("\n2. Тест get_time_context:")
    try:
        time_of_day, weekday = get_time_context()
        print(f"✅ Время суток: {time_of_day}")
        print(f"   День недели: {weekday}")
    except Exception as e:
        print(f"❌ Ошибка get_time_context: {e}")
    
    # Тест 3: Проверка наличия ключей в словаре
    print("\n3. Проверка ключей в словаре:")
    if phrases:
        required_keys = ['утро', 'день', 'вечер', 'ночь', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        missing_keys = [key for key in required_keys if key not in phrases]
        if missing_keys:
            print(f"❌ Отсутствуют ключи: {missing_keys}")
        else:
            print("✅ Все необходимые ключи присутствуют")
    else:
        print("❌ Словарь не загружен")

if __name__ == "__main__":
    test_error_handling() 
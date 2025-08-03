#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_get_phrase():
    """Тестирует обновленный маршрут /get_phrase"""
    try:
        # Тест get_phrase endpoint
        response = requests.get('http://localhost:5000/get_phrase')
        result = response.json()
        
        print("✅ Маршрут /get_phrase работает!")
        print(f"Полученная фраза: {result['phrase']}")
        
        # Проверяем структуру ответа
        if 'phrase' in result and isinstance(result['phrase'], str):
            print("✅ Структура ответа корректна")
        else:
            print("❌ Неправильная структура ответа")
            
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не запущен. Запустите server.py")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_get_phrase() 
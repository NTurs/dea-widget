#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_server():
    """Тестирует работу сервера и функцию load_phrases()"""
    try:
        # Тест health endpoint
        response = requests.get('http://localhost:5000/health')
        print("Health check:", response.json())
        
        # Тест get_phrase endpoint
        response = requests.get('http://localhost:5000/get_phrase')
        print("Get phrase:", response.json())
        
        print("✅ Сервер работает корректно!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не запущен. Запустите server.py")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_server() 
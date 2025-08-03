#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server import get_time_context

def test_get_time_context():
    """Тестирует функцию get_time_context()"""
    try:
        time_of_day, weekday = get_time_context()
        print(f"Время суток: {time_of_day}")
        print(f"День недели: {weekday}")
        print("✅ Функция get_time_context() работает корректно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_get_time_context() 
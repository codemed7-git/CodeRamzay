"""
Модуль шифрования сообщений по алгоритму Рамзая.
"""
import transliteration
import utils
from typing import Dict


def encryption(text: str, key: str) -> str:
    if not key:
        raise ValueError("Ключ шифрования не может быть пустым")
    
    if not text:
        return ""
    
    # Получаем уникальный ключ
    unique_key = utils.get_unique_key(key.lower())
    
    if not unique_key:
        raise ValueError("Ключ должен содержать хотя бы один символ")
    
    # Транслитерация кириллицы в латиницу
    text = transliteration.transliteration(text.lower())
    
    # Замена пробелов на '/'
    text = text.replace(' ', '/')
    
    # Создание матрицы шифрования
    matrix = utils.create_encryption_matrix(unique_key)
    
    # Создание словаря кодирования
    dict_encryption = utils.create_encryption_dict(matrix)
    
    # Создание обратного словаря для быстрого поиска
    reverse_dict = {v: k for k, v in dict_encryption.items() if v}
    
    # Формирование КЛЕРА (цифрового кода текста)
    kler_parts = []
    for char in text:
        if char in reverse_dict:
            kler_parts.append(str(reverse_dict[char]))
        else:
            continue
    
    # Клер без пробелов для шифрования
    kler_without_space = ''.join(kler_parts)
    
    if not kler_without_space:
        raise ValueError("Не удалось закодировать сообщение. Проверьте входные данные.")
    
    # Расширение гаммы до нужной длины
    gamma = utils.extend_gamma(len(kler_without_space))
    
    # Формирование шифра путем сложения гаммы и клера по модулю 10
    encryption_result = []
    for i in range(len(kler_without_space)):
        digit = (int(kler_without_space[i]) + int(gamma[i])) % 10
        encryption_result.append(str(digit))
    
    return ''.join(encryption_result)
"""
Утилиты для шифра Рамзая - общие функции для шифрования и расшифровки.
"""
from math import ceil
from typing import Dict, List, Tuple

# Константы
ALPHABET_SIZE = 28  # Размер алфавита (26 букв + '/' + '.')
KEY_PHRASE = 'asintoer'  # Анаграмма для кодирования частых символов
ENGLISH_ALPHABET = 'abcdefghijklmnopqrstuvwxyz/.'
PHRASE_START_CODE = 0  # Начальный код для букв из ключевой фразы
PHRASE_END_CODE = 7  # Конечный код для букв из ключевой фразы
OTHER_START_CODE = 80  # Начальный код для остальных букв
OTHER_END_CODE = 99  # Конечный код для остальных букв

# Гамма из справочника 1935 года
GAMMA = ('35635513032493210010781911210621169418617614733091929566220180615112841121386586318091506521343724383992'
         '72733434692432287649732563703537247157737397393033434692322876497325679732563703035372471577373930623819'
         '54334940802573112183802196397625146871395205073121441593153561866950268851101313184965923111443412811779'
         '55412601001471471134480480113771891018393726601245052856424688553144059126188431338494554335274937592565')


def get_unique_key(key: str) -> str:
    unique_chars = []
    seen = set()
    for char in key:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    return ''.join(unique_chars)


def create_encryption_matrix(key: str) -> List[List[str]]:
    eng_dict = ENGLISH_ALPHABET
    matrix = [['*' for _ in range(len(key))] for _ in range(ceil(ALPHABET_SIZE / len(key)))]
    
    # Заполнение первой строки ключом
    remaining_chars = list(eng_dict)
    for ind, char in enumerate(key):
        if char in remaining_chars:
            remaining_chars.remove(char)
        matrix[0][ind] = char
    
    # Заполнение таблицы оставшимися элементами
    char_index = 0
    for i in range(1, len(matrix)):
        for j in range(len(key)):
            if char_index >= len(remaining_chars):
                break
            matrix[i][j] = remaining_chars[char_index]
            char_index += 1
    
    return matrix


def create_encryption_dict(matrix: List[List[str]]) -> Dict[int, str]:
    encryption_dict = {}
    
    # Инициализация словаря
    for code in range(PHRASE_START_CODE, PHRASE_END_CODE + 1):
        encryption_dict[code] = ''
    for code in range(OTHER_START_CODE, OTHER_END_CODE + 1):
        encryption_dict[code] = ''
    
    # Заполнение словаря
    phrase_chars = list(KEY_PHRASE)
    phrase_index = PHRASE_START_CODE
    other_index = OTHER_START_CODE
    
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            char = matrix[row][col]
            if char != '*':
                # Проверяем, есть ли символ в ключевой фразе и еще не использован
                if char in phrase_chars:
                    encryption_dict[phrase_index] = char
                    phrase_chars.remove(char)  # Удаляем использованный символ
                    phrase_index += 1
                else:
                    if other_index <= OTHER_END_CODE:
                        encryption_dict[other_index] = char
                        other_index += 1
    
    return encryption_dict


def extend_gamma(length: int) -> str:
    if length <= len(GAMMA):
        return GAMMA[:length]
    
    repetitions = (length // len(GAMMA)) + 1
    extended = GAMMA * repetitions
    return extended[:length]


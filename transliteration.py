"""
Модуль транслитерации кириллицы в латиницу и обратно.
"""
from typing import Dict


def transliteration(rus_text: str) -> str:
    dict_trasl: Dict[str, str] = {
        'ё': 'jo', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shh', 'ъ': '*', 'ы': 'y', 'ь': "'",
        'э': 'je', 'ю': 'ju', 'я': 'ya'
    }

    nums: Dict[int, str] = {
        0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре',
        5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'
    }

    processed_text = rus_text
    for digit in sorted(nums.keys(), reverse=True):
        word = nums[digit]
        processed_text = processed_text.replace(str(digit), word)

    # Транслитерируем текст
    eng_text = ''
    for char in processed_text:
        if char.lower() in dict_trasl:
            eng_text += dict_trasl[char.lower()]
        else:
            eng_text += char

    return eng_text


def de_transliteration(text: str) -> str:
    dict_de_trasl: Dict[str, str] = {
        'jo': 'ё', 'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д',
        'e': 'е', 'zh': 'ж', 'z': 'з', 'i': 'и', 'j': 'й', 'k': 'к',
        'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р',
        's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'c': 'ц',
        'ch': 'ч', 'sh': 'ш', 'shh': 'щ', 'y': 'ы', 'je': 'э',
        'ju': 'ю', 'ya': 'я', '*': 'ъ', "'": 'ь'
    }

    nums: Dict[int, str] = {
        0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре',
        5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'
    }

    list_sym = sorted(dict_de_trasl.keys(), key=lambda x: (-len(x), x))

    result_letters = []
    i = 0
    while i < len(text):
        matched = False
        if i < len(text) and text[i] == "'" and "'" in dict_de_trasl:
            result_letters.append(dict_de_trasl["'"])
            i += 1
            continue
        for sym in list_sym:
            if i + len(sym) <= len(text):
                if len(sym) > 1:
                    if text[i:i+len(sym)] == sym:
                        result_letters.append(dict_de_trasl[sym])
                        i += len(sym)
                        matched = True
                        break
                elif text[i] == sym:
                    result_letters.append(dict_de_trasl[sym])
                    i += 1
                    matched = True
                    break
        if not matched:
            result_letters.append(text[i])
            i += 1

    processed_text = ''.join(result_letters)

    sorted_nums = sorted(nums.items(), key=lambda x: (-len(x[1]), -x[0]))

    result = []
    i = 0
    while i < len(processed_text):
        matched = False
        for digit, word in sorted_nums:
            if processed_text[i:].startswith(word):
                result.append(str(digit))
                i += len(word)
                matched = True
                break
        if not matched:
            result.append(processed_text[i])
            i += 1

    processed_text = ''.join(result)

    return processed_text
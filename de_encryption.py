"""
Модуль расшифровки сообщений по алгоритму Рамзая.
"""
import transliteration
import utils


def de_encryption(encryption: str, key: str) -> str:
    if not key:
        raise ValueError("Ключ шифрования не может быть пустым")
    
    if not encryption:
        return ""

    if not encryption.isdigit():
        raise ValueError("Шифрограмма должна содержать только цифры")
    
    # Получаем уникальный ключ
    unique_key = utils.get_unique_key(key.lower())
    
    if not unique_key:
        raise ValueError("Ключ должен содержать хотя бы один символ")
    
    # Создание матрицы шифрования (та же, что при шифровании)
    matrix = utils.create_encryption_matrix(unique_key)
    
    # Создание словаря кодирования (тот же, что при шифровании)
    dict_encryption = utils.create_encryption_dict(matrix)
    
    # Расширение гаммы до нужной длины
    gamma = utils.extend_gamma(len(encryption))
    
    # Вычисление КЛЕРА путем вычитания из ШИФРА ГАММЫ по модулю 10
    kler = []
    for i in range(len(encryption)):
        digit = (int(encryption[i]) - int(gamma[i])) % 10
        kler.append(str(digit))
    
    kler_str = ''.join(kler)

    sorted_codes = sorted(dict_encryption.keys(), key=lambda x: (len(str(x)), -x), reverse=True)

    result = []
    i = 0
    while i < len(kler_str):
        matched = False
        # Пытаемся найти совпадение с самым длинным кодом
        for code in sorted_codes:
            char = dict_encryption[code]
            if not char:  # Пропускаем пустые значения
                continue
            code_str = str(code)
            # Проверяем, начинается ли строка с этого кода
            if kler_str[i:].startswith(code_str):
                result.append(char)
                i += len(code_str)
                matched = True
                break
        if not matched:
            # Если не нашли совпадение, пропускаем символ (не должно происходить)
            i += 1
    
    kler_str = ''.join(result)
    
    # Замена '/' на пробелы
    de_encryption_text = kler_str.replace('/', ' ')
    
    # Детранслитерация латиницы обратно в кириллицу
    de_encryption_message = transliteration.de_transliteration(de_encryption_text)
    
    return de_encryption_message
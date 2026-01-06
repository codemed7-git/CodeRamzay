"""
Основной модуль для работы с шифром Рамзая.
"""
import encryption
import de_encryption


def validate_message(message: str) -> bool:
    if not message:
        return False
    
    # Разрешенные символы: кириллица, латиница, цифры, точка, пробелы
    allowed_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
                       'abcdefghijklmnopqrstuvwxyz '
                       '0123456789.')
    
    message_lower = message.lower()
    return all(char in allowed_chars for char in message_lower)


def validate_key(key: str) -> bool:
    if not key:
        return False
    
    # Ключ должен содержать только буквы латиницы
    key_lower = key.lower()
    return key_lower.isalpha() and all(char in 'abcdefghijklmnopqrstuvwxyz' for char in key_lower)


def main():
    print("=" * 100)
    print("Шифр Рамзая - Система шифрования сообщений")
    print("=" * 100)
    print()
    
    # Принимаем сообщение и ключ
    while True:
        message = input('Введите сообщение (кириллица, цифры, точка, пробелы): ').strip()
        if validate_message(message):
            break
        print("Ошибка: Сообщение содержит недопустимые символы. "
              "Используйте только кириллицу, латиницу, цифры, точку и пробелы.")
    
    while True:
        key_encryption = input('Введите ключ шифрования (только латинские буквы): ').strip().lower()
        if validate_key(key_encryption):
            break
        print("Ошибка: Ключ должен содержать только латинские буквы и не может быть пустым.")
    
    print()
    print("Обработка...")
    print()
    
    try:
        # ШИФРУЕМ
        encryption_message = encryption.encryption(message, key_encryption)
        
        # РАСШИФРОВЫВАЕМ
        de_encryption_message = de_encryption.de_encryption(encryption_message, key_encryption)
        
        # Выводим результаты
        print("=" * 100)
        print(f'Шифрограмма: {encryption_message}')
        print(f'Дешифрограмма (проверка): {de_encryption_message}')
        print("=" * 100)
        
        # Проверка корректности расшифровки
        if message.lower() == de_encryption_message.lower():
            print("Расшифровка выполнена успешно!")
        else:
            print("Расшифрованное сообщение не совпадает с исходным!")
            print(f"   Исходное: {message}")
            print(f"   Расшифрованное: {de_encryption_message}")
            
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
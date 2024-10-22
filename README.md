![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)    

# Перед началом использования
Запустите скрипт *create_db.py* для создания sqlite базы данных.

Вставьте токен своего бота в *main.py*, *buy_screener.py*, *sell_screener.py*

# Алгоритм работы
Выберите один из 12 предложенных токенов

Укажите процент изменения цены токена для его покупки и продажи

Ожидайте (цена проверяется по API Bybit и сравнивается с ценой с учетом указанного
вами процента). Вам автоматически придут уведомления, когда токены будут куплены/проданы.

Проверяйте статус ваших заказов кнопкой **"Профиль"**.


### Схема работы проверки цены находятся в файлах *buy_screener.py* и *sell_screener.py*
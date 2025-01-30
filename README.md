# IMEI_CHECKER
### Описание
Пользователь отправляет сообщение с IMEI Телеграмм боту. Бот проверяет IMEI на валидность и делает запрос к API Django. Django делает запрос к внешнему сервису (https://imeicheck.net/) и возвращает результат пользователю через бота.

### **Начало работы**
Клонируйте репозиторий и перейдите в него в командной строке:

```bash
git clone git@github.com:LGaben/Megamarket-Parser.git
```


Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Создайте .env по примеру из .env.example


### Запуск бота и локального сервера Django
```bash
python manage.py runserver
python manage.py runbot
```


### Автор проекта

**Филин Иван.**
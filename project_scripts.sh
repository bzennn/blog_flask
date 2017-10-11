#!/bin/bash

echo "Выберите команду:";
echo "    1. Инициализировать";
echo "    2. Сделать миграцию";
echo "    3. Откатить";
echo "    4. Обновить";
echo "    5. Создать Базу Данных";
echo "    6. Удалить Базу Данных";
echo "    7. Создать пользователя admin";
echo "    8. Запустить Python";
echo "    9. Запустить приложение(debug)";
echo "    10. Запустить приложение(production)";

read var

case $var in
    "1") exec python/bin/flask db init;;
    "2") exec python/bin/flask db migrate;;
    "3") exec python/bin/flask db downgrade;;
    "4") exec python/bin/flask db upgrade;;
    "5") exec ./db_create.py;;
    "6") exec rm tmp/app.db
	 echo "Database successfully deleted.";;
    "7") exec ./create_admin_user.py;;
    "8") exec python/bin/python;;
    "9") exec ./run.py;;
    "10") exec ./runp.py;;
esac


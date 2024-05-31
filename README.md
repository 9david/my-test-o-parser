# my-test-o-parser

> ## **Для запуска проекта нужно сделать следующие шаги**

<span class="l"> Для смены пользователя на своего раскоментируйте три строчки в файле docker-compose.yaml в сервисе "django", там где начинается строка "user" и отредактируйте файл ".env". По умолчанию запускать проект будет root.</span>

<span class="l"> **1.** В Docker-compose.yaml установить свои переменные bot_token и chat_id.</span>

<span class="l"> **1.1** Token можно получить, создав бота у Bot_Father, также у него нужно создать команду "/spisok_tovarov"</span>

<span class="l"> **1.2** Chat_id можно получить у бота, набираем в поисковике телеграмма "userinfobot", вводим "/start". </span>

<span class="l"> **2** В директории с файлом docker-compose.yaml вводим следующую команду:</span>

<span class="l"> **docker-compose run --rm django sh -c "python manage.py makemigrations && python manage.py collectstatic"**</span>

<span class="l"> **3** Открываем три терминала:</span>

<span class="l"> **3.1** В первом запускаем **docker-compose up**</span>

<span class="l"> **3.2** Во втором **docker-compose run --rm django sh -c "celery -A app worker --loglevel=info"**</span>

<span class="l"> **3.3** В третьем **docker-compose run --rm django sh -c "python manage.py run_telegram_bot"**</span>

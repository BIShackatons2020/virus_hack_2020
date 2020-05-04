# Virus Hack 2020
Использовался Python 3.8.2

Установить зависимости:

    pip install -r requirements.txt

Установить переменные окружения:
Windows:

    set FOLDER_ID=<folder>
    set IAM_TOKEN=<i am token>
    
Linux:

    FOLDER_ID=<folder>
    IAM_TOKEN=<i am token>

Как получить i'm токен:
https://cloud.yandex.ru/docs/iam/operations/iam-token/create

Запустить:

    python main.py

После этого можно открыть audio_recognition_test.html и
попробовать распознать свой голос, чтобы убедиться, 
что все работает как нужно

Если запускать на Linux based системах нужно будет поставить
эту утилиту:
https://www.ffmpeg.org/
На Windows может понадобиться подложить другой exe 
файлик этой утилиты, если у вас необычная архитектура


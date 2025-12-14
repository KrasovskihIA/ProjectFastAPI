# Проект Погоды (Weather App)

Этот проект состоит из бэкенда на FastAPI и фронтенда на Vue.js для отображения прогноза погоды.
Проект создан для работы с внешним API [OpenWeatherMap](https://openweathermap.org/api#current).

## Структура проекта

- `backend/`: Приложение FastAPI, обрабатывающее запросы данных о погоде.
- `frontend/`: Приложение Vue.js, использующее Vite и Axios.

## Функционал

- **Текущая погода**: Просмотр текущих погодных условий для указанного города.
- **Прогноз на 5 дней**: Просмотр прогноза погоды на следующие 5 дней.

## Получение ключа API для Weather API

Для работы проекта необходим ключ API от OpenWeatherMap. Следуйте инструкции для его получения:

1.  Зарегистрируйтесь или войдите в аккаунт на сайте [OpenWeatherMap](https://openweathermap.org/).
2.  Перейдите на страницу [ваших API ключей](https://home.openweathermap.org/api_keys).
3.  Создайте новый ключ (кнопка "Generate") или используйте существующий `Default` ключ.
4.  Скопируйте полученный ключ.
5.  Вставьте этот ключ в файл `.env` в корне проекта (или в `backend/.env` если используется только бэкенд), присвоив его переменной `API_KEY`.

## Начало работы

### Предварительные требования

- Python 3.8+
- Node.js 16+ (для фронтенда)

### Настройка бэкенда

1. Перейдите в корневую директорию проекта.
2. Создайте виртуальное окружение и установите зависимости (если еще не сделано).
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   *(Примечание: Убедитесь, что `requirements.txt` включает `fastapi`, `uvicorn`, `httpx`, `python-dotenv`)*

3. Создайте файл `.env` в папке `backend/`, если это требуется для API ключей.
4. Запустите сервер бэкенда:
   ```bash
   uvicorn backend.main:app --reload
   ```
   Бэкенд будет запущен по адресу `http://127.0.0.1:8000`.

   **Эндпоинты:**
   - `GET /weather?city={city_name}`: Получить текущую погоду.
   - `GET /five_days?city={city_name}`: Получить прогноз на 5 дней.
   - Документация доступна по адресу `http://127.0.0.1:8000/docs`.

### Настройка фронтенда

1. Перейдите в директорию `frontend`:
   ```bash
   cd frontend
   ```
2. Установите зависимости:
   ```bash
   npm install
   ```
3. Запустите сервер разработки:
   ```bash
   npm run dev
   ```
   Фронтенд будет доступен по адресу `http://localhost:5173`.

### Конфигурация

- **URL Бэкенда**: Фронтенд настроен на проксирование запросов `/api` на `http://127.0.0.1:8000` через `vite.config.js`. Если вы разворачиваете приложения раздельно, обновите `API_BASE` в `src/App.vue`.

## Руководство по деплою на сервер (Ubuntu/Debian)

В этом руководстве описан процесс развертывания приложений (Backend + Frontend) на Linux сервере с использованием Nginx в качестве обратного прокси.

### 1. Подготовка сервера

Обновите пакеты и установите необходимые инструменты:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx curl git -y
```

### 2. Настройка Backend (FastAPI)

1.  **Клонируйте репозиторий** в директорию `/var/www/weather-app` (или любую другую):
    ```bash
    mkdir -p /var/www/weather-app
    cd /var/www/weather-app
    # git clone <repository_url> . 
    # Предполагается что файлы уже на сервере
    ```

2.  **Настройте виртуальное окружение**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn
    ```

3.  **Создайте .env файл**:
    ```bash
    cp .env.example .env # Если есть пример
    nano backend/.env
    # Добавьте API_KEY=вашего_ключа
    ```

4.  **Создайте Systemd сервис** для автозапуска бэкенда:
    Создайте файл `/etc/systemd/system/weather-backend.service`:
    ```ini
    [Unit]
    Description=Gunicorn instance to serve Weather App Backend
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/var/www/weather-app
    Environment="PATH=/var/www/weather-app/venv/bin"
    ExecStart=/var/www/weather-app/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 127.0.0.1:8000

    [Install]
    WantedBy=multi-user.target
    ```

5.  **Запустите сервис**:
    ```bash
    sudo systemctl start weather-backend
    sudo systemctl enable weather-backend
    ```

### 3. Настройка Frontend (Vue.js)

1.  **Установите Node.js** (если не установлен):
    ```bash
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ```

2.  **Соберите проект**:
    Перейдите в папку фронтенда и создайте билд.
    ```bash
    cd frontend
    npm install
    # Создайте .env с URL продакшн бэкенда, если они на разных хостах, 
    # но в нашей конфигурации мы будем использовать проксирование Nginx.
    npm run build
    ```
    Результат сборки появится в папке `frontend/dist`.

### 4. Настройка Nginx

Настроим Nginx для раздачи статики (Frontend) и проксирования API запросов на Backend.

1.  Создайте конфиг `/etc/nginx/sites-available/weather-app`:
    ```nginx
    server {
        listen 80;
        server_name your_domain_or_ip;

        # Frontend (Static files)
        location / {
            root /var/www/weather-app/frontend/dist;
            index index.html;
            try_files $uri $uri/ /index.html;
        }

        # Backend (API Proxy)
        location /api/ {
            proxy_pass http://127.0.0.1:8000/; # Обратите внимание на слэш в конце
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

2.  **Активируйте сайт и перезапустите Nginx**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/weather-app /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

Теперь ваше приложение должно быть доступно по IP адресу или домену сервера.

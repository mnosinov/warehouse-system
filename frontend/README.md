# Frontend (React + Vite)

- стек (Vite, React Router)
- QR сканер с камеры
- JWT аутентификация
- HTTPS настройка для мобильного доступа


### Фронтенд (React микрофронт)
```text
frontend/
├── public/
├── src/
│   ├── components/      # React компоненты
│   ├── pages/          # Страницы
│   ├── services/       # API вызовы
│   └── utils/          # JWT, QR сканирование
```

## Быстрый старт

### Frontend
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --force
```


## .env файл - в корне backend
```
VITE_API_BASE_URL=https://<backend server ip or domain address>:8000
```

---

# 📄 ТЗ — MonkeyType Clone (Frontend + Backend)

## 🎯 Цель

Сделать сервис проверки скорости печати текста с поддержкой гостей и авторизованных пользователей, системой хранения результатов и глобальным **Leaderboard**.

---

## 👥 Типы пользователей

1. **Гость**

   * Может проходить тесты печати.
   * Результаты **не сохраняются**.

2. **Авторизованный пользователь**

   * Авторизация через **JWT**.
   * Альтернативный вход через **Google OAuth2**.
   * Его результаты сохраняются (WPM, Accuracy, время).
   * Есть доступ к профилю и **лидерборду**.

---

## 🛠 Backend (Django + DRF)

### 📌 Модели

1. **User**

   * username, email, password
   * auth\_type (local / google)
   * best\_wpm, average\_accuracy (кэш для быстрого leaderboard).

2. **Word**

   * text (строка, слово)
   * language (например, `en`, `ru`).

3. **TestResult**

   * user (nullable → если гость, то null).
   * wpm (Words Per Minute).
   * accuracy (%).
   * time\_seconds (30 или 60).
   * created\_at.

---

### 📌 API эндпоинты

* **Auth**

  * `POST /api/auth/register/` — регистрация (JWT).
  * `POST /api/auth/login/` — логин (JWT).
  * `POST /api/auth/google/` — вход через Google OAuth2.
  * `POST /api/auth/refresh/` — обновление токена.

* **Typing Test**

  * `GET /api/words/?lang=en&count=50` — получить список слов.
  * `POST /api/test-results/` — сохранить результат (только для авторизованных).
  * `GET /api/test-results/me/` — история моих результатов.

* **Leaderboard**

  * `GET /api/leaderboard/?period=daily|weekly|all` — рейтинг лучших игроков.

---

## 🎨 Frontend (React + Tailwind)

### Страницы

1. **Главная** — кнопка "Начать тест".
2. **Typing Test**

   * отображение текста, подсветка ошибок.
   * выбор режима: 30 или 60 секунд.
   * после окончания — результат (WPM, Accuracy).
3. **Профиль** (для авторизованных)

   * история тестов.
   * лучший результат.
4. **Leaderboard**

   * список топ игроков по WPM.
5. **Login / Register**

   * JWT авторизация.
   * кнопка "Войти через Google".

---

## 📦 Технологии

* **Backend**: Django 5, DRF, PostgreSQL, SimpleJWT, dj-rest-auth (Google OAuth).
* **Frontend**: React, TailwindCSS, Axios.
* **DevOps**: Docker + docker-compose (frontend, backend, db).

---


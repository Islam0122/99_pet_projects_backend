Tailwind CSS 

1. Что такое Tailwind CSS

Tailwind CSS — это utility-first CSS-фреймворк. Вместо готовых компонентов ты используешь маленькие CSS-классы прямо в HTML/JSX.

Идея:

❌ .card {} в CSS

✅ class="p-4 bg-white rounded-xl shadow"


Плюсы:

Быстро

Нет конфликтов классов

Отлично масштабируется

Идеален для React / Next / Vue



---

2. Установка (классика)

npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

tailwind.config.js

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
}

index.css

@tailwind base;
@tailwind components;
@tailwind utilities;


---

3. Layout (основа)

Flex

<div class="flex items-center justify-between"></div>

flex-row, flex-col

items-center (по Y)

justify-center (по X)


Grid

<div class="grid grid-cols-3 gap-4"></div>


---

4. Отступы и размеры

Padding / Margin

p-4, px-6, py-2

m-4, mt-2, mb-6


Width / Height

w-full, h-screen

max-w-md, min-h-screen



---

5. Цвета

<div class="bg-blue-500 text-white"></div>

bg-* — фон

text-* — текст

border-*


Оттенки: 50 → 900


---

6. Типографика

<p class="text-lg font-semibold leading-relaxed"></p>

text-sm | base | lg | xl | 2xl

font-light | normal | bold

tracking-wide



---

7. Border и Shadow

<div class="rounded-xl border shadow-md"></div>

rounded, rounded-lg, rounded-full

shadow-sm | md | xl | 2xl



---

8. Hover / Focus / Active

<button class="bg-blue-500 hover:bg-blue-600 focus:ring-2"></button>

Псевдоклассы:

hover:

focus:

active:

disabled:



---

9. Адаптивность (ОЧЕНЬ ВАЖНО)

<div class="p-2 md:p-6 lg:p-10"></div>

Брейкпоинты:

sm ≥ 640px

md ≥ 768px

lg ≥ 1024px

xl ≥ 1280px



---

10. Position

<div class="relative">
  <span class="absolute top-2 right-2"></span>
</div>

relative

absolute

fixed

sticky



---

11. Overflow и Scroll

overflow-hidden

overflow-y-auto

scroll-smooth



---

12. Animations

<div class="animate-pulse"></div>

animate-spin

animate-bounce

animate-ping



---

13. Кастомизация (extend)

theme: {
  extend: {
    colors: {
      brand: '#6366f1'
    }
  }
}

<div class="bg-brand"></div>


---

14. @apply (если нужен CSS)

.btn {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg;
}


---

15. Best Practices

Не бойся длинных className

Группируй классы логически

Используй clsx / classnames

Tailwind + React = 💙



---

16. Часто используемые шаблоны

Кнопка

<button class="px-4 py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white"></button>

Карточка

<div class="p-4 bg-white rounded-xl shadow"></div>


---


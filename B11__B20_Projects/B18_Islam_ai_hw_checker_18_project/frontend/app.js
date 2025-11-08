const form = document.getElementById('homeworkForm');
const tasksContainer = document.getElementById('tasksContainer');
const addTaskBtn = document.getElementById('addTask');
const responseContainer = document.getElementById('response');

const lessons = [
    {value: "Введение в Python", label: "Введение в Python. Переменные, типы данных"},
    {value: "Условные конструкции", label: "Условные конструкции (if, else, elif)"},
    {value: "Циклы", label: "Циклы for, while"},
    {value: "Списки", label: "Списки, срезы, кортежи"},
    {value: "Словари и множества", label: "Словари, множества"},
    {value: "Функции", label: "Функции, *args, **kwargs"},
    {value: "Lambda и исключения", label: "Lambda, исключения"},
    {value: "Файлы", label: "Работа с файлами (txt, JSON, CSV)"},
    {value: "Алгоритмы", label: "Основы алгоритмов (поиск, сортировка)"},
    {value: "Мини проект", label: "Практика: консольное приложение"},
    {value: "ООП", label: "Введение в ООП. Классы и объекты"},
    {value: "Атрибуты и методы", label: "Атрибуты и методы"},
    {value: "Наследование", label: "Наследование, полиморфизм, инкапсуляция"},
    {value: "Магические методы", label: "Магические методы"},
    {value: "RPG проект", label: "Практика: RPG Game"},
    {value: "Модули", label: "Встроенные и собственные модули"},
    {value: "Окружения", label: "Виртуальные окружения"},
    {value: "Регулярки", label: "Регулярные выражения"},
    {value: "Финальный проект", label: "Итоговый проект месяца"}
];

const lessonSelect = document.getElementById('lesson');
lessons.forEach(lesson => {
    const option = document.createElement('option');
    option.value = lesson.value;
    option.textContent = lesson.label;
    lessonSelect.appendChild(option);
});

function addTask(condition = "", answer = "") {
    const taskDiv = document.createElement('div');
    taskDiv.classList.add('task');
    taskDiv.innerHTML = `
        <input type="text" class="task_condition" placeholder="Условие задачи" required value="${condition}">
        <input type="text" class="student_answer" placeholder="Ответ студента" required value="${answer}">
        <button type="button" class="removeTask">Удалить задачу</button>
    `;
    tasksContainer.appendChild(taskDiv);

    taskDiv.querySelector('.removeTask').addEventListener('click', () => {
        taskDiv.remove();
    });
}

addTaskBtn.addEventListener('click', () => addTask());

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const tasks = Array.from(document.querySelectorAll('.task')).map(task => ({
        task_condition: task.querySelector('.task_condition').value,
        student_answer: task.querySelector('.student_answer').value
    }));

    const data = {
        student_name: document.getElementById('student_name').value,
        student_email: document.getElementById('student_email').value,
        lesson: document.getElementById('lesson').value,
        tasks: tasks
    };

    responseContainer.textContent = "Отправка...";
    try {
        const res = await fetch('https://islamdev.up.railway.app/api/v1/homework/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!res.ok) {
            const error = await res.json();
            responseContainer.textContent = "Ошибка:\n" + JSON.stringify(error, null, 2);
            return;
        }

        const result = await res.json();
        responseContainer.textContent = "Результат:\n" + JSON.stringify(result, null, 2);
    } catch (err) {
        responseContainer.textContent = 'Ошибка сети: ' + err;
    }
});

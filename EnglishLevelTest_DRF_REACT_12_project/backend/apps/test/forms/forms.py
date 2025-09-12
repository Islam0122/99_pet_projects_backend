from django import forms
from ..models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        q_type = cleaned_data.get("question_type")
        correct_answer = cleaned_data.get("correct_answer", "").strip()

        # Проверка: для MCQ правильный ответ должен быть A/B/C/D
        if q_type == "mcq":
            if correct_answer.upper() not in ["A", "B", "C", "D"]:
                raise forms.ValidationError("Для Multiple Choice правильный ответ должен быть A, B, C или D.")

        # Для translate / fill / listening — обязательно заполнено correct_answer
        else:
            if not correct_answer:
                raise forms.ValidationError("Для этого типа вопроса обязательно нужно указать правильный ответ.")

        # Для Listening — аудио обязательно
        if q_type == "listening" and not cleaned_data.get("audio_file"):
            raise forms.ValidationError("Для Listening-вопроса нужно добавить аудио файл.")

        return cleaned_data

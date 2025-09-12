from django.contrib import admin
from .models import Level, Test, Question, ResultsTest
from .forms.forms import QuestionForm

# =========================
# LevelAdmin
# =========================
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("title", "description_short")
    search_fields = ("title", "description")

    def description_short(self, obj):
        return (obj.description[:50] + "...") if obj.description else "—"
    description_short.short_description = "Описание"


# =========================
# QuestionInline для Test
# =========================
class QuestionInline(admin.StackedInline):
    model = Question
    form = QuestionForm
    extra = 1
    show_change_link = True
    fieldsets = (
        ("Основное", {
            "fields": ("text", "question_type", "correct_answer")
        }),
        ("Варианты для MCQ", {
            "fields": ("option_a", "option_b", "option_c", "option_d"),
            "classes": ("collapse",),
        }),
        ("Дополнительно", {
            "fields": ("translation", "image", "audio_file"),
            "classes": ("collapse",),
        }),
    )


# =========================
# TestAdmin с Inline
# =========================
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "description_short")
    list_filter = ("level",)
    search_fields = ("name", "description")
    inlines = [QuestionInline]  # здесь добавляем вопросы прямо в Test

    def description_short(self, obj):
        return (obj.description[:50] + "...") if obj.description else "—"
    description_short.short_description = "Описание"


# =========================
# QuestionAdmin отдельно
# =========================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm

    list_display = ("text_short", "question_type", "test", "has_media")
    list_filter = ("question_type", "test__level")
    search_fields = ("text",)

    fieldsets = (
        ("Основное", {
            "fields": ("test", "text", "question_type", "correct_answer")
        }),
        ("Варианты для MCQ", {
            "fields": ("option_a", "option_b", "option_c", "option_d"),
            "classes": ("collapse",),
        }),
        ("Дополнительно", {
            "fields": ("translation", "image", "audio_file"),
            "classes": ("collapse",),
        }),
    )

    def text_short(self, obj):
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")
    text_short.short_description = "Вопрос"

    def has_media(self, obj):
        return bool(obj.image or obj.audio_file)
    has_media.boolean = True
    has_media.short_description = "Медиа"


# =========================
# ResultsTestAdmin
# =========================
@admin.register(ResultsTest)
class ResultsTestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "test", "score", "percentage", "certificate_preview", "created_at")
    list_filter = ("test__level", "created_at")
    search_fields = ("name", "email", "test__name")
    readonly_fields = ("percentage", "certificate", "created_at", "updated_at")

    def certificate_preview(self, obj):
        if obj.certificate:
            return f"<a href='{obj.certificate.url}' target='_blank'>📄 Открыть</a>"
        return "—"
    certificate_preview.allow_tags = True
    certificate_preview.short_description = "Сертификат"

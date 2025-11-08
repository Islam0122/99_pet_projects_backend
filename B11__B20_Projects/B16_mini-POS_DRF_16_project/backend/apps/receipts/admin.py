from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Receipt, ReceiptItem


class ReceiptItemInline(admin.TabularInline):
    """Позиции внутри чека"""
    model = ReceiptItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "discount", "final_price")
    can_delete = False
    can_insert = False


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    """Админ-панель чеков"""
    list_display = (
        "id",
        "cashier",
        "total_amount",
        "payment_method",
        "created_at",
        "show_qr_code",
        "download_pdf_link",
    )
    list_filter = ("payment_method", "created_at")
    search_fields = ("id", "cashier__username", "cashier__fullname")
    readonly_fields = (
        "cashier",
        "total_amount",
        "payment_method",
        "paid_amount",
        "change",
        "created_at",
        "qr_code_preview",
        "pdf_download",
    )
    inlines = [ReceiptItemInline]

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "cashier",
                "total_amount",
                "payment_method",
                "paid_amount",
                "change",
                "created_at",
            )
        }),
        ("Файлы", {
            "fields": ("qr_code_preview", "pdf_download"),
        }),
    )

    def show_qr_code(self, obj):
        """Отображение QR-кода в списке"""
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code.url)
        return "—"
    show_qr_code.short_description = "QR"

    def qr_code_preview(self, obj):
        """Превью QR-кода в карточке"""
        if obj.qr_code:
            return format_html('<img src="{}" width="120" height="120" />', obj.qr_code.url)
        return "QR-код не сгенерирован"
    qr_code_preview.short_description = "QR-код"

    def download_pdf_link(self, obj):
        """Ссылка на PDF в списке"""
        if obj.pdf_receipt:
            return format_html('<a href="{}" target="_blank">📄 PDF</a>', obj.pdf_receipt.url)
        return "—"
    download_pdf_link.short_description = "PDF"

    def pdf_download(self, obj):
        """Кнопка для скачивания PDF в карточке"""
        if obj.pdf_receipt:
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background:#1976d2;color:white;padding:4px 8px;border-radius:4px;text-decoration:none;">Скачать чек (PDF)</a>',
                obj.pdf_receipt.url,
            )
        return "PDF не создан"
    pdf_download.short_description = "Скачать чек (PDF)"




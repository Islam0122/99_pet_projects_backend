from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
import qrcode
from io import BytesIO

class Receipt(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Наличные")
        CARD = "card", _("Карта")
        MIXED = "mixed", _("Смешанная")

    cashier = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="receipts",
        verbose_name=_("Кассир")
    )

    total_amount = models.DecimalField(_("Итоговая сумма"), max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        _("Способ оплаты"),
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    paid_amount = models.DecimalField(_("Оплачено клиентом"), max_digits=12, decimal_places=2, default=0)
    change = models.DecimalField(_("Сдача"), max_digits=12, decimal_places=2, default=0)

    qr_code = models.ImageField(
        upload_to="receipts/qrcodes/",
        blank=True,
        null=True,
        verbose_name=_("QR-код")
    )

    pdf_receipt = models.FileField(
        upload_to="receipts/pdfs/",
        blank=True,
        null=True,
        verbose_name=_("PDF чек")
    )

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Чек")
        verbose_name_plural = _("Чеки")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Чек №{self.id} — {self.total_amount} сом"

    def save(self, *args, **kwargs):
        """При сохранении генерируем QR и PDF"""
        super().save(*args, **kwargs)
        self.generate_qr_code()
        self.generate_pdf_receipt()


    def generate_qr_code(self):
        """Создание QR-кода с данными чека"""
        qr_data = f"Чек №{self.id}\nСумма: {self.total_amount} сом\nОплата: {self.get_payment_method_display()}"

        # Создаем объект QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)

        file_name = f"receipt_{self.id}_qr.png"
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
        buffer.close()

        super().save(update_fields=["qr_code"])

    def generate_pdf_receipt(self):
        """Генерация PDF-чека"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A6)
        p.setTitle(f"Чек №{self.id}")

        # Заголовок
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, 380, "MINI POS — ЧЕК")

        # Информация о чеке
        p.setFont("Helvetica", 10)
        p.drawString(20, 360, f"Чек №: {self.id}")
        p.drawString(20, 345, f"Кассир: {self.cashier.fullname}")
        p.drawString(20, 330, f"Дата: {self.created_at.strftime('%d.%m.%Y %H:%M')}")
        p.drawString(20, 315, f"Способ оплаты: {self.get_payment_method_display()}")

        y = 295
        for item in self.items.all():
            p.drawString(20, y, f"{item.product.title} x{item.quantity} = {item.final_price} сом")
            y -= 15

        # Итого
        p.setFont("Helvetica-Bold", 10)
        p.drawString(20, y - 10, f"ИТОГО: {self.total_amount} сом")
        p.showPage()
        p.save()

        file_name = f"receipt_{self.id}.pdf"
        self.pdf_receipt.save(file_name, ContentFile(buffer.getvalue()), save=False)
        buffer.close()
        super().save(update_fields=["pdf_receipt"])


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Чек")
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Товар")
    )
    quantity = models.PositiveIntegerField(_("Количество"), default=1)
    price = models.DecimalField(_("Цена за единицу"), max_digits=12, decimal_places=2)
    discount = models.DecimalField(_("Скидка"), max_digits=12, decimal_places=2, default=0)
    final_price = models.DecimalField(_("Итоговая сумма"), max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = _("Позиция чека")
        verbose_name_plural = _("Позиции чеков")

    def __str__(self):
        return f"{self.product} × {self.quantity}"

    def save(self, *args, **kwargs):
        """Автоматический пересчёт итоговой цены"""
        self.final_price = (self.price * self.quantity) - self.discount
        super().save(*args, **kwargs)

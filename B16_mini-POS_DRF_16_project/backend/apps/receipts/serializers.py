from rest_framework import serializers
from .models import Receipt, ReceiptItem
from ..product.serializers import ProductSerializer


class ReceiptItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ReceiptItem
        fields = (
            "id",
            "product",
            "quantity",
            "price",
            "discount",
            "final_price",
        )


class ReceiptSerializer(serializers.ModelSerializer):
    cashier = serializers.StringRelatedField(read_only=True)
    items = ReceiptItemSerializer(many=True, read_only=True)
    qr_code_url = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Receipt
        fields = (
            "id",
            "cashier",
            "total_amount",
            "payment_method",
            "paid_amount",
            "change",
            "created_at",
            "items",
            "qr_code_url",
            "pdf_url",
        )

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.qr_code.url)
        return None

    def get_pdf_url(self, obj):
        if obj.pdf_receipt:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.pdf_receipt.url)
        return None

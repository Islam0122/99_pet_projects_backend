from rest_framework import serializers
from .models import Receipt, ReceiptItem
from ..product.serializers import ProductSerializer


class ReceiptItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ReceiptItem
        fields = ('id', 'product', 'quantity', 'price', 'discount', 'final_price')


class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True, read_only=True)
    cashier_name = serializers.CharField(source='cashier.fullname', read_only=True)
    pdf_url = serializers.SerializerMethodField()
    qr_url = serializers.SerializerMethodField()

    class Meta:
        model = Receipt
        fields = (
            'id', 'cashier', 'cashier_name', 'total_amount', 'payment_method',
            'paid_amount', 'change', 'created_at', 'items', 'pdf_url', 'qr_url'
        )
        read_only_fields = ('total_amount', 'change', 'created_at', 'items', 'pdf_url', 'qr_url')

    def get_pdf_url(self, obj):
        if obj.pdf_receipt:
            return obj.pdf_receipt.url
        return None

    def get_qr_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None
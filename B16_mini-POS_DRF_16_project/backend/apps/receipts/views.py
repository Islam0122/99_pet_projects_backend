from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Receipt, ReceiptItem
from .serializers import ReceiptSerializer, ReceiptItemSerializer
from ..product.models import Product

class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Receipt.objects.all().order_by("-created_at")
        return Receipt.objects.filter(cashier=user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.get("items", [])
        payment_method = data.get("payment_method", "cash")
        paid_amount = data.get("paid_amount", 0)

        if not items_data:
            return Response({"error": "Добавьте хотя бы один товар"}, status=status.HTTP_400_BAD_REQUEST)

        receipt = Receipt.objects.create(
            cashier=request.user,
            total_amount=0,
            payment_method=payment_method,
            paid_amount=paid_amount,
            change=0
        )

        total_amount = 0
        for item in items_data:
            product_id = item.get("product_id")
            quantity = int(item.get("quantity", 1))
            product = Product.objects.get(id=product_id)
            price = product.sale_price
            final_price = price * quantity

            ReceiptItem.objects.create(
                receipt=receipt,
                product=product,
                quantity=quantity,
                price=price,
                discount=0,
                final_price=final_price
            )
            total_amount += final_price

        receipt.total_amount = total_amount
        receipt.change = float(paid_amount) - float(total_amount) if payment_method == "cash" else 0
        receipt.save()

        serializer = self.get_serializer(receipt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

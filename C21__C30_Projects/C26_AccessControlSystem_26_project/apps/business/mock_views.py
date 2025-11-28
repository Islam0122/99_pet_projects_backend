from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from apps.users.permissions import RoleBasedPermission

# Тестовые данные
MOCK_PRODUCTS = [
    {"id": 1, "name": "Ноутбук", "price": 50000, "owner_id": 1},
    {"id": 2, "name": "Телефон", "price": 30000, "owner_id": 2},
    {"id": 3, "name": "Планшет", "price": 25000, "owner_id": 1},
    {"id": 4, "name": "Наушники", "price": 5000, "owner_id": 3},
]

MOCK_ORDERS = [
    {"id": 1, "product_id": 1, "quantity": 2, "total": 100000, "owner_id": 1, "status": "pending"},
    {"id": 2, "product_id": 2, "quantity": 1, "total": 30000, "owner_id": 2, "status": "completed"},
    {"id": 3, "product_id": 3, "quantity": 3, "total": 75000, "owner_id": 1, "status": "shipping"},
]

MOCK_STORES = [
    {"id": 1, "name": "Магазин Электроники", "city": "Москва", "owner_id": 1},
    {"id": 2, "name": "Цифровой Мир", "city": "Санкт-Петербург", "owner_id": 2},
]


class MockView:
    def __init__(self, business_element_name, action_type, check_owner=False):
        self.business_element_name = business_element_name
        self.action_type = action_type
        self.check_owner = check_owner
        self._object = None

    def get_object(self):
        return self._object

    def set_object(self, obj):
        self._object = obj


@api_view(['GET', 'POST'])
@permission_classes([RoleBasedPermission])
def products_list_create(request):
    mock_view = MockView(
        business_element_name='products',
        action_type='read' if request.method == 'GET' else 'create',
        check_owner=False
    )

    permission = RoleBasedPermission()
    if not permission.has_permission(request, mock_view):
        return Response(
            {"error": permission.message},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        user = request.user
        user_role_ids = user.roles.all().values_list('role_id', flat=True)

        from apps.access.models import AccessRolesRules, BusinessElement
        element = BusinessElement.objects.get(name='products')
        rules = AccessRolesRules.objects.filter(role_id__in=user_role_ids, element=element)

        has_read_all = any(rule.read_all_permission for rule in rules)

        if has_read_all:
            products = MOCK_PRODUCTS
        else:
            products = [p for p in MOCK_PRODUCTS if p['owner_id'] == user.id]

        return Response({
            "count": len(products),
            "results": products
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        new_product = {
            "id": len(MOCK_PRODUCTS) + 1,
            "name": request.data.get('name'),
            "price": request.data.get('price'),
            "owner_id": request.user.id
        }
        MOCK_PRODUCTS.append(new_product)

        return Response({
            "message": "Товар успешно создан",
            "product": new_product
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([RoleBasedPermission])
def products_detail(request, pk):
    product = next((p for p in MOCK_PRODUCTS if p['id'] == pk), None)
    if not product:
        return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

    action_map = {'GET': 'read', 'PUT': 'update', 'DELETE': 'delete'}
    action_type = action_map.get(request.method)

    mock_view = MockView(
        business_element_name='products',
        action_type=action_type,
        check_owner=True
    )

    class MockProduct:
        def __init__(self, data):
            self.owner_id = data['owner_id']
            self.id = data['id']

    mock_view.set_object(MockProduct(product))

    permission = RoleBasedPermission()
    if not permission.has_permission(request, mock_view):
        return Response(
            {"error": permission.message},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        return Response(product, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        product['name'] = request.data.get('name', product['name'])
        product['price'] = request.data.get('price', product['price'])
        return Response({
            "message": "Товар успешно обновлён",
            "product": product
        }, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        MOCK_PRODUCTS.remove(product)
        return Response({
            "message": "Товар успешно удалён"
        }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([RoleBasedPermission])
def orders_list_create(request):
    mock_view = MockView(
        business_element_name='orders',
        action_type='read' if request.method == 'GET' else 'create',
        check_owner=False
    )

    permission = RoleBasedPermission()
    if not permission.has_permission(request, mock_view):
        return Response(
            {"error": permission.message},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        user = request.user
        user_role_ids = user.roles.all().values_list('role_id', flat=True)

        from apps.access.models import AccessRolesRules, BusinessElement
        element = BusinessElement.objects.get(name='orders')
        rules = AccessRolesRules.objects.filter(role_id__in=user_role_ids, element=element)

        has_read_all = any(rule.read_all_permission for rule in rules)

        if has_read_all:
            orders = MOCK_ORDERS
        else:
            orders = [o for o in MOCK_ORDERS if o['owner_id'] == user.id]

        return Response({
            "count": len(orders),
            "results": orders
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        new_order = {
            "id": len(MOCK_ORDERS) + 1,
            "product_id": request.data.get('product_id'),
            "quantity": request.data.get('quantity'),
            "total": request.data.get('total'),
            "owner_id": request.user.id,
            "status": "pending"
        }
        MOCK_ORDERS.append(new_order)

        return Response({
            "message": "Заказ успешно создан",
            "order": new_order
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([RoleBasedPermission])
def stores_list(request):
    mock_view = MockView(
        business_element_name='stores',
        action_type='read',
        check_owner=False
    )

    permission = RoleBasedPermission()
    if not permission.has_permission(request, mock_view):
        return Response(
            {"error": permission.message},
            status=status.HTTP_403_FORBIDDEN
        )

    user = request.user
    user_role_ids = user.roles.all().values_list('role_id', flat=True)

    from apps.access.models import AccessRolesRules, BusinessElement
    element = BusinessElement.objects.get(name='stores')
    rules = AccessRolesRules.objects.filter(role_id__in=user_role_ids, element=element)

    has_read_all = any(rule.read_all_permission for rule in rules)

    if has_read_all:
        stores = MOCK_STORES
    else:
        stores = [s for s in MOCK_STORES if s['owner_id'] == user.id]

    return Response({
        "count": len(stores),
        "results": stores
    }, status=status.HTTP_200_OK)
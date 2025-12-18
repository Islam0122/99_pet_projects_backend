def binary_search(arr, target, low, high):
    """
    Рекурсивный бинарный поиск
    :param arr: отсортированный список
    :param target: элемент для поиска
    :param low: нижний индекс
    :param high: верхний индекс
    :return: индекс элемента или -1, если не найден
    """
    if low > high:
        return -1  # элемент не найден

    mid = (low + high) // 2
    print(f"Проверяем индекс {mid}, значение {arr[mid]}")  # для наглядности

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)

def main():
    # Ввод и сортировка массива
    arr = list(map(int, input("Введите числа через пробел: ").split()))
    arr.sort()
    print(f"Отсортированный массив: {arr}")

    # Ввод числа для поиска
    target = int(input("Введите число для поиска: "))
    
    # Вызов рекурсивного бинарного поиска
    index = binary_search(arr, target, 0, len(arr) - 1)
    
    if index != -1:
        print(f"Элемент {target} найден на индексе {index}.")
    else:
        print(f"Элемент {target} не найден в массиве.")

if __name__ == "__main__":
    main()

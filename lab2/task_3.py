import sys

# 1. Считываем массив из командной строки
arr = []

for i in range(1, len(sys.argv)):
    arr.append(int(sys.argv[i]))

# 2. Находим максимальный элемент
max_element = arr[0]

for i in range(len(arr)):
    if arr[i] > max_element:
        max_element = arr[i]

print("Максимальный элемент:", max_element)

# 3. Вывод массива в обратном порядке
print("Обратный порядок:")

for i in range(len(arr) - 1, -1, -1):
    print(arr[i], end=" ")

print()

# 4. Находим среднее арифметическое
sum_arr = 0

for i in range(len(arr)):
    sum_arr = sum_arr + arr[i]

average = sum_arr / len(arr)

# 5. Заменяем нули на среднее
for i in range(len(arr)):
    if arr[i] == 0:
        arr[i] = average

print("Массив после замены нулей:")

for i in range(len(arr)):
    print(arr[i], end=" ")
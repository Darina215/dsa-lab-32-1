#1.4
numbers = input("Введите целые числа (через пробел):")

#Создание переменных
current_number = ""
sum_numbers = 0
count = 0

#Цикл подсчета суммы и количества чисел
i = 0
while i < len(numbers):
    if numbers[i] != " ": # не пробел ли число
        current_number = current_number + numbers[i] # добавление символа к строке
    else: 
        if current_number != "": # не пустая ли строка
            sum_numbers = sum_numbers + int(current_number) # добавление числа к сумме
            count = count + 1
            current_number = ""
    i = i + 1

if current_number != "": # обработка последнего числа
    sum_numbers = sum_numbers +int(current_number)
    count = count + 1

print("Сумма чисел:", sum_numbers)
print("Количество чисел:", count)
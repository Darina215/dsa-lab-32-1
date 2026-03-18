#1.1
# Считываем числа с клавиатуры
a1 = float(input("Первое число:"))
a2 = float(input("Второе число:"))
a3 = float(input("Третье число:"))

# Переменная для хранения мин.значения
min_count = a1

#Определение мин числа
if a2 < min_count:
    min_count = a2
    
if a3 < min_count:
    min_count = a3
    
print("минимальное число:", min_count)

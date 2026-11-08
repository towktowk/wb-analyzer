import pandas as pd

print("Запускаю ИИ-агента для анализа отчёта Wildberries...")
print("---------------------------------------------------")

# Указываем имя файла, который нужно прочитать
file_name = "wb_report_test.xlsx"

# Читаем файл с помощью pandas
df = pd.read_excel(file_name)

print(f"Файл {file_name} успешно загружен!")
print("Начинаю анализ данных...\n")

# Считаем общие суммы по колонкам
total_quantity = df["Количество"].sum()
total_sales = df["Сумма_продаж"].sum()
total_commission = df["Комиссия"].sum()
total_logistics = df["Логистика"].sum()
total_storage = df["Хранение"].sum()
total_payout = df["К_выплате"].sum()

# Считаем сумму всех удержаний
total_deductions = total_commission + total_logistics + total_storage

# Выводим красивый отчёт для селлера
print("📊 ИТОГИ НЕДЕЛИ 📊")
print(f"📦 Продано товаров: {total_quantity} шт.")
print(f"💰 Общая сумма продаж (выручка): {total_sales} руб.")
print("")
print(f"📉 Итого удержано Wildberries: {total_deductions} руб.")
print(f"   - Комиссия WB: {total_commission} руб.")
print(f"   - Логистика: {total_logistics} руб.")
print(f"   - Хранение: {total_storage} руб.")
print("")
print(f"✅ К выплате на расчётный счёт: {total_payout} руб.")
print("---------------------------------------------------")
print("Анализ завершён. Жду дальнейших указаний!")
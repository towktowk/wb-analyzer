import pandas as pd

print("Запускаю продвинутого ИИ-агента...")
print("---------------------------------------------------")

# 1. Читаем факт из отчёта
df_fact = pd.read_excel("wb_report_test.xlsx")
fact = {
    "Количество": df_fact["Количество"].sum(),
    "Продажи": df_fact["Сумма_продаж"].sum(),
    "Комиссия": df_fact["Комиссия"].sum(),
    "Логистика": df_fact["Логистика"].sum(),
    "Хранение": df_fact["Хранение"].sum(),
    "К_выплате": df_fact["К_выплате"].sum(),
}

# 2. Читаем план из файла
df_plan = pd.read_excel("plan.xlsx")
plan = {}
for index, row in df_plan.iterrows():
    plan[row["Показатель"]] = row["План"]

# 3. Считаем расходы, которых нет в отчёте ВБ (юнит-экономика)
# Фактические расходы на закупку = количество * себестоимость за штуку
fact_sebestoimost = fact["Количество"] * plan["Себестоимость_ед"]
fact_upakovka = fact["Количество"] * plan["Упаковка_ед"]
fact_reklama = plan["Реклама_общая"]  # Пока берём из плана

# 4. Считаем плановую и фактическую чистую прибыль
plan_profit = (plan["К_выплате"] 
               - (plan["Количество"] * plan["Себестоимость_ед"]) 
               - (plan["Количество"] * plan["Упаковка_ед"]) 
               - plan["Реклама_общая"])

fact_profit = (fact["К_выплате"] 
               - fact_sebestoimost 
               - fact_upakovka 
               - fact_reklama)


# 5. Функция сравнения
def print_comparison(name, plan_value, fact_value):
    diff = fact_value - plan_value
    percent = (diff / plan_value * 100) if plan_value != 0 else 0
    sign = "+" if diff > 0 else ""
    print(f"{name:<12} | План: {plan_value:>8} | Факт: {fact_value:>8} | Отклонение: {sign}{diff:>8} ({percent:.1f}%)")


print("СРАВНЕНИЕ ПЛАНА И ФАКТА")
print("---------------------------------------------------")

print_comparison("Количество", plan["Количество"], fact["Количество"])
print_comparison("Продажи", plan["Продажи"], fact["Продажи"])
print_comparison("Комиссия", plan["Комиссия"], fact["Комиссия"])
print_comparison("Логистика", plan["Логистика"], fact["Логистика"])
print_comparison("Хранение", plan["Хранение"], fact["Хранение"])
print_comparison("К выплате", plan["К_выплате"], fact["К_выплате"])

print("---------------------------------------------------")
print("💰 РАСЧЁТ ЧИСТОЙ ПРИБЫЛИ")
print("---------------------------------------------------")
print_comparison("Прибыль", plan_profit, fact_profit)

print(f"📦 Фактическая себестоимость товара: {fact_sebestoimost} руб.")
print(f"📦 Фактические расходы на упаковку: {fact_upakovka} руб.")
print(f"📦 Расходы на рекламу: {fact_reklama} руб.")
print("---------------------------------------------------")

# 6. Рекомендации
recommendations = []

if fact["Комиссия"] > plan["Комиссия"] * 1.05:
    recommendations.append(f"⚠️ Комиссия выше плана на {fact['Комиссия'] - plan['Комиссия']:.0f} руб. Проверь категорию и акции.")

if fact["Логистика"] > plan["Логистика"] * 1.10:
    recommendations.append(f"⚠️ Логистика выше плана на {fact['Логистика'] - plan['Логистика']:.0f} руб. Проверь габариты и склады.")

if fact["Хранение"] > plan["Хранение"] * 1.10:
    recommendations.append(f"⚠️ Хранение выше плана. Проверь оборачиваемость.")

if fact_profit < plan_profit * 0.90:
    recommendations.append(f"🚨 Чистая прибыль ниже плана более чем на 10%! Разрыв: {plan_profit - fact_profit:.0f} руб. Срочно проверь цену и расходы.")

print("🤖 РЕКОМЕНДАЦИИ АГЕНТА:")
if not recommendations:
    print("✅ Всё отлично, показатели в норме!")
else:
    for i, rec in enumerate(recommendations, start=1):
        print(f"{i}. {rec}")

print("---------------------------------------------------")
print("Анализ завершён.")
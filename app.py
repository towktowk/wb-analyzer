import streamlit as st
import pandas as pd

# Настраиваем внешний вид сайта
st.set_page_config(page_title="ИИ-Агент WB", page_icon="📊", layout="wide")

st.title("📊 ИИ-Агент для селлеров Wildberries")
st.write("Загрузите недельный отчёт ВБ и вашу юнит-экономику, чтобы увидеть реальную прибыль и рекомендации.")

# Создаём окошки для загрузки файлов
col_upload_1, col_upload_2 = st.columns(2)

with col_upload_1:
    file_fact = st.file_uploader("1. Отчёт WB (факт)", type=["xlsx"])

with col_upload_2:
    file_plan = st.file_uploader("2. План (юнит-экономика)", type=["xlsx"])

# Проверяем, загружены ли оба файла
if file_fact is not None and file_plan is not None:
    if st.button("🚀 Запустить анализ"):
        with st.spinner("Агент анализирует данные..."):
            
            # Читаем файлы
            df_fact = pd.read_excel(file_fact)
            df_plan = pd.read_excel(file_plan)
            
            # Считаем факт из отчёта
            fact = {
                "Количество": df_fact["Количество"].sum(),
                "Продажи": df_fact["Сумма_продаж"].sum(),
                "Комиссия": df_fact["Комиссия"].sum(),
                "Логистика": df_fact["Логистика"].sum(),
                "Хранение": df_fact["Хранение"].sum(),
                "К_выплате": df_fact["К_выплате"].sum(),
            }
            
            # Читаем план
            plan = {}
            for index, row in df_plan.iterrows():
                plan[row["Показатель"]] = row["План"]
                
            # Считаем прибыль
            fact_sebest = fact["Количество"] * plan["Себестоимость_ед"]
            fact_upak = fact["Количество"] * plan["Упаковка_ед"]
            fact_reklama = plan["Реклама_общая"]
            fact_profit = fact["К_выплате"] - fact_sebest - fact_upak - fact_reklama
            
            plan_profit = (plan["К_выплате"] 
                           - (plan["Количество"] * plan["Себестоимость_ед"]) 
                           - (plan["Количество"] * plan["Упаковка_ед"]) 
                           - plan["Реклама_общая"])
            
            st.success("Анализ завершён! Ниже представлены ваши данные.")
            
            # Выводим главные цифры в виде красивых карточек
            st.subheader("📈 Главные показатели (Факт)")
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.metric(label="Продажи", value=f"{fact['Продажи']:.0f} руб.")
            with c2:
                total_deductions = fact['Комиссия'] + fact['Логистика'] + fact['Хранение']
                st.metric(label="Удержания ВБ", value=f"{total_deductions:.0f} руб.")
            with c3:
                st.metric(label="К выплате", value=f"{fact['К_выплате']:.0f} руб.")
            with c4:
                st.metric(label="Чистая прибыль", value=f"{fact_profit:.0f} руб.")
                
            # Сравнение прибыли
            st.subheader("⚖️ План / Факт по прибыли")
            diff_profit = fact_profit - plan_profit
            st.metric(label="Отклонение от плана", value=f"{diff_profit:.0f} руб.", delta=f"{diff_profit:.0f} руб.")
            
            # Рекомендации
            st.subheader("🤖 Рекомендации агента")
            
            if fact["Комиссия"] > plan["Комиссия"] * 1.05:
                st.warning(f"⚠️ Комиссия выше плана на {fact['Комиссия'] - plan['Комиссия']:.0f} руб. Проверь категорию и акции.")
                
            if fact["Логистика"] > plan["Логистика"] * 1.10:
                st.warning(f"⚠️ Логистика выше плана на {fact['Логистика'] - plan['Логистика']:.0f} руб. Проверь габариты и склады.")
                
            if fact["Хранение"] > plan["Хранение"] * 1.10:
                st.warning(f"⚠️ Хранение выше плана. Проверь оборачиваемость.")
                
            if fact_profit < plan_profit * 0.90:
                st.error(f"🚨 Чистая прибыль ниже плана более чем на 10%! Разрыв: {plan_profit - fact_profit:.0f} руб.")
            
            # Если всё хорошо и тревог нет
            if fact_profit >= plan_profit * 0.90 and fact["Комиссия"] <= plan["Комиссия"] * 1.05:
                st.success("✅ Все ключевые показатели в норме. Отличная работа!")
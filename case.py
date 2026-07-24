#место для твоего кода
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('Space_Corrected.csv')
r_max = df[' Rocket'].value_counts().index[0]
df[' Rocket'] = df[' Rocket'].fillna(r_max)

df['Is_Success'] = (df['Status Mission'] == 'Success').astype(int)

company_stats = df.groupby('Company Name').agg(
    Total_Launches=('Status Mission', 'count'),    # Всего запусков
    Success_Launches=('Is_Success', 'sum')          # Успешных запусков
).reset_index()

# 4. Считаем процент успеха (от 0% до 100%)
company_stats['Success_Rate_%'] = (company_stats['Success_Launches'] / company_stats['Total_Launches']) * 100

# Округлим для красивого вывода
company_stats['Success_Rate_%'] = company_stats['Success_Rate_%'].round(1)

print("\nКрупные компании (более 50 запусков) — топ по опыту:")
top_experienced = company_stats[company_stats['Total_Launches'] > 50].sort_values(by='Total_Launches', ascending=True)
print(top_experienced[['Company Name', 'Total_Launches', 'Success_Rate_%']].head(10).to_string(index=False))

df['Date_Cleaned'] = pd.to_datetime(df['Datum'], errors='coerce', utc=True)

# Удалим строки, где дату не удалось распознать (если такие есть)
df = df.dropna(subset=['Date_Cleaned'])

# 3. Задаем пограничную дату (20 мая 2020 года)
# Используем таймзону UTC, чтобы избежать конфликтов при сравнении
split_date = pd.to_datetime('2020-05-20', utc=True)

# 4. Делим датасет на два периода
before_2020 = df[df['Date_Cleaned'] <= split_date]
after_2020 = df[df['Date_Cleaned'] > split_date]

# 5. Функция для расчета процента успеха
def calculate_success_rate(data_period):
    total = len(data_period)
    if total == 0:
        return 0, 0
    successes = (data_period['Status Mission'] == 'Success').sum()
    rate = (successes / total) * 100
    return rate, total

# Считаем метрики для обоих периодов
rate_before, total_before = calculate_success_rate(before_2020)
rate_after, total_after = calculate_success_rate(after_2020)

print("--- СРАВНЕНИЕ УСПЕШНОСТИ ЗАПУСКОВ ---")
print(f"До 20 мая 2020 года:")
print(f"  • Всего запусков: {total_before}")
print(f"  • Процент успешных: {rate_before:.2f}%")

print(f"\nПосле 20 мая 2020 года:")
print(f"  • Всего запусков: {total_after}")
print(f"  • Процент успешных: {rate_after:.2f}%")

#top_experienced.plot(kind='barh')
companies = top_experienced['Company Name'].head(10)
launches = top_experienced["Total_Launches"].head(10)
colors = ['yellowgreen', 'gold', 'lightskyblue']
#plt.pie(launches, labels=companies, autopct='%1.1f%%')

#plt.title('Топ 10 компаний по кол-во запусков')
#pl.set_xlabel('Всего запусков')
#pl.set_ylabel("Компания")
periods = ['До 20 мая 2020', 'После 20 мая 2020']
rates = [rate_before, rate_after]
plt.bar(periods, rates, color=['lightcoral', 'lightgreen'], edgecolor='black', width=0.5)
plt.title('Проценты успеха космических миссий')
plt.ylabel('Процент успеха')
plt.grid(axis='y', linestyle= '--', alpha =0.7)


plt.show()

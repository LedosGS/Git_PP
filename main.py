import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-darkgrid')

sns.set_palette("husl")


def load_dataset():
    df = pd.read_csv('dataset.csv')
    df['дата'] = pd.to_datetime(df['дата'], format='%d.%m.%Y')
    df['цена_руб'] = df['цена_руб'].astype(float)
    df['цена_тен'] = df['цена_тен'].astype(float)
    df['оружие'] = df['оружие'].astype(str)
    df['название скина'] = df['название скина'].astype(str)
    correct_df = df[df['оружие'] != "nan"]
    correct_df = correct_df.drop(columns=['Unnamed: 6' , 'Unnamed: 7'])
    return correct_df

def old_price_NST_array(df):
    new_df = df[df['дата'] == "2025-10-18"]
    new_df = new_df[new_df['statrack'] == "нет"]
    new_df['оружие и скин'] = new_df['оружие'] + ' | '+new_df['название скина']
    print(new_df)
    return new_df

def price_NST_array_in_update_day(df):
    new_df = df[df['дата'] == "2025-10-23"]
    new_df = new_df[new_df['statrack'] == "нет"]
    new_df['оружие и скин'] = new_df['оружие'] + ' | '+new_df['название скина']
    print(new_df)
    return new_df

def old_price_ST_array(df):
    new_df = df[df['дата'] == "2025-10-18"]
    new_df = new_df[new_df['statrack'] == "да"]
    new_df['оружие и скин'] = new_df['оружие'] + ' | '+new_df['название скина']
    print(new_df)
    return new_df

def price_ST_array_in_update_day(df):
    new_df = df[df['дата'] == "2025-10-23"]
    new_df = new_df[new_df['statrack'] == "да"]
    new_df['оружие и скин'] = new_df['оружие'] + ' | '+new_df['название скина']
    print(new_df)
    return new_df

df = load_dataset()
print(df)
grid_step = 1000
bar_1 = old_price_NST_array(df)
bar_2 = price_NST_array_in_update_day(df)
bar_3 = old_price_ST_array(df)
bar_4 = price_ST_array_in_update_day(df)

# 4 графика в одной строке
fig, axes = plt.subplots(2, 2, figsize=(16, 9))

# График 1
axes[0, 0].barh(bar_1['оружие и скин'], bar_1['цена_руб'], color='skyblue')
axes[0, 0].set_title('Цены на скины до обновления')
axes[0, 0].set_ylabel('Название скина')
axes[0, 0].set_xlabel('Цена (рубли)')
axes[0, 0].set_xlim([0, 6000])

# График 2
axes[1, 0].barh(bar_2['оружие и скин'], bar_2['цена_руб'], color='skyblue')
axes[1, 0].set_title('Цены на скины в день обновления')
axes[1, 0].set_ylabel('Название скина')
axes[1, 0].set_xlabel('Цена (рубли)')
axes[1, 0].set_xlim([0, 6000])


# График 3
axes[0, 1].barh(bar_3['оружие и скин'], bar_3['цена_руб'], color='lightgreen')
axes[0, 1].set_title('Цены на скины до обновления с пометкой stattrack')
axes[0, 1].set_ylabel('Название скина')
axes[0, 1].set_xlabel('Цена (рубли)')
axes[0, 1].set_xlim([0, 6000])


# График 4
axes[1, 1].barh(bar_4['оружие и скин'], bar_4['цена_руб'], color='lightgreen')
axes[1, 1].set_title('Цены на скины в день обновления с пометкой stattrack')
axes[1, 1].set_ylabel('Название скина')
axes[1, 1].set_xlabel('Цена (рубли)')
axes[1, 1].set_xlim([0, 6000])

plt.tight_layout()
plt.show()

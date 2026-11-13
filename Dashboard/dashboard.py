import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_style("ticks")

def create_daily_rentals_df(df):
    daily_rentals_df = (
        df.resample(rule="D", on="dteday")
        .agg({
            "cnt": "sum",
            "registered": "sum",
            "casual": "sum"
        })
        .reset_index()
    )
    return daily_rentals_df


def create_byseason_df(df):
    all_season = df["season"].unique()
    byseason_df = (
        df.groupby(by="season")["cnt"]
        .mean()
        .reindex(["Spring", "Summer", "Fall", "Winter"], fill_value=0)
        .sort_values(ascending=False)
        .reset_index()
    )
    return byseason_df

def create_byweather_df(df):
    all_weather = df["weathersit"].unique()
    byweather_df = (
        df.groupby(by="weathersit")["cnt"]
        .mean()
        .reindex(all_weather, fill_value=0)
        .sort_values(ascending=False)
        .reset_index()
    )
    return byweather_df

def create_hourly_workingday_df(df):
    workingday_df = (
        df[df["workingday"] == 1]
        .groupby(by="hr")[["casual", "registered"]]
        .mean()
        .reset_index()
    )
    return workingday_df

def create_hourly_holiday_df(df):
    holiday_df = (
        df[df["workingday"] == 0]
        .groupby(by="hr")[["casual", "registered"]]
        .mean()
        .reset_index()
    )
    return holiday_df

def create_quarterly_rentals_df(df):
    temp_df = df.copy()
    temp_df["quarter"] = temp_df["dteday"].dt.to_period("Q").astype(str)
    quarterly_rentals_df = temp_df.groupby(by="quarter")[["casual", "registered"]].sum().reset_index()
    return quarterly_rentals_df

def create_demand_clustering_df(df):
    temp_df = df.copy()
    max_val = max(6001, temp_df["cnt"].max())
    bins = [0, 3000, 6000, max_val]
    labels = ["Low Demand", "Medium Demand", "High Demand"]
    temp_df["demand_category"] = pd.cut(temp_df["cnt"], bins=bins, labels=labels)
    demand_clustering_df = temp_df.groupby(by="demand_category", observed=False)["cnt"].count().reset_index()
    demand_clustering_df.rename(columns={"cnt": "day_count"}, inplace=True)
    return demand_clustering_df

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
day_df = pd.read_csv(os.path.join(BASE_DIR, "day_clean.csv"))
hour_df = pd.read_csv(os.path.join(BASE_DIR, "hour_clean.csv"))

day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(drop=True, inplace=True)
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(drop=True, inplace=True)
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.title("🚲 Bike Sharing Dashboard")
    st.markdown("## Date Range Filter")

    start_date = st.date_input(
        label = 'Tanggal Mulai',
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )

    end_date = st.date_input(
        label = 'Tanggal Akhir',
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

if start_date > end_date:
    st.sidebar.error("Tanggal mulai harus lebih kecil dari tanggal akhir.")
    st.stop()

main_day_df = day_df[(day_df["dteday"] >=   str(start_date)) & (day_df["dteday"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))]       

daily_rentals_df = create_daily_rentals_df(main_day_df)
byseason_df = create_byseason_df(main_day_df)
byweather_df = create_byweather_df(main_day_df)
workingday_df = create_hourly_workingday_df(main_hour_df)
holiday_df = create_hourly_holiday_df(main_hour_df)
quarterly_rentals_df = create_quarterly_rentals_df(main_day_df)
demand_clustering_df = create_demand_clustering_df(main_day_df)

st.header("Bike Sharing Analytics Dashboard :sparkles:")
st.markdown(f"Menampilkan data penyewaan sepeda dari **{start_date}** hingga **{end_date}**.")
st.subheader("Daily Rentals")

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rentals_df["cnt"].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")

with col2:
    total_registered = daily_rentals_df["registered"].sum()
    st.metric("Pengguna Registered", value=f"{total_registered:,}")

with col3:
    total_casual = daily_rentals_df["casual"].sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["cnt"],
    linewidth=2,
    color="#90caf9"
)
ax.tick_params(axis="y", labelsize=12)
ax.tick_params(axis="x", labelsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.7)
sns.despine()
st.pyplot(fig)

#Pertanyaan 1 
st.subheader("Identifikasi Penurunan Penyewaan untuk Jadwal Perawatan")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

colors_season = ["#D3D3D3"] * (len(byseason_df) - 1) + ["#90caf9"]
colors_weather = ["#D3D3D3"] * (len(byweather_df) - 1) + ["#90caf9"]    

sns.barplot(
    x="season",
    y="cnt",
    data=byseason_df,
    hue="season",
    ax=ax[0],
    palette=colors_season,
    legend=False
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Rata-rata Penyewaan per Musim", loc="center", fontsize=16)
ax[0].tick_params(axis="y", labelsize=14)
ax[0].tick_params(axis="x", labelsize=14)
ax[0].grid(axis="y", linestyle="--", alpha=0.7)


sns.barplot(
    x="weathersit",
    y="cnt",
    data=byweather_df,
    hue="weathersit",
    ax=ax[1],
    palette=colors_weather,
    legend=False
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Rata-rata Penyewaan per Kondisi Cuaca", loc="center", fontsize=16)
ax[1].tick_params(axis="y", labelsize=14)
ax[1].tick_params(axis="x", labelsize=14)
ax[1].grid(axis="y", linestyle="--", alpha=0.7)

sns.despine()
st.pyplot(fig)

with st.expander("Insight dan Rekomendasi Perawatan Armada"):
    st.markdown(
        """
        - **Waktu Perawatan Optimal:** Penyewaan harian turun paling rendah pada musim semi (*Spring*) dan saar kondisi cuaca buruk (hujan ringan / bersalju).
        - **Rekomendasi Operasional:** Jadwalkan pemeliharaan besar, pengecekan rem, dan penggantian suku cadang armada pada periode musim semi agar tidak mengganggu ketersediaan sepeda pada saat musim puncak penyewaan.
        """
    )
st.divider()

#Pertanyaan 2
st.subheader("Perbedaan Jam Sibuk di Hari Kerja dan Hari Libur untuk Rebalancing Stok Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

ax[0].plot(
    workingday_df["hr"],
    workingday_df["registered"],
    label="Pekerja Registered",
    linewidth=2.5,
    color="#90caf9",
    marker="o"
)
ax[0].plot(
    workingday_df["hr"],
    workingday_df["casual"],
    label="Pekerja Casual",
    linewidth=2.5,
    color="#d3d3d3",
    marker="o"
)
ax[0].set_title("Pola Jam Sibuk di Hari Kerja", loc="center", fontsize=18)
ax[0].set_xlabel("Jam (00.00 - 23.00)", fontsize=14)
ax[0].set_xticks(range(0, 24))
ax[0].tick_params(axis="y", labelsize=12)
ax[0].tick_params(axis="x", labelsize=12)
ax[0].legend(fontsize=12)
ax[0].grid(axis="y", linestyle="--", alpha=0.7)

ax[1].plot(
    holiday_df["hr"],
    holiday_df["registered"],
    label="Pekerja Registered",
    linewidth=2.5,
    color="#90caf9",
    marker="o"
)
ax[1].plot(
    holiday_df["hr"],
    holiday_df["casual"],
    label="Pekerja Casual",
    linewidth=2.5,
    color="#d3d3d3",
    marker="o"
)
ax[1].set_title("Pola Jam Sibuk di Hari Libur", loc="center", fontsize=18)
ax[1].set_xlabel("Jam (00.00 - 23.00)", fontsize=14)
ax[1].set_xticks(range(0, 24))
ax[1].tick_params(axis="y", labelsize=12)
ax[1].tick_params(axis="x", labelsize=12)
ax[1].legend(fontsize=12)   
ax[1].grid(axis="y", linestyle="--", alpha=0.7)

sns.despine()
st.pyplot(fig)

with st.expander("Insight dan Strategi Rebalancing Stok Sepeda"):
    st.markdown(
        """
        - **Pola Komuter (Hari Kerja):** Terjadi dua lonjakan tajam pada **pukul 08.00** (jam berangkat kerja/sekolah) dan **pukul 17.00 - 18.00** (jam pulang) yang didominasi olah pegguna *registered*.
        - **Pola Rekreasi (Hari Libur):** Kurva meladai dan memuncak di siang hari sekitar **pukul 10.00 - 16.00** dengan peningkatan signifikan dari pengguna *casual*. 
        - **Rekomendasi Operasional:** Lakukan distribusi ulang sepeda (*rebalancing*) pada jam-jam sibuk di hari kerja untuk memenuhi permintaan pengguna *registered*, dan fokus pada penyediaan sepeda di lokasi-lokasi rekreasi pada siang hari di hari libur untuk memenuhi permintaan pengguna *casual*.
        """
    )
st.divider()

#Pertanyaan 3
st.subheader("Pertumbuhan Kuartalan dan Segmentasi Permintaan Harian")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(
            quarterly_rentals_df["quarter"],
            quarterly_rentals_df["registered"],
            label="Penyewaan Registered",
            linewidth=2.5,
            color="#90caf9",
            marker="o"
        )
    ax.plot(
        quarterly_rentals_df["quarter"],
        quarterly_rentals_df["casual"],
        label="Penyewaan Casual",
        linewidth=2.5,
        color="#d3d3d3",
        marker="o"
    )
    ax.set_title("Pertumbuhan Penyewaan Sepeda per Kuartal", loc="center", fontsize=18)
    ax.set_ylabel("Total Penyewaan", fontsize=14)
    ax.tick_params(axis="y", labelsize=12)
    ax.tick_params(axis="x", labelsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend(fontsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(12, 7))
    colors_cluster = ["#d3d3d3", "#90caf9", "#d3d3d3"]
    sns.barplot(
        x="demand_category",
        y="day_count",
        data=demand_clustering_df,
        hue="demand_category",
        palette=colors_cluster,
        legend=False,
        ax=ax,
    )
    ax.set_title("Distribusi Hari Berdasarkan Kluster Permintaan", loc="center", fontsize=18)
    ax.set_ylabel("Jumlah Hari", fontsize=14)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=12)
    ax.tick_params(axis="x", labelsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    sns.despine()
    st.pyplot(fig)

with st.expander("Insight Pertumbuhan dan Kapasitas Armada"):
    st.markdown(
        """
        - **Tren Pertumbuhan Tahunan:** Volume penyewaan meningkat pesat dari tahun 2011 ke 2012, dengan pola musim yang selalu memuncak pada **Kuartal 3 (Q3)** dan menurun pada **Kuartal 1 (Q1)**. Hal ini menunjukkan adanya permintaan yang tinggi pada musim panas dan rendah pada musim dingin.
        - **Segmentasi Permintaan Harian:** Sebagian besar hari operasional berada pada kategori **Medium Demand (3000 - 6000 penyewaan)** yang terkonsentrasi di tahun 2012, sementara hari dengan **High Demand (>6000 penyewaan)** hanya terjadi pada beberapa hari tertentu. Hal ini menunjukkan bahwa kapasitas armada sepeda saat ini cukup untuk memenuhi permintaan harian, namun perlu diperhatikan adanya lonjakan permintaan pada hari-hari tertentu.
        """
    )
st.divider()
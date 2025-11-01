import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

# Load cleaned data
all_df = pd.read_csv("dashboard/main_data.csv")

# Kolom yang dikonversi menjadi datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Tambah kolom tahun dan bulan
all_df["year"] = all_df["yr"].map({0: 2011, 1: 2012})
all_df["month"] = all_df["dteday"].dt.month

# Mapping nama bulan
month_map = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
all_df["month_name"] = all_df["month"].map(month_map)


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("dashboard/bike_sharing_logo.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

# Filter dataset berdasarkan rentang waktu yang dipilih
main_df = all_df[
    (all_df["dteday"] >= pd.to_datetime(start_date))
    & (all_df["dteday"] <= pd.to_datetime(end_date))
]

# Menampilkan header Dashboard
st.header("Bike Sharing Analysis Dashboard:bike:")

# SUBHEADER 1
st.subheader("Tren Peminjaman Sepeda Tahun 2012")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    all_df[all_df["year"] == 2012]["dteday"],
    all_df[all_df["year"] == 2012]["cnt"],
    color="blue",
)
ax.set_title("Tren Harian Peminjaman Sepeda Tahun 2012")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman (cnt)")
st.pyplot(fig)

# SUBHEADER 2
st.subheader("Rata-rata Peminjaman Sepeda per Bulan (2012)")

# Hitung rata-rata
monthly_avg = (
    all_df[all_df["year"] == 2012]
    .groupby("month_name")["cnt"]
    .mean()
    .reindex(month_map.values())
)

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(monthly_avg.index, monthly_avg.values, color="skyblue")
ax.set_title("Rata-rata Peminjaman Sepeda per Bulan (2012)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Peminjaman (cnt)")
plt.xticks(rotation=45)
st.pyplot(fig)

# SUBHEADER 3
st.subheader("Perbandingan Total Pengguna Casual vs Registered")

total_casual = main_df["casual"].sum()
total_registered = main_df["registered"].sum()

fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(
    ["Casual", "Registered"],
    [total_casual, total_registered],
    color=["orange", "green"],
)
ax.set_ylabel("Total Peminjaman")
ax.set_title("Perbandingan Pengguna Casual vs Registered")
st.pyplot(fig)

# SUBHEADER 4
st.subheader("Scatter Plot Hubungan Suhu (temp) dengan Peminjaman Sepeda")

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(main_df["temp"], main_df["cnt"], alpha=0.6, color="red")
ax.set_xlabel("Suhu (Normalized)")
ax.set_ylabel("Jumlah Peminjaman (cnt)")
ax.set_title("Hubungan Suhu dengan Peminjaman Sepeda")
st.pyplot(fig)

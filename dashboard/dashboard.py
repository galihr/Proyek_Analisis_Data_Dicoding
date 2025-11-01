import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

# Load cleaned data
all_df = pd.read_csv("main_data.csv")

# Kolom yang ingin dikonversi menjadi datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bike_sharing_logo.jpg")

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

st.subheader("Tren Peminjaman Sepeda Tahun 2012")
df_2012 = main_df[main_df["year"] == 2012]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_2012["dteday"], df_2012["cnt"], color="blue")
ax.set_title("Tren Peminjaman Sepeda Tahun 2012")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

st.subheader("Rata-rata Peminjaman Sepeda per Bulan (2012)")

monthly_avg = df_2012.groupby("month")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(monthly_avg["month"], monthly_avg["cnt"], color="skyblue")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Rata-rata Peminjaman Sepeda per Bulan (2012)")
st.pyplot(fig)


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

st.subheader("Scatter Plot Hubungan Suhu (temp) dengan Peminjaman Sepeda")

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(main_df["temp"], main_df["cnt"], alpha=0.6, color="red")
ax.set_xlabel("Suhu (Normalized)")
ax.set_ylabel("Jumlah Peminjaman (cnt)")
ax.set_title("Hubungan Suhu dengan Peminjaman Sepeda")
st.pyplot(fig)

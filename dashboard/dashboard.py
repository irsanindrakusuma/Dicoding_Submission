import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

st.set_page_config(
    page_title="Dashboard E-Commerce Brasil", page_icon=None, layout="wide"
)


@st.cache_data
def load_data():
    """Memuat dataset dashboard"""
    orders_reviews = pd.read_csv("orders_reviews.csv")
    geo_orders = pd.read_csv("geo_orders.csv")

    date_cols = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for col in date_cols:
        if col in orders_reviews.columns:
            orders_reviews[col] = pd.to_datetime(orders_reviews[col])

    return orders_reviews, geo_orders


def create_delivery_boxplot(df):
    """Boxplot waktu pengiriman"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="review_score", y="delivery_time", palette="coolwarm", ax=ax)
    ax.set_title(
        "Distribusi Waktu Pengiriman per Skor Review", fontsize=14, fontweight="bold"
    )
    ax.set_xlabel("Skor Review (1-5)", fontsize=12)
    ax.set_ylabel("Waktu Pengiriman (hari)", fontsize=12)
    ax.grid(axis="y", alpha=0.5)
    plt.tight_layout()
    return fig


def create_delivery_histogram(df):
    """Histogram waktu pengiriman"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x="delivery_time", bins=30, kde=True, color="#3498db", ax=ax)
    ax.axvline(
        df["delivery_time"].mean(),
        color="red",
        linestyle="--",
        label=f"Mean: {df['delivery_time'].mean():.1f}",
    )
    ax.axvline(
        df["delivery_time"].median(),
        color="green",
        linestyle="--",
        label=f"Median: {df['delivery_time'].median():.1f}",
    )
    ax.set_title("Distribusi Waktu Pengiriman", fontsize=14, fontweight="bold")
    ax.set_xlabel("Waktu Pengiriman (hari)", fontsize=12)
    ax.set_ylabel("Jumlah Order", fontsize=12)
    ax.legend()
    plt.tight_layout()
    return fig


def create_score_distribution(df):
    """Distribusi skor review"""
    fig, ax = plt.subplots(figsize=(10, 6))
    score_counts = df["review_score"].value_counts().sort_index()
    colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"]
    bars = ax.bar(score_counts.index, score_counts.values, color=colors)
    ax.set_title("Distribusi Skor Review", fontsize=14, fontweight="bold")
    ax.set_xlabel("Skor Review", fontsize=12)
    ax.set_ylabel("Jumlah Order", fontsize=12)
    for bar, val in zip(bars, score_counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 100,
            f"{val:,}",
            ha="center",
            fontsize=10,
        )
    plt.tight_layout()
    return fig


def create_delivery_status_pie(df):
    """Pie chart status pengiriman"""
    fig, ax = plt.subplots(figsize=(8, 8))
    status_counts = df["delivery_status"].value_counts()
    colors = ["#27ae60", "#e74c3c"]
    ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        explode=(0.02, 0.02),
        startangle=90,
        textprops={"fontsize": 12},
    )
    ax.set_title("Proporsi Status Pengiriman", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def create_monthly_trend(df):
    """Tren bulanan order"""
    df_copy = df.copy()
    df_copy["month"] = df_copy["order_purchase_timestamp"].dt.to_period("M")
    monthly = (
        df_copy.groupby("month")
        .agg({"order_id": "count", "delivery_time": "mean", "review_score": "mean"})
        .reset_index()
    )
    monthly["month"] = monthly["month"].astype(str)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    ax1.plot(
        monthly["month"], monthly["order_id"], "b-o", label="Jumlah Order", linewidth=2
    )
    ax2.plot(
        monthly["month"],
        monthly["review_score"],
        "g-s",
        label="Rata-rata Skor",
        linewidth=2,
    )

    ax1.set_xlabel("Bulan", fontsize=12)
    ax1.set_ylabel("Jumlah Order", color="blue", fontsize=12)
    ax2.set_ylabel("Rata-rata Skor Review", color="green", fontsize=12)
    ax1.tick_params(axis="x", rotation=45)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax1.set_title("Tren Bulanan: Order dan Skor Review", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def create_avg_delivery_by_score(df):
    """Rata-rata pengiriman per skor"""
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_delivery = df.groupby("review_score")["delivery_time"].mean()
    colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"]
    bars = ax.bar(avg_delivery.index, avg_delivery.values, color=colors)
    ax.set_title(
        "Rata-rata Waktu Pengiriman per Skor Review", fontsize=14, fontweight="bold"
    )
    ax.set_xlabel("Skor Review", fontsize=12)
    ax.set_ylabel("Rata-rata Waktu Pengiriman (hari)", fontsize=12)
    for bar, val in zip(bars, avg_delivery.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f"{val:.1f}",
            ha="center",
            fontsize=10,
        )
    ax.axhline(
        df["delivery_time"].mean(),
        color="red",
        linestyle="--",
        label=f"Mean keseluruhan: {df['delivery_time'].mean():.1f}",
    )
    ax.legend()
    plt.tight_layout()
    return fig


def create_state_barplot(df):
    """Barplot status per state"""
    fig, ax = plt.subplots(figsize=(14, 6))
    state_order = df.groupby("customer_state").size().sort_values(ascending=False).index
    sns.countplot(
        data=df,
        x="customer_state",
        hue="delivery_status",
        order=state_order,
        palette={"Terlambat": "#e74c3c", "Tepat Waktu": "#27ae60"},
        ax=ax,
    )
    ax.set_title(
        "Pengiriman Tepat Waktu vs Terlambat per State", fontsize=14, fontweight="bold"
    )
    ax.set_xlabel("Kode State", fontsize=12)
    ax.set_ylabel("Jumlah Pengiriman", fontsize=12)
    ax.legend(title="Status")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def create_late_percentage_by_state(df):
    """Persentase keterlambatan per state"""
    state_stats = (
        df.groupby("customer_state")
        .apply(lambda x: (x["delivery_status"] == "Terlambat").sum() / len(x) * 100)
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(14, 6))
    colors = [
        "#e74c3c" if val > state_stats.mean() else "#f39c12"
        for val in state_stats.values
    ]
    ax.bar(state_stats.index, state_stats.values, color=colors)
    ax.axhline(
        state_stats.mean(),
        color="blue",
        linestyle="--",
        label=f"Rata-rata: {state_stats.mean():.1f}%",
    )
    ax.set_title("Persentase Keterlambatan per State", fontsize=14, fontweight="bold")
    ax.set_xlabel("Kode State", fontsize=12)
    ax.set_ylabel("Persentase Terlambat (%)", fontsize=12)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    plt.tight_layout()
    return fig


def create_geo_scatter(df):
    """Scatter plot geografis"""
    fig, ax = plt.subplots(figsize=(10, 10))
    late = df[df["delivery_status"] == "Terlambat"]
    ontime = df[df["delivery_status"] == "Tepat Waktu"]

    ax.scatter(
        ontime["geolocation_lng"],
        ontime["geolocation_lat"],
        s=2,
        alpha=0.3,
        color="#27ae60",
        label="Tepat Waktu",
    )
    ax.scatter(
        late["geolocation_lng"],
        late["geolocation_lat"],
        s=2,
        alpha=0.5,
        color="#e74c3c",
        label="Terlambat",
    )

    ax.set_xlim(-74, -34)
    ax.set_ylim(-34, 6)
    ax.set_title("Peta Sebaran Pengiriman di Brasil", fontsize=14, fontweight="bold")
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig


def create_top_cities(df, n=10):
    """Top kota dengan order terbanyak"""
    city_counts = df["geolocation_city"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(city_counts.index[::-1], city_counts.values[::-1], color="#3498db")
    ax.set_title(f"Top {n} Kota dengan Order Terbanyak", fontsize=14, fontweight="bold")
    ax.set_xlabel("Jumlah Order", fontsize=12)
    ax.set_ylabel("Kota", fontsize=12)
    for bar, val in zip(bars, city_counts.values[::-1]):
        ax.text(
            val + 50,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center",
            fontsize=10,
        )
    plt.tight_layout()
    return fig


def create_delivery_time_by_state(df, top_n=10):
    """Waktu pengiriman per state"""
    state_delivery = df.groupby("customer_state")["delivery_time"].agg(
        ["mean", "count"]
    )
    state_delivery = state_delivery[state_delivery["count"] >= 100].sort_values(
        "mean", ascending=True
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.RdYlGn_r(
        [i / len(state_delivery) for i in range(len(state_delivery))]
    )
    ax.barh(state_delivery.index, state_delivery["mean"], color=colors)
    ax.axvline(
        df["delivery_time"].mean(),
        color="red",
        linestyle="--",
        label=f"Rata-rata nasional: {df['delivery_time'].mean():.1f} hari",
    )
    ax.set_title("Rata-rata Waktu Pengiriman per State", fontsize=14, fontweight="bold")
    ax.set_xlabel("Rata-rata Waktu Pengiriman (hari)", fontsize=12)
    ax.set_ylabel("State", fontsize=12)
    ax.legend()
    plt.tight_layout()
    return fig


def create_score_heatmap(df):
    """Heatmap skor dan waktu pengiriman"""
    df_copy = df.copy()
    df_copy["delivery_bin"] = pd.cut(
        df_copy["delivery_time"],
        bins=[0, 7, 14, 21, 30, float("inf")],
        labels=["0-7", "8-14", "15-21", "22-30", ">30"],
    )
    heatmap_data = (
        df_copy.groupby(["delivery_bin", "review_score"]).size().unstack(fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    ax.set_title(
        "Distribusi Skor Review berdasarkan Waktu Pengiriman",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Skor Review", fontsize=12)
    ax.set_ylabel("Waktu Pengiriman (hari)", fontsize=12)
    plt.tight_layout()
    return fig


# Load data
orders_reviews, geo_orders = load_data()

# Sidebar filters
st.sidebar.title("Filter Data")

if "order_purchase_timestamp" in orders_reviews.columns:
    min_date = orders_reviews["order_purchase_timestamp"].min().date()
    max_date = orders_reviews["order_purchase_timestamp"].max().date()
    date_range = st.sidebar.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

score_range = st.sidebar.slider(
    "Rentang Skor Review", min_value=1, max_value=5, value=(1, 5)
)

max_delivery_time = int(orders_reviews["delivery_time"].max())
delivery_range = st.sidebar.slider(
    "Rentang Waktu Pengiriman (hari)",
    min_value=0,
    max_value=min(max_delivery_time, 60),
    value=(0, 30),
)

status_options = ["Semua", "Tepat Waktu", "Terlambat"]
selected_status = st.sidebar.selectbox("Status Pengiriman", status_options)

all_states = sorted(geo_orders["customer_state"].unique())
selected_states = st.sidebar.multiselect(
    "Pilih State", options=all_states, default=all_states
)

# Apply filters
filtered_reviews = orders_reviews.copy()

if "order_purchase_timestamp" in filtered_reviews.columns and len(date_range) == 2:
    filtered_reviews = filtered_reviews[
        (filtered_reviews["order_purchase_timestamp"].dt.date >= date_range[0])
        & (filtered_reviews["order_purchase_timestamp"].dt.date <= date_range[1])
    ]

filtered_reviews = filtered_reviews[
    (filtered_reviews["review_score"] >= score_range[0])
    & (filtered_reviews["review_score"] <= score_range[1])
    & (filtered_reviews["delivery_time"] >= delivery_range[0])
    & (filtered_reviews["delivery_time"] <= delivery_range[1])
]

if selected_status != "Semua":
    filtered_reviews = filtered_reviews[
        filtered_reviews["delivery_status"] == selected_status
    ]

filtered_geo = geo_orders[geo_orders["customer_state"].isin(selected_states)].copy()

if selected_status != "Semua":
    filtered_geo = filtered_geo[filtered_geo["delivery_status"] == selected_status]

filtered_geo = filtered_geo[
    (filtered_geo["delivery_time"] >= delivery_range[0])
    & (filtered_geo["delivery_time"] <= delivery_range[1])
]

# Header
st.title("Dashboard Analisis E-Commerce Brasil")
st.markdown(
    "Analisis hubungan waktu pengiriman dengan kepuasan pelanggan dan distribusi geografis keterlambatan"
)

# Metrics
st.subheader("Metrik Utama")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Order", f"{len(filtered_reviews):,}")

with col2:
    avg_delivery = filtered_reviews["delivery_time"].mean()
    st.metric("Rata-rata Pengiriman", f"{avg_delivery:.1f} hari")

with col3:
    median_delivery = filtered_reviews["delivery_time"].median()
    st.metric("Median Pengiriman", f"{median_delivery:.1f} hari")

with col4:
    avg_score = filtered_reviews["review_score"].mean()
    st.metric("Rata-rata Skor", f"{avg_score:.2f}")

with col5:
    if len(filtered_reviews) > 1:
        correlation = filtered_reviews["delivery_time"].corr(
            filtered_reviews["review_score"]
        )
        st.metric("Korelasi", f"{correlation:.3f}")
    else:
        st.metric("Korelasi", "N/A")

with col6:
    if len(filtered_reviews) > 0:
        late_pct = (
            (filtered_reviews["delivery_status"] == "Terlambat").sum()
            / len(filtered_reviews)
            * 100
        )
        st.metric("Keterlambatan", f"{late_pct:.1f}%")
    else:
        st.metric("Keterlambatan", "N/A")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["Ringkasan", "Analisis Pengiriman", "Analisis Geografis", "Analisis Tren"]
)

with tab1:
    st.header("Ringkasan Analisis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Skor Review")
        if len(filtered_reviews) > 0:
            fig_score = create_score_distribution(filtered_reviews)
            st.pyplot(fig_score)
            plt.close()

            st.markdown(
                """
            **Insight:**
            - Mayoritas pelanggan memberikan skor 5 (sangat puas)
            - Skor rendah (1-2) perlu perhatian khusus
            - Distribusi cenderung positif (skewed right)
            """
            )

    with col2:
        st.subheader("Status Pengiriman")
        if len(filtered_reviews) > 0:
            fig_pie = create_delivery_status_pie(filtered_reviews)
            st.pyplot(fig_pie)
            plt.close()

            ontime_pct = (
                (filtered_reviews["delivery_status"] == "Tepat Waktu").sum()
                / len(filtered_reviews)
                * 100
            )
            st.markdown(
                f"""
            **Insight:**
            - {ontime_pct:.1f}% pengiriman tepat waktu
            - {100-ontime_pct:.1f}% pengiriman terlambat
            - Target: tingkatkan ketepatan waktu pengiriman
            """
            )

    st.subheader("Statistik Deskriptif")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Waktu Pengiriman (hari)**")
        if len(filtered_reviews) > 0:
            delivery_stats = filtered_reviews["delivery_time"].describe()
            st.dataframe(delivery_stats.to_frame().T.round(2))

    with col2:
        st.markdown("**Skor Review**")
        if len(filtered_reviews) > 0:
            score_stats = filtered_reviews["review_score"].describe()
            st.dataframe(score_stats.to_frame().T.round(2))

with tab2:
    st.header("Analisis Waktu Pengiriman")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Waktu Pengiriman")
        if len(filtered_reviews) > 0:
            fig_hist = create_delivery_histogram(filtered_reviews)
            st.pyplot(fig_hist)
            plt.close()

            st.markdown(
                """
            **Insight:**
            - Distribusi waktu pengiriman skewed ke kanan
            - Mayoritas pengiriman selesai dalam 10-15 hari
            - Outlier menunjukkan kasus pengiriman ekstrem
            """
            )

    with col2:
        st.subheader("Waktu Pengiriman vs Skor Review")
        if len(filtered_reviews) > 0:
            fig_box = create_delivery_boxplot(filtered_reviews)
            st.pyplot(fig_box)
            plt.close()

            st.markdown(
                """
            **Insight:**
            - Skor tinggi memiliki median pengiriman lebih rendah
            - Skor rendah menunjukkan variasi pengiriman tinggi
            - Korelasi negatif: pengiriman cepat = skor tinggi
            """
            )

    st.subheader("Rata-rata Waktu Pengiriman per Skor")
    if len(filtered_reviews) > 0:
        fig_avg = create_avg_delivery_by_score(filtered_reviews)
        st.pyplot(fig_avg)
        plt.close()

    st.subheader("Heatmap Skor dan Waktu Pengiriman")
    if len(filtered_reviews) > 0:
        fig_heatmap = create_score_heatmap(filtered_reviews)
        st.pyplot(fig_heatmap)
        plt.close()

        st.markdown(
            """
        **Insight:**
        - Pengiriman 0-7 hari dominan mendapat skor 5
        - Pengiriman >21 hari cenderung mendapat skor rendah
        - Threshold optimal: pengiriman di bawah 14 hari
        """
        )

    st.subheader("Detail per Skor Review")
    if len(filtered_reviews) > 0:
        score_detail = (
            filtered_reviews.groupby("review_score")
            .agg(
                {
                    "delivery_time": ["count", "mean", "median", "std", "min", "max"],
                    "delivery_status": lambda x: (x == "Terlambat").sum(),
                }
            )
            .round(2)
        )
        score_detail.columns = [
            "Jumlah",
            "Mean",
            "Median",
            "Std",
            "Min",
            "Max",
            "Terlambat",
        ]
        score_detail["Persen Terlambat"] = (
            score_detail["Terlambat"] / score_detail["Jumlah"] * 100
        ).round(1)
        st.dataframe(score_detail)

with tab3:
    st.header("Analisis Geografis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Peta Sebaran Pengiriman")
        if len(filtered_geo) > 0:
            fig_geo = create_geo_scatter(filtered_geo)
            st.pyplot(fig_geo)
            plt.close()

            st.markdown(
                """
            **Insight:**
            - Pengiriman terkonsentrasi di wilayah selatan dan tenggara
            - Keterlambatan tersebar merata di seluruh wilayah
            - Tidak ada pola geografis spesifik untuk keterlambatan
            """
            )

    with col2:
        st.subheader("Persentase Keterlambatan per State")
        if len(filtered_geo) > 0:
            fig_late_pct = create_late_percentage_by_state(filtered_geo)
            st.pyplot(fig_late_pct)
            plt.close()

            st.markdown(
                """
            **Insight:**
            - Variasi keterlambatan antar state relatif kecil
            - State di atas rata-rata perlu perhatian khusus
            - Masalah bersifat sistemik, bukan regional
            """
            )

    st.subheader("Distribusi per State")
    if len(filtered_geo) > 0:
        fig_state = create_state_barplot(filtered_geo)
        st.pyplot(fig_state)
        plt.close()

    st.subheader("Rata-rata Waktu Pengiriman per State")
    if len(filtered_geo) > 0:
        fig_state_delivery = create_delivery_time_by_state(filtered_geo)
        st.pyplot(fig_state_delivery)
        plt.close()

        st.markdown(
            """
        **Insight:**
        - State dengan waktu pengiriman di atas rata-rata nasional perlu evaluasi
        - Perbedaan waktu pengiriman antar state relatif signifikan
        - Pertimbangkan optimasi rute logistik untuk state tertentu
        """
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Kota dengan Order Terbanyak")
        n_cities = st.slider("Jumlah kota", min_value=5, max_value=20, value=10)
        if len(filtered_geo) > 0:
            fig_cities = create_top_cities(filtered_geo, n=n_cities)
            st.pyplot(fig_cities)
            plt.close()

    with col2:
        st.subheader("Detail per State")
        if len(filtered_geo) > 0:
            state_detail = (
                filtered_geo.groupby("customer_state")
                .agg(
                    {
                        "order_id": "count",
                        "delivery_time": "mean",
                        "delivery_status": lambda x: (x == "Terlambat").sum(),
                    }
                )
                .round(2)
            )
            state_detail.columns = ["Total Order", "Mean Delivery", "Total Terlambat"]
            state_detail["Persen Terlambat"] = (
                state_detail["Total Terlambat"] / state_detail["Total Order"] * 100
            ).round(1)
            state_detail = state_detail.sort_values("Total Order", ascending=False)
            st.dataframe(state_detail, height=400)

with tab4:
    st.header("Analisis Tren")

    if (
        "order_purchase_timestamp" in filtered_reviews.columns
        and len(filtered_reviews) > 0
    ):
        st.subheader("Tren Bulanan")
        fig_trend = create_monthly_trend(filtered_reviews)
        st.pyplot(fig_trend)
        plt.close()

        st.markdown(
            """
        **Insight:**
        - Tren order menunjukkan pola pertumbuhan seiring waktu
        - Skor review relatif stabil sepanjang periode
        - Puncak order tertentu mungkin terkait event atau promo
        """
        )

        st.subheader("Detail per Bulan")
        monthly_df = filtered_reviews.copy()
        monthly_df["month"] = (
            monthly_df["order_purchase_timestamp"].dt.to_period("M").astype(str)
        )
        monthly_stats = (
            monthly_df.groupby("month")
            .agg(
                {
                    "order_id": "count",
                    "delivery_time": "mean",
                    "review_score": "mean",
                    "delivery_status": lambda x: (x == "Terlambat").sum(),
                }
            )
            .round(2)
        )
        monthly_stats.columns = [
            "Total Order",
            "Mean Delivery",
            "Mean Score",
            "Terlambat",
        ]
        monthly_stats["Persen Terlambat"] = (
            monthly_stats["Terlambat"] / monthly_stats["Total Order"] * 100
        ).round(1)
        st.dataframe(monthly_stats)

        st.subheader("Analisis per Hari dalam Seminggu")
        daily_df = filtered_reviews.copy()
        daily_df["day_name"] = daily_df["order_purchase_timestamp"].dt.day_name()
        day_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        fig_day, ax = plt.subplots(figsize=(12, 5))
        day_counts = daily_df["day_name"].value_counts().reindex(day_order)
        colors = plt.cm.Blues([0.3 + i * 0.1 for i in range(7)])
        ax.bar(day_counts.index, day_counts.values, color=colors)
        ax.set_title("Distribusi Order per Hari", fontsize=14, fontweight="bold")
        ax.set_xlabel("Hari", fontsize=12)
        ax.set_ylabel("Jumlah Order", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig_day)
        plt.close()

        st.markdown(
            """
        **Insight:**
        - Pola order bervariasi sepanjang minggu
        - Identifikasi hari dengan volume tertinggi untuk perencanaan kapasitas
        - Pertimbangkan promosi di hari dengan volume rendah
        """
        )
    else:
        st.warning("Data timestamp tidak tersedia untuk analisis tren")

# Kesimpulan
st.markdown("---")
st.header("Kesimpulan dan Rekomendasi")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    ### Pertanyaan 1: Waktu Pengiriman vs Kepuasan

    **Temuan:**
    - Korelasi negatif (-0.334) antara waktu pengiriman dan skor review
    - Pelanggan dengan pengiriman cepat memberikan skor lebih tinggi
    - Threshold optimal: pengiriman di bawah 10 hari

    **Rekomendasi:**
    - Optimalkan proses pengiriman untuk target di bawah 10 hari
    - Prioritaskan pengiriman untuk pelanggan yang sudah menunggu lama
    - Komunikasi proaktif jika terjadi keterlambatan
    """
    )

with col2:
    st.markdown(
        """
    ### Pertanyaan 2: Distribusi Keterlambatan Geografis

    **Temuan:**
    - Keterlambatan tersebar merata di seluruh wilayah
    - Tidak ada konsentrasi geografis spesifik
    - Masalah bersifat sistemik, bukan regional

    **Rekomendasi:**
    - Fokus perbaikan pada sistem logistik keseluruhan
    - Evaluasi mitra logistik secara berkala
    - Pertimbangkan penambahan gudang distribusi
    """
    )

# Footer
st.markdown("---")
st.caption("Dashboard Analisis E-Commerce Brasil - Irsan Indra Kusuma")

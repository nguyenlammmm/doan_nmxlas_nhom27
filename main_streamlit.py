import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Cấu hình trang ---
st.set_page_config(page_title="Lịch sử nhận diện", layout="wide")

# --- Đường dẫn file ---
LOG_PATH = "app/data/detections.csv"

# --- Sidebar ---
st.sidebar.header("Bộ lọc & Chức năng")
view_option = st.sidebar.radio("Chọn nội dung:", [
    "Dashboard tổng quan",
    "Dữ liệu chi tiết",
    "Phân bố cảm xúc",
    "Thống kê theo người",
    "Biểu đồ thời gian",
    "Xếp hạng theo cảm xúc"
])

# --- Đọc dữ liệu ---
if os.path.exists(LOG_PATH):
    df = pd.read_csv(LOG_PATH, names=["timestamp", "name", "emotion", "age", "gender"], skiprows=1)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Bộ lọc người dùng ---
    names = df["name"].unique().tolist()
    selected_names = st.sidebar.multiselect("Lọc theo tên:", names, default=names)
    df = df[df["name"].isin(selected_names)]

    # --- Bộ lọc giới tính ---
    genders = df["gender"].unique().tolist()
    selected_genders = st.sidebar.multiselect("Lọc theo giới tính:", genders, default=genders)
    df = df[df["gender"].isin(selected_genders)]

    # --- Bộ lọc thời gian ---
    min_time = df["timestamp"].min().to_pydatetime()
    max_time = df["timestamp"].max().to_pydatetime()
    start_time, end_time = st.sidebar.slider(
        "Chọn khoảng thời gian:",
        min_value=min_time,
        max_value=max_time,
        value=(min_time, max_time),
        format="YYYY-MM-DD HH:mm:ss"
    )
    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    # --- Nội dung chính ---
    if view_option == "Dashboard tổng quan":
        st.title("Tổng quan nhận diện")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng lượt nhận diện", len(df))
        col2.metric("Số người khác nhau", df['name'].nunique())
        col3.metric("Số cảm xúc ghi nhận", df['emotion'].nunique())

        st.subheader("Phân bố cảm xúc")
        st.bar_chart(df["emotion"].value_counts())

        st.subheader("Tuổi trung bình theo cảm xúc")
        st.bar_chart(df.groupby("emotion")["age"].mean())

        st.subheader("Phân bố cảm xúc theo giới tính")
        st.bar_chart(df.groupby(["gender", "emotion"]).size().unstack(fill_value=0))

    elif view_option == "Dữ liệu chi tiết":
        st.title("Bảng dữ liệu nhận diện")
        st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    elif view_option == "Phân bố cảm xúc":
        st.title("Biểu đồ tròn phân bố cảm xúc")
        counts = df["emotion"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

    elif view_option == "Thống kê theo người":
        st.title("Số lần nhận diện theo người")
        st.bar_chart(df["name"].value_counts())

    elif view_option == "Biểu đồ thời gian":
        st.title("Biểu đồ số lượt nhận diện theo thời gian (phút)")
        time_chart = df.set_index("timestamp").resample("1min").count()["name"]
        st.line_chart(time_chart)

    elif view_option == "Xếp hạng theo cảm xúc":
        st.title("Xếp hạng người theo cảm xúc")
        emotion_list = df["emotion"].unique().tolist()
        selected_emotion = st.selectbox("Chọn cảm xúc:", emotion_list)

        emo_df = df[df["emotion"] == selected_emotion]
        emo_count = emo_df["name"].value_counts()

        st.subheader(f"Số lần xuất hiện cảm xúc '{selected_emotion}'")
        st.bar_chart(emo_count)

        if not emo_count.empty:
            st.success(f"Nhiều nhất: {emo_count.idxmax()} ({emo_count.max()} lần)")
            st.info(f"Ít nhất: {emo_count.idxmin()} ({emo_count.min()} lần)")
        else:
            st.warning("Không có dữ liệu cho cảm xúc này.")
else:
    st.warning("Chưa có dữ liệu nhận diện để hiển thị.")

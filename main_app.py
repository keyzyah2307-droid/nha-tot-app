import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Nhà Tốt - Chuyên trang Bất động sản", 
    page_icon="🏠",
    layout="wide"
)

# --- 2. GIAO DIỆN (CSS TÙY CHỈNH NÂNG CAO) ---
st.markdown("""
    <style>
    /* Tổng thể */
    .main { background-color: #f8f9fa; }
    
    /* Thanh Header màu vàng đặc trưng của Nhà Tốt */
    .header-style {
        background-color: #ffba00;
        padding: 20px;
        border-radius: 10px;
        color: #222;
        margin-bottom: 30px;
        text-align: center;
    }

    /* Card nhà giống giao diện web */
    .house-card {
        background-color: white;
        padding: 0px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        transition: 0.3s;
        overflow: hidden;
    }
    .house-card:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.1); transform: translateY(-5px); }
    
    .card-content { padding: 12px; }
    .price-text { color: #d0021b; font-weight: bold; font-size: 17px; text-transform: uppercase; }
    .info-text { color: #777; font-size: 13px; margin: 5px 0; }
    .title-text { font-weight: 600; font-size: 15px; color: #222; line-height: 1.4; height: 42px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
    .location-text { font-size: 12px; color: #888; border-top: 1px solid #eee; padding-top: 8px; margin-top: 8px; }
    
    /* Nút bấm vàng */
    div.stButton > button {
        background-color: #ffba00;
        color: #222;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        width: 100%;
    }
    div.stButton > button:hover { background-color: #e5a700; color: #000; }

    /* Search bar container */
    .search-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: -50px;
        z-index: 99;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOAD DỮ LIỆU ---
@st.cache_resource
def load_data():
    df = pd.read_csv("final_master.csv")
    try:
        with open("nha_cosine_sim.pkl", "rb") as f:
            cosine_sim = pickle.load(f)
    except:
        cosine_sim = None
    return df, cosine_sim

df, cosine_sim = load_data()

# --- 4. SIDEBAR ---
try:
    st.sidebar.image("nhatot.jpg", use_container_width=True) # Thay bằng file banner của bạn
except:
    st.sidebar.markdown("## 🏠 NHÀ TỐT")

st.sidebar.markdown("---")
choice = st.sidebar.radio("KHÁM PHÁ", ["🏠 Trang chủ", "📈 Định giá AI", "🔍 Gợi ý thông minh", "📊 Phân tích"])

# --- 5. NỘI DUNG ---

if choice == "🏠 Trang chủ":
    # Hiển thị banner ở trên cùng
    st.image("nhatot.png", use_container_width=True)
    # Hero Section
    st.markdown('<div class="header-style"><h1>Tìm nhà tốt, chọn Nhà Tốt</h1><p>Hệ thống hỗ trợ tìm kiếm và phân tích bất động sản thông minh</p></div>', unsafe_allow_html=True)
    
    # Search & Filter Bar
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search_query = st.text_input("📍 Tìm kiếm khu vực, dự án...", placeholder="Ví dụ: Căn hộ Bình Thạnh...")
        with c2:
            q_filter = st.selectbox("Quận/Huyện", ["Tất cả"] + list(df['quan'].unique()))
        with c3:
            price_range = st.select_slider("Khoảng giá (Tỷ)", options=[0, 2, 5, 10, 20, 50], value=(0, 20))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Logic Lọc
    data_view = df.copy()
    if q_filter != "Tất cả":
        data_view = data_view[data_view['quan'] == q_filter]
    data_view = data_view[(data_view['gia_ban'] >= price_range[0]) & (data_view['gia_ban'] <= price_range[1])]
    
    st.subheader(f"🏠 Có {len(data_view)} bất động sản dành cho bạn")
    
# Hiển thị Grid
    items_per_page = 12
    # Lấy dữ liệu an toàn tránh lỗi index
    data_display = data_view.head(items_per_page)
    
# --- PHẦN HIỂN THỊ GRID TRONG TRANG CHỦ ---
    
    # Thiết lập số lượng tin hiển thị
    items_per_page = 12
    data_display = data_view.head(items_per_page)
    
    for i in range(0, len(data_display), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(data_display):
                row = data_display.iloc[i + j]
                
                with cols[j]:
                    # Bao bọc toàn bộ card trong một thẻ div để giữ style
                    st.markdown('<div class="house-card">', unsafe_allow_html=True)
                    
                    # 1. HIỂN THỊ ẢNH ĐỒNG NHẤT (nhatot.png)
                    try:
                        # Thử load file nội bộ, nếu lỗi (thiếu file) thì dùng màu nền xám
                        st.image("nhatot.png", use_container_width=True)
                    except:
                        st.markdown("""
                            <div style="width:100%; height:150px; background:#f0f0f0; 
                                 display:flex; align-items:center; justify-content:center; color:#ccc;">
                                🖼️ nhatot.png not found
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # 2. HIỂN THỊ NỘI DUNG CHI TIẾT
                    st.markdown(f"""
                        <div class="card-content" style="padding: 10px;">
                            <div class="title-text" style="font-weight:600; font-size:15px; height:42px; overflow:hidden;">
                                {row['loai_hinh']} tại {row['quan']}
                            </div>
                            <div class="info-text" style="color:#777; font-size:13px; margin:5px 0;">
                                {row['dien_tich']} m² • {int(row.get('so_phong_ngu', 0))} PN
                            </div>
                            <div class="price-text" style="color:#d0021b; font-weight:bold; font-size:18px;">
                                {row['gia_ban']} tỷ
                            </div>
                            <div class="location-text" style="font-size:12px; color:#888; border-top:1px solid #eee; padding-top:5px; margin-top:8px;">
                                📍 {row['quan']}, TP. Hồ Chí Minh
                            </div>
                        </div>
                        </div> """, unsafe_allow_html=True)

elif choice == "📈 Định giá AI":
    st.title("📈 Công cụ Định giá & Kiểm tra tin đăng")
    st.info("Sử dụng AI NHATOT để đối chiếu giá của bạn với giá thị trường hiện tại.")
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        with st.expander("📝 Thông tin chi tiết bất động sản", expanded=True):
            quan_box = st.selectbox("Chọn Quận", df['quan'].unique())
            loai_hinh = st.selectbox("Loại hình", df['loai_hinh'].unique())
            dt = st.number_input("Diện tích (m²)", 20, 500, 50)
            pn = st.number_input("Số phòng ngủ", 1, 10, 2)
            price_input = st.number_input("Giá bạn muốn đăng (Tỷ VNĐ)", 0.1, 100.0, 5.0)
            check_btn = st.button("KIỂM TRA ĐỘ HỢP LÝ")

    if check_btn:
        # Giả lập model predict
        pred_price = (dt * 0.12) + (pn * 0.5) 
        diff = (price_input - pred_price) / pred_price
        
        with col_r:
            st.metric("Giá trị ước tính từ AI", f"{pred_price:.2f} Tỷ", f"{diff:+.1%}")
            if diff > 0.2:
                st.warning("⚠️ **Giá cao hơn thị trường:** Tin đăng có thể khó tiếp cận người mua.")
            elif diff < -0.2:
                st.success("🔥 **Giá hời:** Tin đăng này sẽ thu hút rất nhiều lượt quan tâm!")
            else:
                st.info("✅ **Giá hợp lý:** Mức giá tương đồng với khu vực.")
            
            # Biểu đồ so sánh nhỏ
            fig, ax = plt.subplots(figsize=(5,3))
            sns.barplot(x=["Giá của bạn", "Giá thị trường"], y=[price_input, pred_price], palette=['#ffba00', '#eee'])
            st.pyplot(fig)

elif choice == "🔍 Gợi ý thông minh":
    st.title("🔍 Gợi ý nhà tương tự")
    
    if cosine_sim is not None:
        # KIỂM TRA ĐỘ DÀI MA TRẬN
        max_supported = len(cosine_sim)
        st.info(f"Hệ thống gợi ý hiện tại hỗ trợ {max_supported} căn nhà đầu tiên trong danh sách.")
        
        # Chỉ cho phép chọn trong phạm vi AI hỗ trợ để tránh lỗi Index
        df_limited = df.iloc[:max_supported]
        
        selected_id = st.selectbox(
            "Chọn căn nhà để tìm căn tương tự:", 
            options=df_limited.index,
            format_func=lambda x: f"ID {x}: {df_limited.loc[x, 'loai_hinh']} - {df_limited.loc[x, 'gia_ban']} tỷ"
        )
        
        # XỬ LÝ GỢI Ý AN TOÀN
        if selected_id < max_supported:
            sim_scores = list(enumerate(cosine_sim[selected_id]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:5]
            
            st.subheader("Kết quả gợi ý:")
            rcols = st.columns(4)
            for i, (sim_idx, score) in enumerate(sim_scores):
                if sim_idx < len(df):
                    item = df.iloc[sim_idx]
                    with rcols[i]:
                        st.markdown(f"""
                            <div class="house-card">
                                <div style="background:#fff3e0; color:#e65100; font-size:10px; padding:5px; font-weight:bold; text-align:center">TƯƠNG ĐỒNG {score:.0%}</div>
                                <div class="card-body">
                                    <div class="price-text">{item['gia_ban']} tỷ</div>
                                    <div style="font-size:12px;">{item['loai_hinh']}</div>
                                    <div style="font-size:11px; color:#888;">📍 {item['quan']}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
    else:
        st.error("Không tìm thấy file nha_cosine_sim.pkl")

    # Sử dụng Tabs để phân loại báo cáo
# --- BÁO CÁO & PHÂN TÍCH (Gộp lại cho gọn) ---
elif choice == "📊 Phân tích":
    st.title("📊 Phân tích thị trường")
    
    tab_m1, tab_m2, tab_m3 = st.tabs(["💰 Biểu đồ giá", "📍 Theo khu vực", "🎯 Phân khúc thị trường"])
    
    # Tab 1: Biểu đồ giá
    with tab_m1:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.write("#### Giá trung bình theo Quận")
            fig1, ax1 = plt.subplots()
            sns.barplot(data=df, x='quan', y='gia_ban', palette='YlOrBr', ax=ax1)
            st.pyplot(fig1)
        with col_c2:
            st.write("#### Phân bổ giá nhà (Tỷ VNĐ)")
            fig2, ax2 = plt.subplots()
            sns.histplot(df['gia_ban'], bins=30, kde=True, color='orange', ax=ax2)
            ax2.set_xlim(0, 40)
            st.pyplot(fig2)
            
        st.write("#### Phân bổ chi tiết (Boxenplot)")
        fig4 = plt.figure(figsize=(10, 4))
        sns.boxenplot(data=df, x='quan', y='gia_ban', palette='YlOrBr')
        st.pyplot(fig4)

    # Tab 2: Theo khu vực (Loại hình)
    with tab_m2:
        st.write("#### Tỷ trọng tin đăng theo loại hình")
        fig5 = plt.figure(figsize=(8, 5))
        df['loai_hinh'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#ffba00', '#ffd54f', '#fff176'])
        plt.ylabel("")
        st.pyplot(fig5)

    # Tab 3: Phân khúc (Scatter plot)
    with tab_m3:
        st.write("#### Mối tương quan giữa Diện tích & Giá (Phân cụm)")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=df, x='dien_tich', y='gia_ban', hue='quan', alpha=0.6, s=100, ax=ax3)
        ax3.set_title("Biểu đồ phân khúc theo khu vực")
        st.pyplot(fig3)

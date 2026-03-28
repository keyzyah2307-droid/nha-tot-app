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
        max_supported = len(cosine_sim)
        st.info(f"Hệ thống gợi ý hiện tại hỗ trợ {max_supported} căn nhà đầu tiên trong danh sách.")

        # Giới hạn dữ liệu theo ma trận cosine
        df_limited = df.iloc[:max_supported].copy()

        # =========================
        # CSS hiển thị đẹp hơn
        # =========================
        st.markdown("""
        <style>
        .section-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .sub-block {
            border-left: 5px solid #2f6f4f;
            padding-left: 12px;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 18px;
            font-weight: 700;
            color: #2c2c2c;
        }
        .house-card {
            border-radius: 16px;
            overflow: hidden;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 16px;
            border: 1px solid #eee;
        }
        .sim-header {
            background: #fff3e0;
            color: #e65100;
            font-size: 12px;
            padding: 6px;
            font-weight: bold;
            text-align: center;
        }
        .card-body {
            padding: 14px;
        }
        .price-text {
            color: #d32f2f;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .meta-text {
            font-size: 13px;
            color: #555;
            margin-bottom: 4px;
        }
        .tag-box {
            display: inline-block;
            background: #f3f4f6;
            color: #333;
            padding: 4px 8px;
            border-radius: 8px;
            font-size: 11px;
            margin-right: 6px;
            margin-top: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

        # =========================
        # Chuẩn hóa dữ liệu an toàn
        # =========================
        def safe_col(col_name, default_value="Không rõ"):
            return df_limited[col_name] if col_name in df_limited.columns else default_value

        # Các option cho selectbox
        quan_options = ["Tất cả"] + sorted(df_limited["quan"].dropna().astype(str).unique().tolist()) if "quan" in df_limited.columns else ["Tất cả"]
        loai_hinh_options = ["Tất cả"] + sorted(df_limited["loai_hinh"].dropna().astype(str).unique().tolist()) if "loai_hinh" in df_limited.columns else ["Tất cả"]
        noi_that_options = ["Tất cả"] + sorted(df_limited["tinh_trang_noi_that"].dropna().astype(str).unique().tolist()) if "tinh_trang_noi_that" in df_limited.columns else ["Tất cả"]

        # =========================
        # KHU VỰC NHẬP TIÊU CHÍ NHƯ HÌNH
        # =========================
        st.markdown('<div class="sub-block">📌 Thông tin căn nhà cần tìm</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            selected_quan = st.selectbox("Quận (ưu tiên)", quan_options, index=quan_options.index("Bình Thạnh") if "Bình Thạnh" in quan_options else 0)
        with c2:
            selected_loai_hinh = st.selectbox("Loại hình", loai_hinh_options, index=loai_hinh_options.index("Nhà ngõ, hẻm") if "Nhà ngõ, hẻm" in loai_hinh_options else 0)
        with c3:
            selected_noi_that = st.selectbox("Nội thất", noi_that_options, index=noi_that_options.index("Nội thất cao cấp") if "Nội thất cao cấp" in noi_that_options else 0)

        st.markdown('<div class="sub-block">📐 Kích thước & Phòng ốc</div>', unsafe_allow_html=True)

        d1, d2, d3, d4, d5 = st.columns(5)
        with d1:
            target_price = st.number_input("Giá (triệu)", min_value=0.0, value=5000.0, step=100.0)
        with d2:
            target_area = st.number_input("Diện tích (m²)", min_value=0.0, value=50.0, step=1.0)
        with d3:
            target_floors = st.number_input("Số tầng", min_value=0, value=3, step=1)
        with d4:
            target_bedrooms = st.number_input("Phòng ngủ", min_value=0, value=3, step=1)
        with d5:
            target_width = st.number_input("Ngang (m)", min_value=0.0, value=4.0, step=0.1)

        top_k = st.slider("Số nhà gợi ý (Top K)", min_value=1, max_value=10, value=5, step=1)

        # =========================
        # Chọn căn gốc để tìm tương tự
        # =========================
        st.markdown("### Chọn căn nhà tham chiếu")
        selected_id = st.selectbox(
            "Chọn căn nhà để tìm căn tương tự:",
            options=df_limited.index,
            format_func=lambda x: (
                f"ID {x} | "
                f"{df_limited.loc[x, 'loai_hinh'] if 'loai_hinh' in df_limited.columns else 'N/A'} | "
                f"{df_limited.loc[x, 'quan'] if 'quan' in df_limited.columns else 'N/A'} | "
                f"{df_limited.loc[x, 'gia_ban'] if 'gia_ban' in df_limited.columns else 'N/A'}"
            )
        )

        # =========================
        # Lọc ứng viên theo form nhập
        # =========================
        candidate_df = df_limited.copy()

        if selected_quan != "Tất cả" and "quan" in candidate_df.columns:
            candidate_df = candidate_df[candidate_df["quan"].astype(str) == selected_quan]

        if selected_loai_hinh != "Tất cả" and "loai_hinh" in candidate_df.columns:
            candidate_df = candidate_df[candidate_df["loai_hinh"].astype(str) == selected_loai_hinh]

        if selected_noi_that != "Tất cả" and "tinh_trang_noi_that" in candidate_df.columns:
            candidate_df = candidate_df[candidate_df["tinh_trang_noi_that"].astype(str) == selected_noi_that]

        # Lọc khoảng gần đúng cho biến số
        if "gia_ban" in candidate_df.columns:
            candidate_df = candidate_df[
                pd.to_numeric(candidate_df["gia_ban"], errors="coerce").between(target_price * 0.7, target_price * 1.3)
            ]

        if "dien_tich" in candidate_df.columns:
            candidate_df = candidate_df[
                pd.to_numeric(candidate_df["dien_tich"], errors="coerce").between(target_area * 0.7, target_area * 1.3)
            ]

        if "tong_so_tang" in candidate_df.columns:
            candidate_df = candidate_df[
                pd.to_numeric(candidate_df["tong_so_tang"], errors="coerce").between(max(0, target_floors - 1), target_floors + 1)
            ]

        if "so_phong_ngu" in candidate_df.columns:
            candidate_df = candidate_df[
                pd.to_numeric(candidate_df["so_phong_ngu"], errors="coerce").between(max(0, target_bedrooms - 1), target_bedrooms + 1)
            ]

        if "chieu_ngang" in candidate_df.columns:
            candidate_df = candidate_df[
                pd.to_numeric(candidate_df["chieu_ngang"], errors="coerce").between(target_width * 0.7, target_width * 1.3)
            ]

        # =========================
        # Tính cosine similarity
        # =========================
        if selected_id < max_supported:
            sim_scores = list(enumerate(cosine_sim[selected_id]))

            # Bỏ chính nó
            sim_scores = [(idx, score) for idx, score in sim_scores if idx != selected_id]

            # Chỉ giữ những căn còn nằm trong candidate_df
            valid_indices = set(candidate_df.index)
            sim_scores = [(idx, score) for idx, score in sim_scores if idx in valid_indices]

            # Sắp xếp giảm dần theo độ tương đồng
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:top_k]

            st.subheader("Kết quả gợi ý")

            if len(sim_scores) == 0:
                st.warning("Không tìm thấy căn nhà phù hợp với tiêu chí đã chọn.")
            else:
                cols = st.columns(min(top_k, 4))
                for i, (sim_idx, score) in enumerate(sim_scores):
                    item = df_limited.loc[sim_idx]

                    gia_ban = item["gia_ban"] if "gia_ban" in df_limited.columns else "N/A"
                    loai_hinh = item["loai_hinh"] if "loai_hinh" in df_limited.columns else "N/A"
                    quan = item["quan"] if "quan" in df_limited.columns else "N/A"
                    dien_tich = item["dien_tich"] if "dien_tich" in df_limited.columns else "N/A"
                    so_phong_ngu = item["so_phong_ngu"] if "so_phong_ngu" in df_limited.columns else "N/A"
                    tong_so_tang = item["tong_so_tang"] if "tong_so_tang" in df_limited.columns else "N/A"
                    chieu_ngang = item["chieu_ngang"] if "chieu_ngang" in df_limited.columns else "N/A"
                    noi_that = item["tinh_trang_noi_that"] if "tinh_trang_noi_that" in df_limited.columns else "N/A"

                    with cols[i % len(cols)]:
                        st.markdown(f"""
                        <div class="house-card">
                            <div class="sim-header">TƯƠNG ĐỒNG {score:.0%}</div>
                            <div class="card-body">
                                <div class="price-text">{gia_ban} triệu</div>
                                <div class="meta-text"><b>Loại hình:</b> {loai_hinh}</div>
                                <div class="meta-text"><b>Quận:</b> {quan}</div>
                                <div class="meta-text"><b>Diện tích:</b> {dien_tich} m²</div>
                                <div class="meta-text"><b>Phòng ngủ:</b> {so_phong_ngu}</div>
                                <div class="meta-text"><b>Số tầng:</b> {tong_so_tang}</div>
                                <div class="meta-text"><b>Ngang:</b> {chieu_ngang} m</div>
                                <div class="meta-text"><b>Nội thất:</b> {noi_that}</div>
                                <div class="tag-box">ID: {sim_idx}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # =========================
                # Bảng chi tiết bên dưới
                # =========================
                st.markdown("### Bảng chi tiết")
                result_rows = []
                for sim_idx, score in sim_scores:
                    item = df_limited.loc[sim_idx]
                    result_rows.append({
                        "ID": sim_idx,
                        "Độ tương đồng": f"{score:.2%}",
                        "Quận": item["quan"] if "quan" in df_limited.columns else None,
                        "Loại hình": item["loai_hinh"] if "loai_hinh" in df_limited.columns else None,
                        "Giá": item["gia_ban"] if "gia_ban" in df_limited.columns else None,
                        "Diện tích": item["dien_tich"] if "dien_tich" in df_limited.columns else None,
                        "Phòng ngủ": item["so_phong_ngu"] if "so_phong_ngu" in df_limited.columns else None,
                        "Số tầng": item["tong_so_tang"] if "tong_so_tang" in df_limited.columns else None,
                        "Ngang": item["chieu_ngang"] if "chieu_ngang" in df_limited.columns else None,
                        "Nội thất": item["tinh_trang_noi_that"] if "tinh_trang_noi_that" in df_limited.columns else None
                    })

                st.dataframe(pd.DataFrame(result_rows), use_container_width=True)

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

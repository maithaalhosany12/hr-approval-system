import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة وتوسيع العرض
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="expanded")

# 2. التنسيق الشامل (الدزاين القديم + الحقول القصيرة)
st.markdown("""
    <style>
    /* التوجه العام */
    .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f9; }
    
    /* الشريط الجانبي - Sidebar */
    [data-testid="stSidebar"] { background-color: white !important; direction: rtl !important; }
    
    /* تقليص عرض الحاوية */
    .block-container { max-width: 1000px !important; padding-top: 1rem; }

    /* الهيدر الرسمي في المنتصف */
    .header-box {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background: white; padding: 15px; border-radius: 15px; margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center;
    }
    .header-box img { width: 50px; margin-bottom: 8px; }

    /* السلم الجانبي (التصميم القديم) */
    .step-container { position: relative; padding-right: 65px; margin-bottom: 30px; }
    .step-line {
        position: absolute; right: 30px; top: 40px; bottom: -40px;
        width: 3px; background: #5d5fef; opacity: 0.2; z-index: 1;
    }
    .step-container:last-child .step-line { display: none; }
    
    .step-circle {
        position: absolute; right: 10px; top: 0;
        width: 42px; height: 42px; border-radius: 50%;
        background: #5d5fef; color: white; display: flex;
        align-items: center; justify-content: center; font-weight: bold;
        font-size: 18px; z-index: 2; box-shadow: 0 4px 10px rgba(93,95,239,0.3);
    }

    /* البطاقة والعناوين */
    .content-card { 
        background: white; border-radius: 15px; overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04); border: 1px solid #eef0f2;
    }
    .step-title-bar { 
        background: linear-gradient(90deg, #5d5fef, #7a7cfc); 
        color: white; padding: 10px 25px; font-size: 16px; font-weight: bold;
    }
    .form-padding { padding: 20px 25px; }

    /* مربعات التعبئة القصيرة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 35px !important; height: 35px !important;
        text-align: right !important; border-radius: 8px !important;
    }
    label { font-size: 13px !important; font-weight: bold !important; color: #475569 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. محتوى الشريط الجانبي (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/281/281764.png", width=50)
    st.title("القائمة الرئيسية")
    menu = st.radio("انتقل إلى:", ["تقديم طلب جديد", "تتبع حالة الطلبات"])
    st.divider()
    st.info("نظام الموارد البشرية V2.0")

# 4. الهيدر في الصفحة الرئيسية
st.markdown("""
    <div class="header-box">
        <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png">
        <h2 style="margin:0; font-size:22px;">مؤسسة المسار المتكامل</h2>
        <p style="margin:0; color:#5d5fef; font-weight:bold;">نموذج طلبات شؤون الموظفين</p>
    </div>
    """, unsafe_allow_html=True)

# --- محتوى النموذج ---
if menu == "تقديم طلب جديد":
    
    # الخطوة 1
    st.markdown('<div class="step-container"><div class="step-circle">1</div><div class="step-line"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-card"><div class="step-title-bar">👤 الخطوة الأولى: البيانات الشخصية</div><div class="form-padding">', unsafe_allow_html=True)
        # الحقول بجانب بعضها لتقصير المساحة
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.text_input("الرقم الوظيفي")
        with c2: st.text_input("الاسم الكامل")
        with c3: st.text_input("المسمى")
        with c4: st.text_input("القسم")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-container"><div class="step-circle">2</div><div class="step-line"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-card"><div class="step-title-bar">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-padding">', unsafe_allow_html=True)
        c5, c6, c7 = st.columns([1, 1, 2])
        with c5: st.selectbox("نوع الطلب", ["نقل", "تعديل", "أخرى"])
        with c6: st.date_input("التاريخ", value=datetime.now(), disabled=True)
        with c7: st.text_input("ملاحظات إضافية")
        
        st.markdown("<br><b>✍️ التوقيع والموافقة</b>", unsafe_allow_html=True)
        c8, c9 = st.columns([3, 1])
        with c8: st.file_uploader("ارفق صورة التوقيع", type=['png', 'jpg'], label_visibility="collapsed")
        with c9: st.button("إرسال الآن", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
else:
    st.markdown("<h3>🔍 تتبع طلباتك</h3>", unsafe_allow_html=True)
    st.write("لا توجد طلبات سابقة لعرضها حالياً.")

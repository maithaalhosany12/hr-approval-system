import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS لتقليص عرض الحقول وضمان اتجاه اليمين
st.markdown("""
    <style>
    .main { direction: rtl !important; text-align: right !important; background-color: #f8fafc; }
    div[data-testid="stVerticalBlock"] { direction: rtl !important; gap: 0.5rem !important; }
    
    /* تحديد عرض النموذج ليكون ملموماً */
    .block-container { max-width: 950px !important; padding-top: 1rem; }

    /* الهيدر */
    .header-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background: white; padding: 10px; border-radius: 12px; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;
    }
    .header-container img { width: 40px; margin-bottom: 5px; }
    .header-container h1 { margin: 0; font-size: 18px; color: #1e293b; }

    /* بطاقة الخطوات */
    .step-card {
        background: white; border-radius: 10px; overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;
        margin-bottom: 15px; direction: rtl;
    }

    /* شريط العنوان */
    .step-bar {
        background: linear-gradient(90deg, #5d5fef, #7a7cfc);
        color: white; padding: 8px 20px; display: flex;
        justify-content: space-between; align-items: center;
    }
    .step-num {
        width: 25px; height: 25px; background: rgba(255,255,255,0.2);
        border: 1px solid white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; font-size: 13px;
    }

    /* تقصير عرض وطول المربعات */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 30px !important; height: 30px !important;
        text-align: right !important; font-size: 13px !important;
        border-radius: 6px !important;
    }

    label { font-size: 12px !important; font-weight: 600 !important; margin-bottom: 2px !important; }
    .body-padding { padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 3. الهيدر
st.markdown("""
    <div class="header-container">
        <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png">
        <h1>مؤسسة المسار المتكامل</h1>
        <p style="margin:0; font-size:11px; color:#5d5fef;">قسم شؤون الموظفين</p>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة الأولى: النموذج بحقول متجاورة ---
if st.session_state.page == 'form':
    
    # الخطوة 1: بيانات الموظف (4 حقول في سطر واحد)
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-bar"><span>👤 بيانات مقدم الطلب</span><div class="step-num">1</div></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="body-padding">', unsafe_allow_html=True)
        # تقسيم السطر إلى 4 أعمدة لجعل الحقول قصيرة جداً وبجانب بعضها
        c1, c2, c3, c4 = st.columns(4)
        with c1: job_num = st.text_input("الرقم الوظيفي")
        with c2: name = st.text_input("الاسم الكامل")
        with c3: title = st.text_input("المسمى")
        with c4: dept = st.text_input("القسم")
        st.markdown('</div></div></div>', unsafe_allow_html=True)

    # الخطوة 2: تفاصيل الطلب (حقول مدمجة)
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-bar"><span>📝 تفاصيل الطلب</span><div class="step-num">2</div></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="body-padding">', unsafe_allow_html=True)
        
        # وضع نوع الطلب والتاريخ والملاحظات في سطر واحد مقسم
        c5, c6, c7 = st.columns([1, 1, 2])
        with c5: req_type = st.selectbox("نوع الطلب", ["نقل", "تعديل مهنة", "استقالة"])
        with c6: eff_date = st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        with c7: notes = st.text_input("ملاحظات إضافية")
        
        # سطر التوقيع والزر
        st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)
        c8, c9 = st.columns([3, 1])
        with c8: sig_file = st.file_uploader("ارفع صورة التوقيع الرقمي", type=['png', 'jpg'], label_visibility="collapsed")
        with c9: 
            st.markdown("<div style='height:0px;'></div>", unsafe_allow_html=True)
            submit = st.button("إرسال الطلب", use_container_width=True)
        
        if submit:
            if job_num and name and sig_file:
                st.toast("✅ تم الإرسال بنجاح")
                time.sleep(0.5)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("أكمل البيانات")
        st.markdown('</div></div></div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.markdown("<h5 style='text-align:right;'>🔍 حالة الطلب</h5>", unsafe_allow_html=True)
    st.info("طلبك قيد المعالجة الآن.")
    if st.button("عودة"):
        st.session_state.page = 'form'
        st.rerun()

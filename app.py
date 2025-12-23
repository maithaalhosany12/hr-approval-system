import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS: ضغط مساحات التعبئة والمسافات البينية
st.markdown("""
    <style>
    /* الاتجاه العام وتقليص الحواف العلوية والسفلية */
    .main { background-color: #f4f7f9; direction: rtl; }
    .block-container { max-width: 800px !important; padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* تقليص ارتفاع مربعات التعبئة لأقصى حد (28px) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 28px !important; height: 28px !important;
        padding: 0px 8px !important; font-size: 13px !important;
        text-align: right; border-radius: 6px !important;
    }

    /* تقليل المسافات بين الحقول (Vertical Gap) */
    div[data-testid="stVerticalBlock"] { gap: 0.4rem !important; }

    /* الهيدر المدمج */
    .official-header {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background-color: white; padding: 10px; border-radius: 12px; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;
    }
    .header-logo img { width: 40px; margin-bottom: 5px; }
    .header-text h1 { margin: 0; font-size: 17px; color: #2d3436; font-weight: bold; }
    .header-text p { margin: 0; font-size: 11px; color: #5d5fef; }

    /* بطاقة المحتوى المدمجة */
    .content-box { 
        background-color: white; border-radius: 10px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); overflow: hidden; 
        border: 1px solid #eef0f2; margin-bottom: 12px;
    }

    .step-header { 
        background: linear-gradient(90deg, #5d5fef, #7a7cfc); 
        color: white; padding: 6px 15px; font-size: 14px; font-weight: bold;
        display: flex; justify-content: space-between; align-items: center;
    }

    .step-number-circle {
        background-color: rgba(255, 255, 255, 0.2);
        width: 24px; height: 24px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; border: 1px solid white;
    }

    .form-body { padding: 12px 20px; text-align: right; }

    /* تصغير حجم خطوط العناوين (Labels) */
    label { font-size: 13px !important; margin-bottom: 2px !important; }

    /* تصغير زر الإرسال */
    .stButton>button { height: 2.2em !important; padding: 0 20px !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 3. الهيدر المدمج
st.markdown("""
    <div class="official-header">
        <div class="header-logo">
            <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" alt="Logo">
        </div>
        <div class="header-text">
            <h1>مؤسسة المسار المتكامل</h1>
            <p>قسم شؤون الموظفين - نموذج الطلبات</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج المدمجة ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    with st.container():
        st.markdown('''
            <div class="content-box">
                <div class="step-header">
                    <span>👤 بيانات مقدم الطلب</span>
                    <div class="step-number-circle">1</div>
                </div>
                <div class="form-body">
        ''', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        job_num = c1.text_input("الرقم الوظيفي")
        full_name = c2.text_input("الاسم الكامل")
        
        c3, c4 = st.columns(2)
        job_title = c3.text_input("المسمى الوظيفي")
        unit = c4.text_input("الوحدة / القسم")
        st.markdown('</div></div>', unsafe_allow_html=True)

    # الخطوة 2
    with st.container():
        st.markdown('''
            <div class="content-box">
                <div class="step-header">
                    <span>📝 تفاصيل الطلب</span>
                    <div class="step-number-circle">2</div>
                </div>
                <div class="form-body">
        ''', unsafe_allow_html=True)
        
        c5, c6 = st.columns(2)
        req_type = c5.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        eff_date = c6.date_input("تاريخ السريان (تلقائي)", value=datetime.now(), disabled=True)
        
        st.markdown("<div style='text-align:right; font-size:12px; font-weight:bold; margin-top:5px;'>✍️ ارفع صورة التوقيع</div>", unsafe_allow_html=True)
        sig_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        notes = st.text_input("ملاحظات إضافية")
        
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("إرسال الطلب الآن"):
            if job_num and full_name and sig_file:
                st.toast("✅ تم الإرسال!", icon="🎉")
                time.sleep(0.5)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ أكمل البيانات")
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- صفحة التتبع المدمجة ---
elif st.session_state.page == 'tracking':
    st.markdown("<h5 style='text-align:right;'>🔍 حالة الطلب</h5>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; justify-content: space-around; background: white; padding: 15px; border-radius: 10px; direction: rtl;">
            <div style="text-align: center;"><div style="width:15px; height:15px; background:#5d5fef; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">تم التقديم</div></div>
            <div style="text-align: center;"><div style="width:15px; height:15px; background:#5d5fef; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">مراجعة</div></div>
            <div style="text-align: center;"><div style="width:15px; height:15px; background:#ddd; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">اعتماد</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("العودة"):
        st.session_state.page = 'form'
        st.rerun()

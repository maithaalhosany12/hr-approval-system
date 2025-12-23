import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة (نفس العرض والنمط القديم)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS القديم (الفخم) مع تعديل عرض الحقول فقط
st.markdown("""
    <style>
    /* التوجه العام */
    .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f9; }
    
    /* تقليص عرض الحاوية ليكون التصميم ملموم في الوسط */
    .block-container { max-width: 950px !important; padding-top: 2rem; }

    /* الهيدر القديم (المسمى يمين والشعار بجانبه) */
    .company-header {
        display: flex; align-items: center; justify-content: flex-start;
        padding: 15px 25px; background: white; border-radius: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }
    .header-logo { margin-left: 15px; }
    .header-logo img { width: 45px; }
    .header-text h1 { margin: 0; font-size: 19px; color: #2d3436; font-weight: bold; }
    .header-text p { margin: 0; font-size: 12px; color: #666; }

    /* الخط الجانبي والدوائر المرقمة (الدزاين القديم) */
    .step-block { position: relative; padding-right: 60px; margin-bottom: 30px; }
    .step-block::before {
        content: ""; position: absolute; right: 28px; top: 45px; bottom: -45px;
        width: 3px; background-color: #5d5fef; z-index: 1; opacity: 0.2;
    }
    .step-block:last-child::before { display: none; }

    .step-icon {
        position: absolute; right: 8px; top: 0;
        width: 42px; height: 42px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 18px;
        box-shadow: 0 4px 10px rgba(93,95,239,0.3);
    }

    /* بطاقة المحتوى والعناوين الملونة */
    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { 
        background: linear-gradient(90deg, #5d5fef, #7a7cfc); 
        color: white; padding: 12px 25px; font-size: 16px; font-weight: bold;
        display: flex; justify-content: space-between; align-items: center;
    }
    .step-number-circle {
        background-color: rgba(255, 255, 255, 0.2);
        width: 28px; height: 28px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; border: 1px solid white;
    }
    .form-body { padding: 25px; }

    /* تقصير عرض مربعات التعبئة بجعلها نحيفة ومنظمة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 35px !important; height: 35px !important;
        text-align: right !important; font-size: 14px !important;
        border-radius: 8px !important;
    }
    label { font-size: 13px !important; font-weight: bold !important; margin-bottom: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر القديم الفخم
st.markdown("""
    <div class="company-header">
        <div class="header-logo">
            <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png">
        </div>
        <div class="header-text">
            <h1>مؤسسة المسار المتكامل</h1>
            <p>قسم الموارد البشرية - نموذج الطلبات الإلكتروني</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

with st.sidebar:
    st.title("القائمة")
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('''
            <div class="content-box">
                <div class="step-header">
                    <span>👤 الخطوة الأولى: بيانات مقدم الطلب</span>
                    <div class="step-number-circle">1</div>
                </div>
                <div class="form-body">
        ''', unsafe_allow_html=True)
        # تقسيم الحقول لأعمدة لتقصير عرضها
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.text_input("الرقم الوظيفي")
        with c2: st.text_input("الاسم الكامل")
        with c3: st.text_input("المسمى")
        with c4: st.text_input("القسم")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('''
            <div class="content-box">
                <div class="step-header">
                    <span>📝 الخطوة الثانية: تفاصيل الطلب</span>
                    <div class="step-number-circle">2</div>
                </div>
                <div class="form-body">
        ''', unsafe_allow_html=True)
        c5, c6, c7 = st.columns([1, 1, 2])
        with c5: st.selectbox("نوع الطلب", ["نقل", "تعديل", "إنهاء"])
        with c6: st.date_input("التاريخ", value=datetime.now(), disabled=True)
        with c7: st.text_input("ملاحظات إضافية")
        
        st.markdown("<br><b>✍️ التوقيع الرقمي</b>", unsafe_allow_html=True)
        c8, c9 = st.columns([3, 1])
        with c8: st.file_uploader("", type=['png', 'jpg'], label_visibility="collapsed")
        with c9: st.button("إرسال الطلب", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.info("جاري مراجعة طلبك...")
    if st.button("رجوع"):
        st.session_state.page = 'form'
        st.rerun()

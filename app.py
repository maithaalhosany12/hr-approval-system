import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة (التصميم الأصلي الفخم)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS: الحفاظ على الاتجاه لليمين + تقصير الحقول بجانب بعضها
st.markdown("""
    <style>
    /* التوجه العام لليمين */
    .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f9; }
    
    /* تقليص عرض الحاوية ليكون التصميم ملموم */
    .block-container { max-width: 1050px !important; padding-top: 1.5rem; }

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
        color: white; padding: 10px 25px; font-size: 15px; font-weight: bold;
        display: flex; justify-content: space-between; align-items: center;
    }
    .step-number-circle {
        background-color: rgba(255, 255, 255, 0.2);
        width: 26px; height: 26px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 13px; border: 1px solid white;
    }
    .form-body { padding: 20px 25px; }

    /* تقصير عرض وطول مربعات التعبئة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 32px !important; height: 32px !important;
        text-align: right !important; font-size: 13px !important;
        border-radius: 8px !important;
    }
    label { font-size: 12px !important; font-weight: bold !important; margin-bottom: 4px !important; color: #475569 !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر الرسمي
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

# القائمة الجانبية
with st.sidebar:
    st.title("القائمة")
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج ---
if st.session_state.page == 'form':
    
    # الخطوة 1: بيانات مقدم الطلب (مع إضافة تاريخ التعيين وتوزيع الحقول بجانب بعضها)
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
        
        # توزيع الحقول الـ 5 في سطر واحد لتكون "قصيرة"
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.text_input("الرقم الوظيفي")
        with c2: st.text_input("الاسم الكامل")
        with c3: st.text_input("المسمى")
        with c4: st.text_input("القسم")
        with c5: st.date_input("تاريخ التعيين") # الحقل الجديد
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2: تفاصيل الطلب
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
        
        c6, c7, c8 = st.columns([1, 1, 2])
        with c6: st.selectbox("نوع الطلب", ["نقل", "تعديل مهنة", "إنهاء خدمة"])
        with c7: st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        with c8: st.text_input("ملاحظات إضافية")
        
        st.markdown("<div style='margin-top:15px;'><b>✍️ التوقيع الرقمي</b></div>", unsafe_allow_html=True)
        c9, c10 = st.columns([3, 1])
        with c9: st.file_uploader("", type=['png', 'jpg'], label_visibility="collapsed")
        with c10: 
            st.markdown("<div style='height:0px;'></div>", unsafe_allow_html=True)
            if st.button("إرسال الطلب", use_container_width=True):
                st.toast("✅ تم الإرسال")
                time.sleep(0.5)
                st.session_state.page = 'tracking'
                st.rerun()
                
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.info("طلبك قيد المراجعة حالياً.")
    if st.button("العودة"):
        st.session_state.page = 'form'
        st.rerun()

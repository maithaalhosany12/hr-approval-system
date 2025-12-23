import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS: العودة للتصميم الفخم مع ضبط الهيدر
st.markdown("""
    <style>
    /* الاتجاه العام للموقع من اليمين لليسار */
    .main { background-color: #f4f7f9; direction: rtl; }
    [data-testid="stSidebar"] { direction: rtl; }

    /* تقليص عرض الحاوية لتكون ملمومة في المنتصف */
    .block-container { max-width: 850px !important; padding-top: 1.5rem; }

    /* الهيدر: الشعار في المنتصف والكتابة متصلة به */
    .official-header {
        display: flex;
        flex-direction: column; /* ترتيب رأسي لجعل الشعار فوق النص أو بجانبه */
        align-items: center;
        justify-content: center;
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
    }
    .header-logo img { width: 50px; margin-bottom: 10px; }
    .header-text h1 { margin: 0; font-size: 20px; color: #2d3436; font-weight: bold; }
    .header-text p { margin: 0; font-size: 13px; color: #5d5fef; font-weight: 600; }

    /* بطاقة المحتوى (الشكل القديم) */
    .content-box { 
        background-color: white; border-radius: 15px; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; 
        border: 1px solid #eef0f2; margin-bottom: 25px;
        direction: rtl;
    }

    /* شريط العنوان مع الرقم على اليسار */
    .step-header { 
        background: linear-gradient(90deg, #5d5fef, #7a7cfc); 
        color: white; padding: 12px 25px; font-size: 16px; font-weight: bold;
        display: flex; justify-content: space-between; align-items: center;
    }

    .step-number-circle {
        background-color: rgba(255, 255, 255, 0.2);
        width: 30px; height: 30px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; border: 1px solid white;
    }

    .form-body { padding: 25px; text-align: right; }

    /* تقليص مساحة مربعات التعبئة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 35px !important; height: 35px !important;
        padding: 0px 10px !important; font-size: 14px !important;
        text-align: right; border-radius: 8px !important;
    }

    /* ضمان محاذاة التسميات لليمين */
    label { text-align: right !important; width: 100%; display: block !important; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 3. الهيدر الرسمي (الشعار والنص في المنتصف)
st.markdown("""
    <div class="official-header">
        <div class="header-logo">
            <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" alt="Logo">
        </div>
        <div class="header-text">
            <h1>مؤسسة المسار المتكامل</h1>
            <p>قسم شؤون الموظفين - نموذج الطلبات الإلكتروني</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية (Drop-down فقط)
with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    with st.container():
        st.markdown('''
            <div class="content-box">
                <div class="step-header">
                    <span>👤 الخطوة الأولى: بيانات مقدم الطلب</span>
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
                    <span>📝 الخطوة الثانية: تفاصيل موضوع الطلب</span>
                    <div class="step-number-circle">2</div>
                </div>
                <div class="form-body">
        ''', unsafe_allow_html=True)
        
        c5, c6 = st.columns(2)
        req_type = c5.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        eff_date = c6.date_input("تاريخ سريان الطلب (تلقائي)", value=datetime.now(), disabled=True)
        
        st.markdown("<div style='text-align:right; font-size:14px; font-weight:bold; margin-top:10px;'>✍️ ارفع صورة التوقيع الرقمي</div>", unsafe_allow_html=True)
        sig_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        notes = st.text_input("ملاحظات إضافية")
        
        st.markdown("<br>", unsafe_allow_html=True)
        c_btn, _ = st.columns([1, 3])
        if c_btn.button("إرسال الطلب الآن"):
            if job_num and full_name and sig_file:
                st.toast("✅ تم إرسال طلبك بنجاح!", icon="🎉")
                time.sleep(0.8)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى تعبئة الحقول ورفع التوقيع")
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.markdown("<h4 style='text-align:right; margin-bottom:20px;'>🔍 تتبع حالة الطلب</h4>", unsafe_allow_html=True)
    
    # Timeline
    st.markdown("""
        <div style="display: flex; justify-content: space-around; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); direction: rtl; margin-bottom: 20px;">
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#5d5fef; border-radius:50%; margin: 0 auto 10px; box-shadow: 0 0 10px #5d5fef;"></div><div style="font-size:13px; font-weight:bold;">تم التقديم</div></div>
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#5d5fef; border-radius:50%; margin: 0 auto 10px; box-shadow: 0 0 10px #5d5fef;"></div><div style="font-size:13px; font-weight:bold;">مراجعة HR</div></div>
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#ddd; border-radius:50%; margin: 0 auto 10px;"></div><div style="font-size:13px; font-weight:bold;">الاعتماد</div></div>
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#ddd; border-radius:50%; margin: 0 auto 10px;"></div><div style="font-size:13px; font-weight:bold;">الاكتمال</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.success("الطلب الآن في مرحلة المراجعة الفنية لدى الموارد البشرية.")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'form'
        st.rerun()

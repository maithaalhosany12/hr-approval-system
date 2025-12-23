import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS: نقل الأرقام لليسار، إزالة تاريخ الهيدر، والمحاذاة لليمين
st.markdown("""
    <style>
    /* إعدادات الصفحة العامة (يمين لليسار) */
    .main { background-color: #f4f7f9; direction: rtl; }
    
    /* تقليص عرض الحاوية لتكون ملمومة */
    .block-container { max-width: 850px !important; padding-top: 1.5rem; }

    /* هيدر الشركة بدون تاريخ */
    .company-header {
        display: flex; align-items: center; 
        padding: 12px 20px; background: white; border-radius: 12px; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }

    /* بطاقة المحتوى */
    .content-box { 
        background-color: white; border-radius: 12px; 
        box-shadow: 0 6px 15px rgba(0,0,0,0.04); overflow: hidden; 
        border: 1px solid #eef0f2; margin-bottom: 20px;
    }

    /* شريط العنوان مع الرقم على اليسار */
    .step-header { 
        background: linear-gradient(90deg, #5d5fef, #7a7cfc); 
        color: white; padding: 10px 20px; font-size: 16px; font-weight: bold;
        display: flex; justify-content: space-between; align-items: center;
        direction: rtl;
    }

    /* دائرة الرقم لتكون على يسار العنوان */
    .step-number-circle {
        background-color: rgba(255, 255, 255, 0.2);
        width: 28px; height: 28px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; border: 1px solid white;
    }

    .form-body { padding: 20px; text-align: right; }

    /* تصغير حجم مربعات التعبئة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 32px !important; height: 32px !important;
        padding: 0px 10px !important; font-size: 14px !important;
        text-align: right; border-radius: 8px !important;
    }

    /* مراجعة النصوص لتكون لليمين */
    label { text-align: right !important; width: 100%; display: block !important; margin-bottom: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 5. هيدر الشركة المحدث (بدون تاريخ)
st.markdown(f"""
    <div class="company-header">
        <div style="display: flex; align-items: center;">
            <div style="background:#5d5fef; padding:6px; border-radius:8px; margin-left:12px; display:flex;">
                <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" width="24" style="filter: brightness(0) invert(1);">
            </div>
            <div>
                <div style="font-weight: bold; font-size: 17px; color: #2d3436;"></div>
                <div style="font-size: 12px; color: #666;">قسم الموارد البشرية</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية
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
                    <span>  بيانات مقدم الطلب</span>
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
                    <span> تفاصيل موضوع الطلب</span>
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
        # زر الإرسال
        c_btn, _ = st.columns([1, 3])
        if c_btn.button("إرسال الطلب الآن"):
            if job_num and full_name and sig_file:
                st.toast("✅ تم إرسال طلبك بنجاح!", icon="🎉")
                time.sleep(0.8)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى تعبئة الحقول المطلوبة ورفع التوقيع")
                
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.markdown("<h5 style='text-align:right;'>🔍 حالة الطلب</h5>", unsafe_allow_html=True)
    st.info("الطلب قيد المراجعة الفنية.")
    if st.button("العودة"):
        st.session_state.page = 'form'
        st.rerun()


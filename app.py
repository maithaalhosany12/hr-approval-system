import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS: تقليص عرض المربعات وتنسيق التصميم
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    
    /* تقليص الارتفاع وتحسين شكل الحقول */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 32px !important;
        height: 32px !important;
        padding: 0px 10px !important;
        font-size: 14px !important;
        border-radius: 8px !important;
    }

    /* هيدر الشركة */
    .company-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 25px; background: white; border-radius: 12px; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }

    /* السلم الجانبي (القديم) */
    .step-block { position: relative; padding-right: 60px; margin-bottom: 20px; }
    .step-block::before {
        content: ""; position: absolute; right: 28px; top: 40px; bottom: -40px;
        width: 3px; background-color: #5d5fef; z-index: 1; opacity: 0.3;
    }
    .step-block:last-child::before { display: none; }

    .step-icon {
        position: absolute; right: 8px; top: 0;
        width: 40px; height: 40px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 18px;
    }

    /* بطاقة المحتوى والعناوين */
    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 8px 25px; font-size: 16px; font-weight: bold; }
    .form-body { padding: 15px 25px; }

    /* التايم لاين */
    .timeline-wrapper {
        display: flex; justify-content: space-around; background: white; 
        padding: 20px; border-radius: 15px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .t-step { text-align: center; flex: 1; }
    .t-dot { width: 22px; height: 22px; background: #ddd; border-radius: 50%; margin: 0 auto 8px; }
    .t-step.active .t-dot { background: #5d5fef; box-shadow: 0 0 8px #5d5fef; }
    .t-label { font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 5. الهيدر
st.markdown(f"""
    <div class="company-header">
        <div style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" width="30">
            <div style="margin-right: 15px;">
                <div style="font-weight: bold; font-size: 16px;">مؤسسة المسار المتكامل</div>
                <div style="font-size: 11px; color: #666;">قسم الموارد البشرية - HR</div>
            </div>
        </div>
        <div style="text-align: left; color: #5d5fef; font-size: 13px; font-weight: bold;">{datetime.now().strftime('%Y-%m-%d')}</div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية المنسدلة
with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج (مربعات تعبئة قصيرة العرض) ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        
        # استخدام 3 أعمدة لتقصير عرض المربعات (الحقول في المنتصف واليمين)
        c1, c2, c3 = st.columns([2, 2, 1])
        job_num = c1.text_input("الرقم الوظيفي")
        name = c2.text_input("الاسم الكامل")
        
        c4, c5, c6 = st.columns([2, 2, 1])
        title = c4.text_input("المسمى الوظيفي")
        dept = c5.text_input("الوحدة / القسم")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب والاعتماد</div><div class="form-body">', unsafe_allow_html=True)
        
        c7, c8, c9 = st.columns([2, 2, 1])
        req_type = c7.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        eff_date = c8.date_input("تاريخ السريان (تلقائي)", value=datetime.now(), disabled=True)
        
        c10, c11 = st.columns([4, 1])
        st.markdown("<b>✍️ التوقيع الرقمي (رفع صورة)</b>", unsafe_allow_html=True)
        sig_file = c10.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        c12, c13 = st.columns([4, 1])
        notes = c12.text_input("ملاحظات إضافية (اختياري)")
        
        # زر الإرسال بمقاس محدد
        st.markdown("<br>", unsafe_allow_html=True)
        c_btn, _ = st.columns([1, 4])
        if c_btn.button("إرسال الطلب"):
            if job_num and name and sig_file:
                st.toast("✅ تم إرسال طلبك بنجاح!", icon="🎉")
                time.sleep(1)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى إكمال البيانات ورفع التوقيع")
                
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع (Timeline) ---
elif st.session_state.page == 'tracking':
    st.markdown("<h4>🔍 حالة الطلبات المقدمة</h4>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="timeline-wrapper">
            <div class="t-step active"><div class="t-dot"></div><div class="t-label">تم التقديم</div></div>
            <div class="t-step active"><div class="t-dot"></div><div class="t-label">مراجعة الموارد</div></div>
            <div class="t-step"><div class="t-dot"></div><div class="t-label">اعتماد الإدارة</div></div>
            <div class="t-step"><div class="t-dot"></div><div class="t-label">مكتمل</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("طلبك حالياً في مرحلة التدقيق.")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'form'
        st.rerun()

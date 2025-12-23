import streamlit as st
import sqlite3
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS (الشكل القديم: الدوائر والخط العمودي + العناوين داخل الأشكال)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    
    /* الهيدر الجديد (أيقونة الشركة) */
    .company-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 25px; background: white; border-radius: 15px; margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }

    /* حاوية الخطوة (التصميم القديم) */
    .step-block { position: relative; padding-right: 60px; margin-bottom: 25px; }

    /* الخط العمودي المتصل */
    .step-block::before {
        content: ""; position: absolute; right: 28px; top: 40px; bottom: -40px;
        width: 3px; background-color: #5d5fef; z-index: 1; opacity: 0.3;
    }
    .step-block:last-child::before { display: none; }

    /* الدوائر الرقمية القديمة */
    .step-icon {
        position: absolute; right: 8px; top: 0;
        width: 42px; height: 42px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 20px;
        box-shadow: 0 4px 10px rgba(93,95,239,0.3);
    }

    /* بطاقة المحتوى والعنوان بداخل الشكل */
    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 17px; font-weight: bold; }
    .form-body { padding: 20px 25px; }

    /* تصغير الحقول */
    .stTextInput>div>div>input, .stSelectbox>div>div>div { min-height: 35px !important; }

    /* التايم لاين الجديد */
    .timeline-wrapper {
        display: flex; justify-content: space-around; background: white; 
        padding: 20px; border-radius: 15px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .t-step { text-align: center; flex: 1; }
    .t-dot { width: 25px; height: 25px; background: #ddd; border-radius: 50%; margin: 0 auto 8px; }
    .t-step.active .t-dot { background: #5d5fef; box-shadow: 0 0 8px #5d5fef; }
    .t-label { font-size: 13px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 5. هيدر الشركة
st.markdown(f"""
    <div class="company-header">
        <div style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" width="35">
            <div style="margin-right: 15px;">
                <div style="font-weight: bold; font-size: 18px;">مؤسسة المسار المتكامل</div>
                <div style="font-size: 12px; color: #666;">قسم الموارد البشرية - HR</div>
            </div>
        </div>
        <div style="text-align: left; color: #5d5fef; font-weight: bold;">نموذج طلب إلكتروني</div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية (Drop-down فقط)
with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج (الشكل القديم) ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        job_num = c1.text_input("الرقم الوظيفي")
        name = c2.text_input("الاسم الكامل")
        title = c1.text_input("المسمى الوظيفي")
        dept = c2.text_input("الوحدة / القسم")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب والاعتماد</div><div class="form-body">', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        req_type = c3.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        # 1. تاريخ تلقائي
        eff_date = c4.date_input("تاريخ سريان الطلب (تلقائي)", value=datetime.now(), disabled=True)
        
        st.text_area("ملاحظات إضافية", height=70)
        
        st.markdown("<br><b>✍️ التوقيع الرقمي (رفع صورة التوقيع)</b>", unsafe_allow_html=True)
        # 2. التوقيع كصورة
        sig_file = st.file_uploader("ارفق صورة توقيعك هنا", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if st.button("إرسال الطلب الآن"):
            if job_num and name and sig_file:
                # 3. Pop-up نجاح
                st.toast("✅ تم إرسال طلبك بنجاح!", icon="🎉")
                time.sleep(1)
                # 7. تحويل تلقائي
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى إكمال البيانات ورفع صورة التوقيع")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع (Timeline) ---
elif st.session_state.page == 'tracking':
    st.markdown("<h4>🔍 حالة الطلبات المقدمة</h4>", unsafe_allow_html=True)
    
    # 4. Timeline
    st.markdown(f"""
        <div class="timeline-wrapper">
            <div class="t-step active"><div class="t-dot"></div><div class="t-label">تم التقديم</div></div>
            <div class="t-step active"><div class="t-dot"></div><div class="t-label">مراجعة الموارد</div></div>
            <div class="t-step"><div class="t-dot"></div><div class="t-label">اعتماد الإدارة</div></div>
            <div class="t-step"><div class="t-dot"></div><div class="t-label">مكتمل</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info(f"مرحباً {name if 'name' in locals() else ''}، طلبك حالياً في مرحلة التدقيق من قبل قسم الموارد البشرية.")
    
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'form'
        st.rerun()

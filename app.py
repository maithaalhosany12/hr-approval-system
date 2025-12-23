import streamlit as st
import sqlite3
from datetime import datetime

# إعداد الصفحة لتكون نظيفة وبدون شريط جانبي
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# تنسيق CSS الاحترافي للنموذج والخط المتصل
st.markdown("""
    <style>
    /* إخفاء القائمة الجانبية تماماً */
    [data-testid="stSidebar"] { display: none; }
    
    .main { background-color: #f4f7f9; }
    
    /* حاوية الخطوة */
    .step-block {
        position: relative;
        padding-right: 60px;
        margin-bottom: 30px;
    }

    /* الخط المتصل خلف الدوائر */
    .step-block::before {
        content: "";
        position: absolute;
        right: 28px;
        top: 40px;
        bottom: -40px;
        width: 3px;
        background-color: #5d5fef;
        z-index: 1;
        opacity: 0.3;
    }
    .step-block:last-child::before { display: none; }

    /* الدائرة الرقمية */
    .step-icon {
        position: absolute;
        right: 8px;
        top: 0;
        width: 42px; height: 42px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3;
        font-size: 20px;
        box-shadow: 0 4px 10px rgba(93,95,239,0.3);
    }

    /* بطاقة المحتوى */
    .content-box {
        background-color: white; border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        overflow: hidden;
        border: 1px solid #eef0f2;
    }

    /* شكل عنوان الخطوة */
    .step-header {
        background: linear-gradient(90deg, #5d5fef, #7a7cfc);
        color: white;
        padding: 12px 25px;
        font-size: 18px;
        font-weight: bold;
    }

    .form-body { padding: 25px; }
    
    .stButton>button { 
        background-color: #5d5fef; color: white; width: 100%; 
        border-radius: 10px; font-weight: bold; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, subject_date TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TEXT, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# محتوى الصفحة الرئيسي مباشرة
st.markdown("<h1 style='text-align: center; color: #2d3436;'>📋 نموذج تقديم طلب إداري</h1><br>", unsafe_allow_html=True)

# --- الخطوة الأولى ---
st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('''
        <div class="content-box">
            <div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div>
            <div class="form-body">
    ''', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        job_number = st.text_input("الرقم الوظيفي")
        full_name = st.text_input("الاسم الكامل")
    with c2:
        job_title = st.text_input("المسمى الوظيفي")
        unit = st.text_input("الوحدة / القسم")
    st.date_input("تاريخ التعيين", key="d1")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- الخطوة الثانية ---
st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('''
        <div class="content-box">
            <div class="step-header">📝 الخطوة الثانية: تفاصيل موضوع الطلب والاعتماد</div>
            <div class="form-body">
    ''', unsafe_allow_html=True)
    
    c3, c4 = st.columns(2)
    with c3:
        subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
    with c4:
        subject_date = st.date_input("تاريخ سريان الطلب", key="d2")
    
    st.text_area("ملاحظات إضافية")
    st.markdown("<hr style='opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown("<b>✍️ التوقيع الرقمي:</b>", unsafe_allow_html=True)
    signature = st.text_input("اكتب الاسم الثلاثي للإقرار بصحة البيانات")
    
    if st.button("إرسال الطلب الآن"):
        if job_number and full_name and signature:
            # هنا يمكنك إضافة كود الحفظ في قاعدة البيانات
            st.success("✅ تم إرسال الطلب بنجاح!")
            st.balloons()
        else:
            st.error("⚠️ يرجى التأكد من تعبئة البيانات الأساسية")
            
    st.markdown('</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

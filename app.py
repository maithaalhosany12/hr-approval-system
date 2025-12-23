import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide")

# تنسيق CSS لربط الخط وجعله متصلاً تماماً
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* الحاوية الكبرى التي تجمع السلالم والمحتوى */
    .stepper-wrapper {
        display: flex;
        position: relative;
        gap: 30px;
        padding-right: 50px;
    }

    /* عمود السلم الجانبي */
    .stepper-column {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }

    /* الدائرة */
    .step-circle {
        width: 40px; height: 40px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 18px;
        z-index: 2;
        margin-top: 10px;
        box-shadow: 0 4px 10px rgba(93, 95, 239, 0.3);
    }

    /* الخط المتصل - تم تعديل وضعه ليكون خلف الدوائر تماماً ومستمراً */
    .step-line-vertical {
        position: absolute;
        top: 30px; /* يبدأ من منتصف الدائرة الأولى */
        bottom: 50px; /* ينتهي عند منتصف الدائرة الأخيرة */
        width: 3px;
        background-color: #5d5fef;
        z-index: 1;
    }

    /* حاوية المحتوى */
    .content-wrapper {
        flex-grow: 1;
    }

    /* بطاقة المحتوى */
    .content-card {
        background-color: white; padding: 30px; border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-right: 6px solid #5d5fef;
        margin-bottom: 50px; /* مسافة بين الخطوة 1 و 2 */
    }
    
    h2 { color: #2d3436; font-size: 20px; margin-top: 0; }
    </style>
    """, unsafe_allow_html=True)

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    try:
        c.execute("SELECT subject_date FROM requests LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS requests")
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, subject_date TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TEXT, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

choice = st.sidebar.radio("التنقل في النظام", ["تقديم طلب جديد", "متابعة الطلبات"])

if choice == "تقديم طلب جديد":
    st.markdown("<h1 style='text-align: center;'>📝 نموذج تقديم طلب جديد</h1><br>", unsafe_allow_html=True)

    # بداية هيكل السلم المتصل
    st.markdown('<div class="stepper-wrapper">', unsafe_allow_html=True)
    
    # العمود الجانبي (الدوائر والخط)
    # ملاحظة: المسافة بين الدوائر ستتعدل تلقائياً حسب طول البطاقات
    st.markdown('''
        <div class="stepper-column">
            <div class="step-line-vertical"></div>
            <div class="step-circle" style="margin-bottom: 460px;">1</div>
            <div class="step-circle">2</div>
        </div>
    ''', unsafe_allow_html=True)

    # عمود المحتوى
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    # --- الخطوة الأولى ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h2>👤 الخطوة الأولى: بيانات مقدم الطلب</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        job_number = st.text_input("الرقم الوظيفي")
        full_name = st.text_input("الاسم الكامل")
    with c2:
        job_title = st.text_input("المسمى الوظيفي")
        unit = st.text_input("الوحدة / القسم")
    appt_date = st.date_input("تاريخ التعيين")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- الخطوة الثانية ---
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h2>📝 الخطوة الثانية: تفاصيل الطلب والاعتماد</h2>", unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
    with cs2:
        subject_date = st.date_input("تاريخ سريان الطلب")
    
    if subject_type == "نقل":
        target_entity = st.text_input("الجهة المطلوب النقل إليها")
    else:
        target_entity = ""
        
    notes = st.text_area("ملاحظات إضافية")
    st.markdown("<hr style='border: 0.2px solid #eee;'>", unsafe_allow_html=True)
    signature = st.text_input("التوقيع الرقمي (اكتب اسمك الثلاثي)")
    
    if st.button("إرسال الطلب للاعتماد"):
        if job_number and full_name and signature:
            st.success("✅ تم الإرسال بنجاح!")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # إغلاق الحاويات
    st.markdown('</div></div>', unsafe_allow_html=True)

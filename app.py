import streamlit as st
import sqlite3
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide")

# تنسيق CSS لجعل الرقم بجانب العنوان مباشرة والخط متصل خلفه
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* حاوية الخطوة */
    .step-block {
        position: relative;
        padding-right: 60px; /* مساحة للخط والدائرة */
        margin-bottom: 20px;
    }

    /* الخط العمودي المتصل خلف الدوائر */
    .step-block::before {
        content: "";
        position: absolute;
        right: 28px; /* وضع الخط في منتصف الدائرة */
        top: 10px;
        bottom: -30px; /* يمتد للخطوة التالية */
        width: 2px;
        background-color: #5d5fef;
        z-index: 1;
    }

    /* إخفاء الخط في آخر خطوة */
    .step-block:last-child::before {
        display: none;
    }

    /* الدائرة الرقمية */
    .step-icon {
        position: absolute;
        right: 8px;
        top: 0;
        width: 40px; height: 40px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 2;
        box-shadow: 0 4px 8px rgba(93,95,239,0.2);
    }

    /* بطاقة المحتوى */
    .content-box {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-right: 4px solid #5d5fef;
    }

    .step-title {
        font-size: 20px; font-weight: bold; color: #2d3436;
        margin-bottom: 20px; display: flex; align-items: center;
    }
    
    .stButton>button { 
        background-color: #5d5fef; color: white; width: 100%; 
        border-radius: 10px; font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

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

choice = st.sidebar.radio("القائمة", ["تقديم طلب جديد", "متابعة الطلبات"])

if choice == "تقديم طلب جديد":
    st.markdown("<h1 style='text-align: center;'>📝 نموذج تقديم طلب جديد</h1><br>", unsafe_allow_html=True)

    # --- الخطوة الأولى ---
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("<div class='step-title'>الخطوة الأولى: بيانات مقدم الطلب</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            job_number = st.text_input("الرقم الوظيفي")
            full_name = st.text_input("الاسم الكامل")
        with c2:
            job_title = st.text_input("المسمى الوظيفي")
            unit = st.text_input("الوحدة / القسم")
        st.date_input("تاريخ التعيين", key="d1")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- الخطوة الثانية ---
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("<div class='step-title'>الخطوة الثانية: تفاصيل الطلب والاعتماد</div>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        with c4:
            subject_date = st.date_input("تاريخ سريان الطلب", key="d2")
        
        st.text_area("ملاحظات إضافية")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.text_input("التوقيع الرقمي (الاسم الثلاثي)")
        
        if st.button("إرسال الطلب للاعتماد"):
            st.success("✅ تم الإرسال بنجاح!")
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == "متابعة الطلبات":
    st.info("صفحة متابعة الطلبات قيد التطوير")

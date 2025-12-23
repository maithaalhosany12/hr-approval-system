import streamlit as st
import sqlite3
from datetime import datetime

# إعداد الصفحة وتنسيق CSS مخصص للخطوات الجانبية
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide")

st.markdown("""
    <style>
    /* تنسيق الخطوات الجانبية (The Stepper) */
    .step-circle {
        width: 40px; height: 40px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 0 auto 10px auto;
        box-shadow: 0 4px 8px rgba(93, 95, 239, 0.3);
    }
    .step-line {
        width: 2px; height: 150px; background-color: #e0e0e0;
        margin: 0 auto 10px auto;
    }
    .step-label { text-align: center; font-size: 14px; color: #666; font-weight: bold; }
    
    /* تنسيق الحاويات */
    .main-card {
        background-color: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    h2 { color: #2d3436; font-size: 22px; margin-bottom: 20px; border-right: 5px solid #5d5fef; padding-right: 15px; }
    </style>
    """, unsafe_allow_html=True)

# دالة إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    try:
        c.execute("SELECT job_title FROM requests LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS requests")
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TEXT, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# القائمة الجانبية للتنقل الأساسي
menu = ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات الإدارية"]
choice = st.sidebar.radio("التنقل في النظام", menu)

if choice == "تقديم طلب جديد":
    # إنشاء تقسيم للصفحة: يمين للخطوات، ويسار للنموذج
    col_stepper, col_form = st.columns([1, 5])

    # --- الجزء الأيمن: الخطوات (كما في الصورة) ---
    with col_stepper:
        st.markdown('<div class="step-circle">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-label">بيانات الموظف</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-line"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="step-circle">2</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-label">تفاصيل الطلب</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-line"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="step-circle">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-label">الإقرار والتوقيع</div>', unsafe_allow_html=True)

    # --- الجزء الأيسر: النموذج الفعلي (أسلوب التمرير) ---
    with col_form:
        # القسم 1
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
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

        # القسم 2
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h2>📝 الخطوة الثانية: موضوع وتفاصيل الطلب</h2>", unsafe_allow_html=True)
        subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        
        if subject_type == "نقل":
            target_entity = st.text_input("الجهة المطلوب النقل إليها")
        else:
            target_entity = ""
            
        if subject_type in ["تغيير مهنة", "إنهاء خدمة"]:
            st.warning(f"مطلوب إرفاق مستندات لحالة: {subject_type}")
            st.file_uploader("رفع المرفق")
            
        notes = st.text_area("ملاحظات إضافية")
        st.markdown('</div>', unsafe_allow_html=True)

        # القسم 3
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h2>✍️ الخطوة الثالثة: التوقيع والإرسال</h2>", unsafe_allow_html=True)
        signature = st.text_input("التوقيع الرقمي (اكتب اسمك الثلاثي كإقرار)")
        
        if st.button("إرسال الطلب نهائياً"):
            if job_number and full_name and signature:
                conn = sqlite3.connect('requests.db')
                c = conn.cursor()
                c.execute("""INSERT INTO requests 
                          (job_number, name, job_title, unit, appt_date, subject_type, 
                           target_entity, notes, submit_date, signature, status, stage) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                          (job_number, full_name, job_title, unit, str(appt_date), subject_type,
                           target_entity, notes, datetime.now().strftime("%Y-%m-%d"), signature, "بانتظار موافقة المسؤول", 1))
                conn.commit()
                st.success("✅ تم الإرسال بنجاح!")
                st.balloons()
            else:
                st.error("الرجاء استكمال البيانات والتوقيع")
        st.markdown('</div>', unsafe_allow_html=True)

elif choice == "متابعة الطلبات":
    st.header("🔍 متابعة حالة الطلب")
    # ... كود المتابعة السابق ...

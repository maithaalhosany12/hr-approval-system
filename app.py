import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF

# --- 1. إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('hr_system_v2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests 
                 (id TEXT PRIMARY KEY, emp_name TEXT, emp_id TEXT, 
                  req_type TEXT, status TEXT, date_created TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- 2. وظيفة إنشاء ملف PDF ---
def create_pdf(req_data):
    pdf = FPDF()
    pdf.add_page()
    # إعداد الخط (ملاحظة: للغة العربية يفضل إضافة خط يدعم Unicode)
    pdf.set_font("Arial", 'B', 16)
    
    # رأس الصفحة
    pdf.cell(200, 10, txt="HR Request Document", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {req_data['date_created']}", ln=True)
    pdf.cell(200, 10, txt=f"Request ID: {req_data['id']}", ln=True)
    pdf.cell(200, 10, txt=f"Employee Name: {req_data['emp_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Employee ID: {req_data['emp_id']}", ln=True)
    pdf.cell(200, 10, txt=f"Request Type: {req_data['req_type']}", ln=True)
    pdf.cell(200, 10, txt=f"Status: {req_data['status']}", ln=True)
    
    pdf.ln(20)
    pdf.cell(200, 10, txt="Signature: __________________", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. واجهة المستخدم ---
st.set_page_config(page_title="نظام HR المطور", layout="wide")

with st.sidebar:
    st.title("👤 بوابة الوصول")
    role = st.radio("اختر الدور:", ["موظف", "مدير (رمز سري)"])

if role == "موظف":
    st.header("📝 تقديم طلب جديد")
    with st.form("request_form"):
        name = st.text_input("اسم الموظف")
        emp_id = st.text_input("الرقم الوظيفي")
        r_type = st.selectbox("نوع الطلب", ["إجازة سنوية", "شهادة راتب", "مباشرة عمل"])
        submit = st.form_submit_button("إرسال الطلب")
        
        if submit and name and emp_id:
            req_id = f"REQ-{datetime.now().strftime('%f')}"
            date_now = datetime.now().strftime("%Y-%m-%d")
            
            # حفظ في قاعدة البيانات
            conn = sqlite3.connect('hr_system_v2.db')
            c = conn.cursor()
            c.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?)",
                      (req_id, name, emp_id, r_type, "قيد الانتظار", date_now))
            conn.commit()
            conn.close()
            st.success(f"تم حفظ الطلب بنجاح! رقم الطلب: {req_id}")

elif role == "مدير (رمز سري)":
    pwd = st.sidebar.text_input("أدخل الرمز السري", type="password")
    if pwd == "1234":
        st.header("📊 لوحة تحكم الإدارة")
        
        conn = sqlite3.connect('hr_system_v2.db')
        df = pd.read_sql_query("SELECT * FROM requests", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            st.subheader("🖨️ استخراج مستندات PDF")
            selected_id = st.selectbox("اختر رقم الطلب لتحميله بصيغة PDF", df['id'])
            
            if st.button("تجهيز ملف PDF"):
                req_info = df[df['id'] == selected_id].iloc[0]
                pdf_bytes = create_pdf(req_info)
                
                st.download_button(
                    label="⬇️ تحميل ملف PDF للطلب",
                    data=pdf_bytes,
                    file_name=f"request_{selected_id}.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("لا توجد طلبات في قاعدة البيانات حالياً.")
    else:
        st.warning("يرجى إدخال الرمز السري الصحيح للوصول إلى بيانات الإدارة.")

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

# --- 1. إعداد قاعدة البيانات والوظائف الخلفية ---
def init_db():
    conn = sqlite3.connect('path_to_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hr_requests 
                 (id TEXT PRIMARY KEY, emp_id TEXT, name TEXT, title TEXT, dept TEXT, 
                  hire_date TEXT, req_type TEXT, status TEXT, stage INT, 
                  created_at TIMESTAMP, last_action TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()

# --- 2. التحقق من القيود (3 طلبات / 30 يوم) ---
def check_constraints(emp_id):
    c = conn.cursor()
    # التحقق من عدد الطلبات
    c.execute("SELECT COUNT(*) FROM hr_requests WHERE emp_id = ?", (emp_id,))
    count = c.fetchone()[0]
    # التحقق من تاريخ آخر طلب
    c.execute("SELECT MAX(created_at) FROM hr_requests WHERE emp_id = ?", (emp_id,))
    last_date = c.fetchone()[0]
    
    if count >= 3: return False, "لقد استنفدت الحد الأقصى (3 طلبات)."
    if last_date:
        last_dt = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S.%f')
        if datetime.now() - last_dt < timedelta(days=30):
            return False, f"يجب الانتظار {(timedelta(days=30) - (datetime.now() - last_dt)).days} يوم إضافي."
    return True, ""

# --- 3. الواجهة والتنسيق CSS ---
st.set_page_config(page_title="نظام المسار المتكامل", layout="wide")
st.markdown("""
    <style>
    .main { direction: rtl !important; text-align: right !important; background-color: #f8f9fa; }
    .stTextInput>div>div>input { height: 35px !important; text-align: right !important; }
    .approval-card { border-right: 5px solid #5d5fef; background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية ونظام الصلاحيات ---
with st.sidebar:
    st.header("🔐 الدخول للنظام")
    user_role = st.radio("الدخول بصفة:", ["موظف", "مدير / HR"])
    is_admin = False
    if user_role == "مدير / HR":
        pin = st.text_input("الرمز السري", type="password")
        if pin == "1234": is_admin = True
    
    st.divider()
    menu = ["تقديم طلب جديد", "متابعة الطلبات"]
    if is_admin: menu.append("لوحة الاعتمادات")
    choice = st.selectbox("القائمة:", menu)

# --- 5. منطق الصفحات ---

# أ- صفحة التقديم (5 حقول متجاورة + قيود)
if choice == "تقديم طلب جديد":
    st.subheader("👤 بيانات مقدم الطلب")
    order_id = f"REQ-{random.randint(1000, 9999)}"
    
    # الـ 5 حقول المتجاورة تماماً كما طلبت
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: emp_id = st.text_input("الرقم الوظيفي")
    with c2: name = st.text_input("الاسم الكامل")
    with c3: title = st.text_input("المسمى")
    with c4: dept = st.text_input("القسم")
    with c5: hire_date = st.date_input("تاريخ التعيين")

    st.divider()
    st.subheader("📝 تفاصيل الطلب والمرفقات")
    col_a, col_b = st.columns(2)
    with col_a: req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
    with col_b: st.file_uploader("تحميل المرفق الرسمي")
    
    st.text_area("ملاحظات إضافية")
    st.file_uploader("توقيع الموظف (صورة)")

    if st.button("إرسال الطلب الآن"):
        allowed, msg = check_constraints(emp_id)
        if not allowed:
            st.error(msg)
        elif emp_id and name:
            c = conn.cursor()
            c.execute("INSERT INTO hr_requests VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (order_id, emp_id, name, title, dept, str(hire_date), req_type, "بانتظار الاعتماد", 1, datetime.now(), datetime.now()))
            conn.commit()
            st.success(f"تم الإرسال! رقم طلبك هو: {order_id}")
        else:
            st.warning("يرجى إكمال البيانات الأساسية")

# ب- صفحة المتابعة والطباعة
elif choice == "متابعة الطلبات":
    st.subheader("🔍 سجل الطلبات")
    df = pd.read_sql_query("SELECT id, req_type, created_at, status FROM hr_requests", conn)
    st.dataframe(df, use_container_width=True)
    
    if not df.empty:
        if st.button("📄 تصدير سجل الطلبات إلى Excel"):
            df.to_csv("requests_report.csv", index=False)
            st.success("تم التصدير بنجاح!")

# ج- لوحة الاعتمادات (نظام الـ 45 يوم)
elif choice == "لوحة الاعتمادات":
    st.subheader("⚖️ نظام الاعتمادات الإدارية")
    pending_df = pd.read_sql_query("SELECT * FROM hr_requests WHERE status != 'مكتمل'", conn)
    
    if pending_df.empty:
        st.info("لا توجد طلبات بانتظار الاعتماد")
    else:
        sel_id = st.selectbox("اختر الطلب للمراجعة", pending_df['id'])
        req = pending_df[pending_df['id'] == sel_id].iloc[0]
        
        # حساب مدة الطلب (تنبيه الـ 45 يوم)
        days_passed = (datetime.now() - datetime.strptime(req['created_at'], '%Y-%m-%d %H:%M:%S.%f')).days
        if days_passed > 45:
            st.markdown(f'<div style="color:red; font-weight:bold;">⚠️ تنبيه: هذا الطلب تجاوز المهلة النظامية ({days_passed} يوم)</div>', unsafe_allow_html=True)
        
        # توزيع خانات الاعتماد الـ 3
        st.write(f"المرحلة الحالية: {req['stage']}")
        col_m1, col_m2, col_m3 = st.columns(3)
        stages_names = ["المدير المباشر", "HR", "المدير العام"]
        
        for i, stage_name in enumerate(stages_names, 1):
            with [col_m1, col_m2, col_m3][i-1]:
                is_active = (req['stage'] == i)
                st.markdown(f'<div class="approval-card"><b>{stage_name}</b></div>', unsafe_allow_html=True)
                st.text_input("الاسم", key=f"n{i}", disabled=not is_active)
                res = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key=f"r{i}", disabled=not is_active)
                reason = st.text_area("المبررات", key=f"rs{i}", disabled=not is_active)
                
                if is_active and st.button(f"حفظ قرار {stage_name}"):
                    if reason:
                        new_stage = i + 1 if res == "موافق" and i < 3 else i
                        new_status = "مكتمل" if res == "موافق" and i == 3 else "مرفوض" if res == "مرفوض" else "بانتظار المرحلة التالية"
                        c = conn.cursor()
                        c.execute("UPDATE hr_requests SET stage=?, status=?, last_action=? WHERE id=?", 
                                  (new_stage, new_status, datetime.now(), sel_id))
                        conn.commit()
                        st.rerun()
                    else: st.error("المبررات إلزامية!")

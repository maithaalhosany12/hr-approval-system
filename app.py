import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random
import time

# --- 1. هندسة الواجهة والتصميم البصري الفاخر ---
st.set_page_config(page_title="نظام المسار الذكي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الأساسيات */
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; }
    .main { background-color: #f0f2f5; }
    
    /* القائمة الجانبية: تباين عالٍ ونصوص واضحة جداً */
    [data-testid="stSidebar"] {
        background-color: #0d1b2a !important;
        border-left: 1px solid #1a237e;
    }
    .stButton>button {
        background-color: #ffffff !important; 
        color: #0d1b2a !important; /* نص أسود كحلي عميق */
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 55px;
        font-size: 17px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e0e6ed !important;
        transform: translateY(-2px);
    }

    /* تصميم الكروت الرئيسية المطور */
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        padding: 20px 0;
    }
    
    .modern-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 40px 25px;
        text-align: center;
        border: 1px solid #e0e6ed;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
    }
    
    .modern-card:hover {
        transform: translateY(-15px);
        box-shadow: 0 20px 40px rgba(13, 27, 42, 0.15);
        border-bottom: 6px solid #1a237e;
    }

    .card-icon {
        font-size: 50px;
        background: #f8f9fa;
        width: 90px;
        height: 90px;
        line-height: 90px;
        border-radius: 50%;
        margin: 0 auto 20px;
        transition: 0.5s;
    }
    .modern-card:hover .card-icon {
        background: #1a237e;
        color: white;
        transform: rotateY(360deg);
    }

    .card-title { color: #0d1b2a; font-size: 20px; font-weight: 700; margin-bottom: 10px; }
    .card-desc { color: #607d8b; font-size: 14px; line-height: 1.6; }

    /* تحسين شكل التتبع (Timeline) */
    .timeline-box {
        background: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin-top: 20px;
    }
    .step-label { font-weight: 700; color: #1a237e; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات ---
def init_db():
    conn = sqlite3.connect('hr_luxury_v1.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests 
                 (id TEXT PRIMARY KEY, emp_id TEXT, name TEXT, type TEXT, status TEXT, date TEXT, notes TEXT)''')
    conn.commit()
    return conn

# إدارة الحالة والتنقل
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"
if 'current_type' not in st.session_state: st.session_state.current_type = ""

# --- 3. القائمة الجانبية المرتبة ---
with st.sidebar:
    st.markdown("<div style='text-align:center; padding:20px;'><h2 style='color:white;'>نظام المسار</h2></div>", unsafe_allow_html=True)
    if st.button("🏠 الصفحة الرئيسية", use_container_width=True): st.session_state.page = "الرئيسية"
    if st.button("📑 تتبع طلباتي", use_container_width=True): st.session_state.page = "تتبع"
    if st.button("🔔 مركز الاعتمادات", use_container_width=True): st.session_state.page = "اعتماد"

# --- 4. المحتوى المنظم ---

def home_page():
    st.markdown("<h1 style='color:#0d1b2a; text-align:right;'>بوابة الخدمات الإلكترونية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#546e7a; font-size:18px;'>يرجى اختيار القسم الموجه له الطلب لبدء الإجراء:</p>", unsafe_allow_html=True)
    
    # شبكة الكروت (الخمس خانات المطلوبة)
    cols = st.columns(5)
    card_data = [
        {"t": "طلب خطي للمدير", "i": "💼", "d": "مراسلات الإدارة العليا"},
        {"t": "طلب خطي للإدارة", "i": "🏛️", "d": "تنسيق الخدمات الإدارية"},
        {"t": "طلب خطي للموظفين", "i": "👥", "d": "شؤون الكادر الوظيفي"},
        {"t": "طلب خطي للعاملين", "i": "⚙️", "d": "الدعم والخدمات اللوجستية"},
        {"t": "طلب خطي للبوابة", "i": "🛂", "d": "تصاريح الأمن والدخول"}
    ]
    
    for i, data in enumerate(card_data):
        with cols[i]:
            # الكرت كمظهر جمالي
            st.markdown(f"""
                <div class="modern-card">
                    <div class="card-icon">{data['i']}</div>
                    <div class="card-title">{data['t']}</div>
                    <div class="card-desc">{data['d']}</div>
                </div>
            """, unsafe_allow_html=True)
            # الزر كأداة ضغط (مخفي خلف التصميم أو تحته مباشرة للتنقل)
            if st.button(f"اختيار {data['t']}", key=f"sel_{i}", use_container_width=True):
                st.session_state.current_type = data['t']
                st.session_state.page = "تقديم"
                st.rerun()

def request_form():
    st.markdown(f"<h2 style='color:#1a237e;'>📝 تقديم: {st.session_state.current_type}</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div style='background:white; padding:40px; border-radius:25px; box-shadow:0 10px 30px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        with st.form("luxury_form"):
            c1, c2 = st.columns(2)
            u_id = c1.text_input("الرقم الوظيفي")
            u_name = c2.text_input("الاسم الكامل للطلبات الرسمية")
            u_notes = st.text_area("نص الطلب الخطي الموجه")
            
            submit = st.form_submit_button("إرسال الطلب بشكل رسمي 🚀")
            if submit:
                if u_id and u_name:
                    order_id = f"REF-{random.randint(10000,99999)}"
                    conn = init_db()
                    conn.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?)", 
                                 (order_id, u_id, u_name, st.session_state.current_type, "قيد المراجعة", 
                                  datetime.now().strftime('%Y-%m-%d %H:%M'), u_notes))
                    conn.commit()
                    st.session_state.last_id = order_id
                    st.session_state.page = "تتبع"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def tracking_page():
    st.markdown("<h2 style='color:#0d1b2a;'>📑 مسار اعتماد الطلب</h2>", unsafe_allow_html=True)
    if 'last_id' not in st.session_state:
        st.info("لا توجد طلبات نشطة لعرضها حالياً.") ; return
    
    st.markdown("""
        <div class="timeline-box">
            <div style="display: flex; justify-content: space-between; position: relative;">
                <div style="position: absolute; top: 25px; left: 5%; right: 5%; height: 3px; background: #e0e6ed; z-index: 1;"></div>
                <div style="z-index: 2; text-align: center;"><div style="width:50px; height:50px; background:#2e7d32; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; font-weight:700;">✓</div><div class="step-label">تم الإرسال</div></div>
                <div style="z-index: 2; text-align: center;"><div style="width:50px; height:50px; background:#1a237e; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; font-weight:700;">1</div><div class="step-label">مراجعة الإدارة</div></div>
                <div style="z-index: 2; text-align: center;"><div style="width:50px; height:50px; background:#e0e6ed; color:#9e9e9e; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; font-weight:700;">2</div><div class="step-label">الاعتماد النهائي</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. منطق التشغيل ---
if st.session_state.page == "الرئيسية": home_page()
elif st.session_state.page == "تقديم": request_form()
elif st.session_state.page == "تتبع": tracking_page()

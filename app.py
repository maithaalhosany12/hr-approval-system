import streamlit as st
from datetime import datetime, timedelta
import time
import random

# 1. إعداد الصفحة والتنسيق (الأصيل والكامل)
st.set_page_config(page_title="نظام شؤون الموظفين - مؤسسة المسار", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f9; }
    .company-header {
        display: flex; align-items: center; justify-content: flex-start;
        padding: 15px 25px; background: white; border-radius: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }
    .header-logo img { width: 45px; margin-left: 15px; }
    .header-text h1 { margin: 0; font-size: 19px; color: #2d3436; font-weight: bold; }
    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 20px 25px; }
    .stat-card { background: white; padding: 15px; border-radius: 10px; border-top: 4px solid #5d5fef; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }
    .stat-val { font-size: 22px; font-weight: bold; color: #5d5fef; }
    .notification-timer { background-color: #fff4f4; border: 1px solid #ffcdd2; color: #c62828; padding: 12px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; text-align: center; border-right: 5px solid #c62828; }
    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    .reason-box { background-color: #f0f7ff; padding: 10px; border-radius: 8px; margin-top: 10px; border: 1px solid #bcd9ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة والأمان
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_role' not in st.session_state: st.session_state.user_role = "موظف"
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"
if 'request_count' not in st.session_state: st.session_state.request_count = 0
if 'last_request_date' not in st.session_state: st.session_state.last_request_date = None
if 'stage_start_date' not in st.session_state: st.session_state.stage_start_date = datetime.now()

# 3. الهيدر الرسمي
st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>نظام الصلاحيات والطلبات الذكي</p></div></div>', unsafe_allow_html=True)

# 4. القائمة الجانبية مع نظام الدخول
with st.sidebar:
    st.title("👤 بوابة الوصول")
    role = st.radio("نوع الدخول:", ["موظف", "إدارة (مدراء)"])
    
    if role == "إدارة (مدراء)":
        password = st.text_input("أدخل الرمز السري للمدراء:", type="password")
        if password == "1234": # يمكنك تغيير الرمز السري هنا
            st.session_state.authenticated = True
            st.session_state.user_role = "مدير"
            st.success("تم الدخول بصلاحية مدير")
        else:
            st.session_state.authenticated = False
            if password: st.error("الرمز السري خاطئ")
    else:
        st.session_state.authenticated = False
        st.session_state.user_role = "موظف"

    st.divider()
    
    # تحديد الخيارات المتاحة بناءً على الصلاحية
    options = ["تقديم طلب جديد", "متابعة الطلبات"]
    if st.session_state.authenticated:
        options.append("لوحة الاعتمادات (إدارة)")
    
    choice = st.selectbox("انتقل إلى:", options)
    st.session_state.page = 'form' if choice == "تقديم طلب جديد" else 'tracking' if choice == "متابعة الطلبات" else 'approvals'

# --- الصفحة 1: تقديم الطلب (للموظف) ---
if st.session_state.page == 'form':
    if st.session_state.request_count >= 3:
        st.error("⚠️ عذراً، لقد استنفدت الحد الأقصى للطلبات (3 طلبات فقط).")
    elif st.session_state.last_request_date and (datetime.now() - st.session_state.last_request_date).days < 30:
        days_left = 30 - (datetime.now() - st.session_state.last_request_date).days
        st.warning(f"⚠️ نظام الجودة: يجب الانتظار {days_left} يوم إضافي.")
    else:
        # (نموذج الطلب الأصلي - الخطوة 1 والخطوة 2 كما هي تماماً)
        with st.container():
            st.markdown('<div class="content-box"><div class="step-header">👤 بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
            r_col, _ = st.columns([1, 4])
            with r_col: st.text_input("رقم الطلب", value=st.session_state.order_id, disabled=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: st.text_input("الرقم الوظيفي")
            with c2: st.text_input("الاسم الكامل")
            with c3: st.text_input("المسمى")
            with c4: st.text_input("القسم")
            with c5: st.date_input("تاريخ التعيين")
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            st.markdown('<div class="content-box"><div class="step-header">📝 تفاصيل الطلب والمرفقات</div><div class="form-body">', unsafe_allow_html=True)
            req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
            if req_type in ["تعديل مهنة", "إنهاء خدمة"]:
                st.markdown(f'<div style="background:#fff9e6; padding:10px; border-radius:5px; border-right:5px solid #ffd43b;">📎 مرفق مطلوب لـ {req_type}</div>', unsafe_allow_html=True)
                st.file_uploader("تحميل المرفق", key="f_up")
            st.text_area("ملاحظات إضافية تفصيلية", height=100)
            c_sig, c_btn = st.columns([3, 1])
            with c_sig: st.file_uploader("توقيع الموظف", key="sig_m")
            with c_btn: 
                if st.button("إرسال الطلب", use_container_width=True):
                    st.session_state.request_count += 1
                    st.session_state.last_request_date = datetime.now()
                    st.session_state.stage_start_date = datetime.now()
                    st.success("تم الإرسال!"); time.sleep(1); st.session_state.page = 'tracking'; st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

# --- الصفحة 2: متابعة الطلبات ---
elif st.session_state.page == 'tracking':
    st.markdown("### 🔍 سجل المتابعة")
    st.info(f"الطلب النشط حالياً: {st.session_state.order_id}")
    if st.button("📄 طباعة ملخص الطلب"): st.write("جاري التحميل...")

# --- الصفحة 3: الاعتمادات (للمدراء فقط بالرمز السري) ---
elif st.session_state.page == 'approvals':
    if not st.session_state.authenticated:
        st.warning("🔒 هذه الصفحة مخصصة للمدراء فقط. يرجى إدخال الرمز السري من القائمة الجانبية.")
    else:
        # Dashboard
        d1, d2, d3 = st.columns(3)
        with d1: st.markdown('<div class="stat-card"><div class="stat-val">1</div><div class="stat-label">طلبات بانتظارك</div></div>', unsafe_allow_html=True)
        with d2: st.markdown('<div class="stat-card"><div class="stat-val" style="color:red;">0</div><div class="stat-label">تجاوزت المهلة</div></div>', unsafe_allow_html=True)
        with d3: st.markdown('<div class="stat-card"><div class="stat-val" style="color:green;">12</div><div class="stat-label">طلبات منجزة</div></div>', unsafe_allow_html=True)
        
        st.divider()
        order_select = st.selectbox("اختر الطلب للمراجعة:", ["--- اختر طلباً ---", f"{st.session_state.order_id}"])
        
        if order_select != "--- اختر طلباً ---":
            remaining = 45 - (datetime.now() - st.session_state.stage_start_date).days
            st.markdown(f'<div class="notification-timer">⏳ متبقي للمسؤول الحالي {remaining} يوم لاتخاذ القرار</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            stages = ["المدير المباشر", "الموارد البشرية", "المدير العام"]
            for i, name in enumerate(stages, 1):
                with [col1, col2, col3][i-1]:
                    active = st.session_state.stage == i
                    st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>{i}️⃣ {name}</b></div>', unsafe_allow_html=True)
                    st.text_input("الاسم الكامل", key=f"nn{i}", disabled=not active)
                    st.text_input("المنصب", key=f"pp{i}", disabled=not active)
                    st.text_input("الوظيفة", key=f"jj{i}", disabled=not active)
                    res = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key=f"rr{i}", disabled=not active)
                    
                    if active and res in ["موافق", "مرفوض"]:
                        st.text_area(f"مبررات القرار (إلزامي لـ {res})", key=f"rsn{i}")
                        if st.button(f"حفظ قرار {name}"):
                            if st.session_state[f"rsn{i}"]:
                                if res == "موافق":
                                    st.session_state.stage += 1
                                    st.session_state.stage_start_date = datetime.now()
                                    st.rerun()
                                else: st.error("تم الرفض")
                            else: st.warning("اكتب السبب أولاً")

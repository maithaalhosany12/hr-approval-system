import streamlit as st
from datetime import datetime, timedelta
import time
import random

# 1. إعداد الصفحة والتنسيق (النسخة الأصلية الثابتة)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f9; }
    .block-container { max-width: 1100px !important; padding-top: 1.5rem; }
    .company-header {
        display: flex; align-items: center; justify-content: flex-start;
        padding: 15px 25px; background: white; border-radius: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }
    .header-logo img { width: 45px; margin-left: 15px; }
    .header-text h1 { margin: 0; font-size: 19px; color: #2d3436; font-weight: bold; }
    
    /* تنسيق الخطوات الأصلي */
    .step-block { position: relative; padding-right: 60px; margin-bottom: 30px; }
    .step-icon {
        position: absolute; right: 8px; top: 0;
        width: 42px; height: 42px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 18px;
    }
    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 20px 25px; }

    /* الحقول المتجاورة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    
    /* التنبيهات والبطاقات */
    .stat-card { background: white; padding: 15px; border-radius: 10px; border-top: 4px solid #5d5fef; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }
    .notification-timer { background-color: #fff4f4; border: 1px solid #ffcdd2; color: #c62828; padding: 12px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; text-align: center; border-right: 5px solid #c62828; }
    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    .styled-table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
    .styled-table th, .styled-table td { padding: 12px 15px; border-bottom: 1px solid #eee; text-align: right; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة والأمان (دون تغيير المنطق السابق)
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"
if 'request_count' not in st.session_state: st.session_state.request_count = 0
if 'last_request_date' not in st.session_state: st.session_state.last_request_date = None
if 'stage_start_date' not in st.session_state: st.session_state.stage_start_date = datetime.now()

# 3. الهيدر الرسمي
st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>نظام شؤون الموظفين المطور</p></div></div>', unsafe_allow_html=True)

# 4. القائمة الجانبية (نظام الصلاحيات المضاف)
with st.sidebar:
    st.title("🔐 تسجيل الدخول")
    user_type = st.radio("الدخول بصفتك:", ["موظف", "مدير / HR"])
    
    is_admin = False
    if user_type == "مدير / HR":
        pin = st.text_input("أدخل الرمز السري:", type="password")
        if pin == "1234":
            is_admin = True
            st.success("تم تفعيل صلاحيات الإدارة")
        elif pin:
            st.error("الرمز خاطئ")

    st.divider()
    menu = ["تقديم طلب جديد", "متابعة الطلبات"]
    if is_admin:
        menu.append("لوحة الاعتمادات")
    
    choice = st.selectbox("القائمة الرئيسية:", menu)
    st.session_state.page = 'form' if choice == "تقديم طلب جديد" else 'tracking' if choice == "متابعة الطلبات" else 'approvals'

# --- الصفحة 1: تقديم الطلب (النموذج الموحد الأصلي 100%) ---
if st.session_state.page == 'form':
    if st.session_state.request_count >= 3:
        st.error("⚠️ عذراً، لقد استنفدت الحد الأقصى للطلبات (3 طلبات فقط).")
    elif st.session_state.last_request_date and (datetime.now() - st.session_state.last_request_date).days < 30:
        days_left = 30 - (datetime.now() - st.session_state.last_request_date).days
        st.warning(f"⚠️ يجب الانتظار {days_left} يوم إضافي لتقديم طلب جديد.")
    else:
        # الخطوة 1: الحقول الـ 5 المتجاورة (كما طلبتِ في البداية)
        st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
            r_col, _ = st.columns([1, 4])
            with r_col: st.text_input("رقم الطلب", value=st.session_state.order_id, disabled=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: st.text_input("الرقم الوظيفي")
            with c2: st.text_input("الاسم الكامل")
            with c3: st.text_input("المسمى")
            with c4: st.text_input("القسم")
            with c5: st.date_input("تاريخ التعيين")
            st.markdown('</div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # الخطوة 2: الملاحظات والمرفقات
        st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
            c6, c7 = st.columns(2)
            with c6: req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
            with c7: st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
            
            if req_type in ["تعديل مهنة", "إنهاء خدمة"]:
                st.markdown(f'<div style="background:#fff9e6; padding:10px; border-radius:8px; border-right:5px solid #ffd43b; margin-bottom:10px;">📎 مرفق مطلوب لطلب {req_type}</div>', unsafe_allow_html=True)
                st.file_uploader("تحميل المرفق الرسمي", key="up_file")

            st.text_area("ملاحظات إضافية تفصيلية", height=120)
            c9, c10 = st.columns([3, 1])
            with c9: st.file_uploader("توقيع الموظف", key="sig_user")
            with c10: 
                if st.button("إرسال الطلب", use_container_width=True):
                    st.session_state.request_count += 1
                    st.session_state.last_request_date = datetime.now()
                    st.session_state.stage_start_date = datetime.now()
                    st.success("تم الإرسال بنجاح!")
                    time.sleep(1); st.session_state.page = 'tracking'; st.rerun()
            st.markdown('</div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة 2: متابعة الطلبات (الجدول المفقود + زر الطباعة) ---
elif st.session_state.page == 'tracking':
    st.markdown("### 🔍 سجل الطلبات والمتابعة")
    st.markdown('<div class="content-box"><div class="form-body">', unsafe_allow_html=True)
    st.markdown(f"""
        <table class="styled-table" style="width:100%">
            <thead><tr style="background:#5d5fef; color:white;"><th>رقم الطلب</th><th>النوع</th><th>التاريخ</th><th>الحالة</th></tr></thead>
            <tbody><tr><td>{st.session_state.order_id}</td><td>طلب نشط</td><td>{datetime.now().strftime('%Y-%m-%d')}</td><td>بانتظار الاعتماد</td></tr></tbody>
        </table>
    """, unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("📄 طباعة الطلب وتصديره"):
        st.info("جاري تجهيز النسخة للطباعة...")
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- الصفحة 3: الاعتمادات (الخانات الـ 4 + Dashboard + السبب الإلزامي) ---
elif st.session_state.page == 'approvals':
    # الإحصائيات (Dashboard)
    d1, d2, d3 = st.columns(3)
    with d1: st.markdown('<div class="stat-card"><div class="stat-val">1</div><div class="stat-label">طلبات نشطة</div></div>', unsafe_allow_html=True)
    with d2: st.markdown('<div class="stat-card"><div class="stat-val" style="color:red;">0</div><div class="stat-label">تجاوزت الـ 45 يوم</div></div>', unsafe_allow_html=True)
    with d3: st.markdown('<div class="stat-card"><div class="stat-val" style="color:green;">12</div><div class="stat-label">مكتملة</div></div>', unsafe_allow_html=True)
    
    st.divider()
    order_id_sel = st.selectbox("اختر الطلب للمراجعة:", ["--- اختر ---", st.session_state.order_id])
    
    if order_id_sel != "--- اختر ---":
        remaining = 45 - (datetime.now() - st.session_state.stage_start_date).days
        st.markdown(f'<div class="notification-timer">📢 متبقي للمسؤول {remaining} يوم لاتخاذ القرار ⏳</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        stages = ["المدير المباشر", "الموارد البشرية", "المدير العام"]
        
        for i, name in enumerate(stages, 1):
            with [col1, col2, col3][i-1]:
                active = st.session_state.stage == i
                st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>{i}️⃣ {name}</b></div>', unsafe_allow_html=True)
                st.text_input("الاسم", key=f"nm{i}", disabled=not active)
                st.text_input("المنصب", key=f"ps{i}", disabled=not active)
                st.text_input("الوظيفة", key=f"jb{i}", disabled=not active)
                st.date_input("التاريخ", key=f"dt{i}", disabled=not active)
                st.file_uploader("التوقيع", key=f"sg{i}", disabled=not active)
                res = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key=f"rs{i}", disabled=not active)
                
                if active and res in ["موافق", "مرفوض"]:
                    reason = st.text_area(f"مبررات القرار (إلزامي لـ {res})", key=f"rea{i}")
                    if st.button(f"حفظ اعتماد {name}"):
                        if reason:
                            if res == "موافق":
                                st.session_state.stage += 1
                                st.session_state.stage_start_date = datetime.now()
                                st.rerun()
                            else: st.error("تم رفض الطلب")
                        else: st.warning("يجب كتابة المبررات")

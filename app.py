import streamlit as st
from datetime import datetime
import time
import random

# 1. إعداد الصفحة والتنسيق (الأصيل والثابت)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

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

    .step-block { position: relative; padding-right: 60px; margin-bottom: 30px; }
    .step-block::before {
        content: ""; position: absolute; right: 28px; top: 45px; bottom: -45px;
        width: 3px; background-color: #5d5fef; z-index: 1; opacity: 0.2;
    }
    .step-block:last-child::before { display: none; }
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

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    .stTextArea>div>div>textarea { border-radius: 8px !important; text-align: right !important; font-size: 14px !important; }
    label { font-size: 12px !important; font-weight: bold !important; color: #475569 !important;}

    .styled-table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border-radius: 10px; overflow: hidden; }
    .styled-table thead tr { background-color: #5d5fef; color: white; text-align: right; }
    .styled-table th, .styled-table td { padding: 12px 15px; border-bottom: 1px solid #eee; font-size: 13px; }

    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    .attachment-box { background-color: #fff9e6; border: 1px dashed #ffd43b; padding: 12px; border-radius: 10px; margin-bottom: 15px; border-right: 5px solid #ffd43b; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (لتخزين البيانات والتنقل)
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"

# 3. الهيدر الرسمي
st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>قسم الموارد البشرية - بوابة الموظفين</p></div></div>', unsafe_allow_html=True)

# القائمة الجانبية للتنقل
with st.sidebar:
    st.title("⚙️ الخيارات")
    choice = st.selectbox("القائمة:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"], 
                          index=0 if st.session_state.page == 'form' else 1 if st.session_state.page == 'tracking' else 2)
    st.session_state.page = 'form' if choice == "تقديم طلب جديد" else 'tracking' if choice == "متابعة الطلبات" else 'approvals'

# --- الصفحة 1: تقديم الطلب (النموذج الأصلي + الإضافات) ---
if st.session_state.page == 'form':
    # الخطوة 1
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        # إضافة حقل رقم الطلب دون تغيير النموذج
        r_col, _ = st.columns([1, 4])
        with r_col: st.text_input("رقم الطلب", value=st.session_state.order_id, disabled=True)
        
        c1, c2, c3, c4, c5 = st.columns(5) # الـ 5 حقول الأصلية
        with c1: st.text_input("الرقم الوظيفي")
        with c2: st.text_input("الاسم الكامل")
        with c3: st.text_input("المسمى")
        with c4: st.text_input("القسم")
        with c5: st.date_input("تاريخ التعيين")
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c6, c7 = st.columns(2)
        with c6: req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
        with c7: st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        
        # إضافة المرفق الشرطي
        if req_type in ["تعديل مهنة", "إنهاء خدمة"]:
            st.markdown(f'<div class="attachment-box">📎 <b>مرفق مطلوب:</b> يرجى تحميل الوثائق الرسمية الخاصة بطلب ({req_type})</div>', unsafe_allow_html=True)
            st.file_uploader("تحميل المستندات", type=['pdf', 'png', 'jpg'], key="file_up")

        # الملاحظات الكبيرة الأصلية
        st.text_area("ملاحظات إضافية تفصيلية", height=120, placeholder="اكتب ملاحظاتك هنا...")
        
        c9, c10 = st.columns([3, 1])
        with c9: st.file_uploader("توقيع الموظف", type=['png', 'jpg'], key="emp_sig")
        with c10: 
            if st.button("إرسال الطلب الآن", use_container_width=True):
                st.success(f"🎉 تم إرسال الطلب رقم {st.session_state.order_id} بنجاح!")
                time.sleep(1.5)
                st.session_state.page = 'tracking'
                st.rerun()
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة 2: متابعة الطلبات (جدول مستقل) ---
elif st.session_state.page == 'tracking':
    st.markdown("### 🔍 سجل الطلبات المقدمة")
    st.markdown(f"""
    <div class="content-box">
        <div class="form-body">
            <table class="styled-table">
                <thead>
                    <tr><th>رقم الطلب</th><th>نوع الطلب</th><th>تاريخ التقديم</th><th>الحالة</th></tr>
                </thead>
                <tbody>
                    <tr><td>{st.session_state.order_id}</td><td>طلب حالي</td><td>{datetime.now().strftime('%Y-%m-%d')}</td><td>بانتظار الاعتماد</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- الصفحة 3: الاعتمادات (نظام الاختيار + التسلسل) ---
elif st.session_state.page == 'approvals':
    st.markdown("### ✅ منصة اعتماد الطلبات")
    
    # إضافة ميزة اختيار الطلب قبل البدء
    order_select = st.selectbox("اختر الطلب من السجل للمراجعة والاعتماد:", ["--- اختر من القائمة ---", f"{st.session_state.order_id} - طلب مقدم"])
    
    if order_select != "--- اختر من القائمة ---":
        st.info(f"مراجعة: {order_select}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            active = st.session_state.stage == 1
            st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>1️⃣ المدير المباشر</b></div>', unsafe_allow_html=True)
            st.text_input("الاسم", key="m_n", disabled=not active)
            m_res = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key="m_r", disabled=not active)
            if active and st.button("اعتماد وإرسال لـ HR"):
                if m_res == "موافق": st.session_state.stage = 2; st.rerun()

        with col2:
            active = st.session_state.stage == 2
            st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>2️⃣ الموارد البشرية</b></div>', unsafe_allow_html=True)
            st.text_input("الاسم ", key="h_n", disabled=not active)
            h_res = st.selectbox("القرار ", ["قيد الانتظار", "موافق", "مرفوض"], key="h_r", disabled=not active)
            if active and st.button("اعتماد وإرسال للمدير العام"):
                if h_res == "موافق": st.session_state.stage = 3; st.rerun()

        with col3:
            active = st.session_state.stage == 3
            st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>3️⃣ المدير العام</b></div>', unsafe_allow_html=True)
            st.text_input("الاسم  ", key="c_n", disabled=not active)
            c_res = st.selectbox("القرار  ", ["قيد الانتظار", "موافق", "مرفوض"], key="c_r", disabled=not active)
            if active and st.button("إتمام الاعتماد النهائي"):
                if c_res == "موافق": st.session_state.stage = 4; st.balloons(); st.success("تم اعتماد الطلب كلياً")
    else:
        st.warning("الرجاء اختيار طلب من القائمة أعلاه لبدء عملية الاعتماد.")

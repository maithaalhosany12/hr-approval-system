import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة والتنسيق (ثابت تماماً)
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

    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; margin-bottom: 20px; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 20px 25px; }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    
    .styled-table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border-radius: 10px; overflow: hidden; }
    .styled-table thead tr { background-color: #5d5fef; color: white; text-align: right; }
    .styled-table th, .styled-table td { padding: 12px 15px; border-bottom: 1px solid #eee; font-size: 13px; }

    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; box-shadow: 0 4px 12px rgba(93,95,239,0.1); }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'selected_order' not in st.session_state: st.session_state.selected_order = None

# الهيدر
st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>نظام الاعتمادات الذكي</p></div></div>', unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإجراءات")
    choice = st.selectbox("انتقل إلى:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"], index=0 if st.session_state.page == 'form' else 1 if st.session_state.page == 'tracking' else 2)
    if choice == "تقديم طلب جديد": st.session_state.page = 'form'
    elif choice == "متابعة الطلبات": st.session_state.page = 'tracking'
    else: st.session_state.page = 'approvals'

# --- صفحة تقديم الطلب (ثابتة) ---
if st.session_state.page == 'form':
    st.markdown('<div class="content-box"><div class="step-header">📝 نموذج طلب جديد</div><div class="form-body">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.text_input("الرقم الوظيفي")
    with c2: st.text_input("الاسم الكامل")
    with c3: st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة"])
    if st.button("إرسال الطلب", use_container_width=True):
        st.success("تم الإرسال بنجاح!")
        time.sleep(1)
        st.session_state.page = 'tracking'
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- صفحة متابعة الطلبات (ثابتة) ---
elif st.session_state.page == 'tracking':
    st.markdown("<h3>🔍 سجل الطلبات العام</h3>", unsafe_allow_html=True)
    st.markdown('<table class="styled-table"><thead><tr><th>رقم الطلب</th><th>الموظف</th><th>الحالة</th></tr></thead><tbody><tr><td>#1028</td><td>أحمد علي</td><td>بانتظار المدير المباشر</td></tr></tbody></table>', unsafe_allow_html=True)

# --- صفحة الاعتمادات (تحديث: الاختيار من السجل) ---
elif st.session_state.page == 'approvals':
    
    # 1. عرض سجل الطلبات المتاحة للاعتماد أولاً
    st.markdown("### 📋 طلبات بانتظار الاعتماد")
    st.markdown("""
    <div style='background: white; padding: 15px; border-radius: 10px; border: 1px solid #eee;'>
    <p style='font-size: 13px; color: #666;'>يرجى اختيار الطلب الذي ترغب في مراجعته من القائمة أدناه:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # محاكاة لسجل الطلبات
    order_options = ["اختر طلباً...", "طلب رقم #1028 - أحمد علي (تعديل مهنة)", "طلب رقم #1029 - سارة محمد (نقل داخلي)"]
    selected = st.selectbox("سجل الطلبات الواردة:", order_options, label_visibility="collapsed")
    
    if selected != "اختر طلباً...":
        st.session_state.selected_order = selected
        st.markdown(f"---")
        st.markdown(f"#### 🔎 معالجة: {selected}")
        
        col_m, col_hr, col_ceo = st.columns(3)
        
        # المرحلة 1: المدير المباشر
        with col_m:
            is_active = st.session_state.stage == 1
            card_class = "active-card" if is_active else "locked-card"
            st.markdown(f'<div class="approval-card {card_class}"><b>1️⃣ المدير المباشر</b></div>', unsafe_allow_html=True)
            st.text_input("الاسم", key="m_name", disabled=not is_active)
            m_dec = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key="m_dec", disabled=not is_active)
            if is_active:
                if st.button("حفظ واعتماد المرحلة 1", use_container_width=True):
                    if m_dec == "موافق":
                        st.session_state.stage = 2
                        st.rerun()
                    else: st.warning("يجب الموافقة للتحويل")

        # المرحلة 2: الموارد البشرية
        with col_hr:
            is_active = st.session_state.stage == 2
            card_class = "active-card" if is_active else "locked-card"
            st.markdown(f'<div class="approval-card {card_class}"><b>2️⃣ الموارد البشرية</b></div>', unsafe_allow_html=True)
            st.text_input("الاسم ", key="hr_name", disabled=not is_active)
            hr_dec = st.selectbox("القرار ", ["قيد الانتظار", "موافق", "مرفوض"], key="hr_dec", disabled=not is_active)
            if is_active:
                if st.button("حفظ واعتماد المرحلة 2", use_container_width=True):
                    if hr_dec == "موافق":
                        st.session_state.stage = 3
                        st.rerun()
                    else: st.warning("يجب الموافقة للتحويل")

        # المرحلة 3: المدير العام
        with col_ceo:
            is_active = st.session_state.stage == 3
            card_class = "active-card" if is_active else "locked-card"
            st.markdown(f'<div class="approval-card {card_class}"><b>3️⃣ المدير العام</b></div>', unsafe_allow_html=True)
            st.text_input("الاسم  ", key="ceo_name", disabled=not is_active)
            ceo_dec = st.selectbox("القرار  ", ["قيد الانتظار", "موافق", "مرفوض"], key="ceo_dec", disabled=not is_active)
            if is_active:
                if st.button("إتمام الاعتماد الكلي", use_container_width=True):
                    if ceo_dec == "موافق":
                        st.session_state.stage = 4
                        st.balloons()
                        st.success("تم إغلاق الطلب بنجاح")
    else:
        st.info("💡 الرجاء اختيار طلب من القائمة المنسدلة أعلاه للبدء في إجراءات الاعتماد.")

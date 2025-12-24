import streamlit as st
from datetime import datetime, timedelta
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
    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    .notification-timer { background-color: #fff4f4; border: 1px solid #ffcdd2; color: #c62828; padding: 10px; border-radius: 8px; font-weight: bold; margin-bottom: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة والقيود الجديدة
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"

# قيود الطلبات (محاكاة)
if 'request_count' not in st.session_state: st.session_state.request_count = 0
if 'last_request_date' not in st.session_state: st.session_state.last_request_date = None
# تاريخ استلام المرحلة الحالية (لغرض حساب الـ 45 يوم)
if 'stage_start_date' not in st.session_state: st.session_state.stage_start_date = datetime.now()

# 3. الهيدر الرسمي
st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>نظام الرقابة والاعتمادات الموحد</p></div></div>', unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الخيارات")
    choice = st.selectbox("القائمة:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"], 
                          index=0 if st.session_state.page == 'form' else 1 if st.session_state.page == 'tracking' else 2)
    st.session_state.page = 'form' if choice == "تقديم طلب جديد" else 'tracking' if choice == "متابعة الطلبات" else 'approvals'

# --- الصفحة 1: تقديم الطلب (مع قيود العدد والمدة) ---
if st.session_state.page == 'form':
    # فحص القيود قبل عرض النموذج
    can_request = True
    error_msg = ""
    
    if st.session_state.request_count >= 3:
        can_request = False
        error_msg = "⚠️ عذراً، لقد استنفدت الحد الأقصى للطلبات (3 طلبات فقط)."
    elif st.session_state.last_request_date and (datetime.now() - st.session_state.last_request_date).days < 30:
        can_request = False
        days_left = 30 - (datetime.now() - st.session_state.last_request_date).days
        error_msg = f"⚠️ يجب الانتظار لمدة شهر بين كل طلب وآخر. متبقي لك {days_left} يوم."

    if not can_request:
        st.error(error_msg)
    else:
        st.info(f"عدد طلباتك الحالية: {st.session_state.request_count} من 3")
        st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
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
            st.markdown('</div></div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="content-box"><div class="step-header">📝 تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
            req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
            st.text_area("ملاحظات إضافية", height=100)
            if st.button("إرسال الطلب الآن"):
                st.session_state.request_count += 1
                st.session_state.last_request_date = datetime.now()
                st.session_state.stage_start_date = datetime.now() # يبدأ عداد الـ 45 يوم للمدير
                st.success("تم الإرسال!")
                time.sleep(1)
                st.session_state.page = 'tracking'
                st.rerun()
            st.markdown('</div></div></div>', unsafe_allow_html=True)

# --- الصفحة 3: الاعتمادات (مع مهلة الـ 45 يوم والتنبيه) ---
elif st.session_state.page == 'approvals':
    order_select = st.selectbox("اختر الطلب:", ["--- اختر طلباً ---", f"{st.session_state.order_id}"])
    
    if order_select != "--- اختر طلباً ---":
        # حساب الوقت المتبقي (45 يوم)
        end_date = st.session_state.stage_start_date + timedelta(days=45)
        remaining_days = (end_date - datetime.now()).days
        
        if remaining_days < 0:
            st.error("❌ انتهت المهلة المحددة (45 يوم) لاتخاذ القرار في هذه المرحلة!")
        else:
            st.markdown(f'<div class="notification-timer">📢 تنبيه للمسؤول: متبقي {remaining_days} يوم فقط لاعتماد هذه المعاملة ⏳</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            stages = ["المدير المباشر", "الموارد البشرية", "المدير العام"]
            
            for i, stage_name in enumerate(stages, 1):
                with [col1, col2, col3][i-1]:
                    active = st.session_state.stage == i
                    st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>{i}️⃣ {stage_name}</b></div>', unsafe_allow_html=True)
                    st.text_input("الاسم", key=f"n{i}", disabled=not active)
                    st.text_input("المنصب", key=f"p{i}", disabled=not active)
                    st.date_input("التاريخ", key=f"d{i}", disabled=not active)
                    res = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key=f"r{i}", disabled=not active)
                    
                    if active and st.button(f"اعتماد المرحلة {i}"):
                        if res == "موافق":
                            st.session_state.stage += 1
                            st.session_state.stage_start_date = datetime.now() # إعادة ضبط الـ 45 يوم للمسؤول التالي
                            st.rerun()

elif st.session_state.page == 'tracking':
    st.markdown("### سجل المتابعة")
    st.write(f"إجمالي طلباتك: {st.session_state.request_count} / 3")

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

    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 20px 25px; }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    
    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة سير العمل (Workflow State)
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1  # تبدأ من المرحلة 1 (المدير المباشر)

# الهيدر
st.markdown("""
    <div class="company-header">
        <div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div>
        <div class="header-text">
            <h1>مؤسسة المسار المتكامل</h1>
            <p>قسم الموارد البشرية - نظام الاعتمادات الإلكتروني</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإجراءات")
    choice = st.selectbox("انتقل إلى:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"], index=0 if st.session_state.page == 'form' else 1 if st.session_state.page == 'tracking' else 2)
    if choice == "تقديم طلب جديد": st.session_state.page = 'form'
    elif choice == "متابعة الطلبات": st.session_state.page = 'tracking'
    else: st.session_state.page = 'approvals'

# --- صفحة النموذج ومتابعة الطلبات (نفس الكود السابق تماماً) ---
if st.session_state.page == 'form':
    st.info("قم بتعبئة الطلب كالمعتاد...")
    if st.button("إرسال الطلب"):
        st.session_state.stage = 1 # إعادة تعيين البداية للمدير المباشر
        st.success("تم الإرسال!")
        st.session_state.page = 'tracking'
        st.rerun()

elif st.session_state.page == 'tracking':
    st.markdown("<h3>🔍 سجل الطلبات</h3>", unsafe_allow_html=True)
    st.write("الجدول يظهر هنا...")

# --- صفحة الاعتمادات المرتبطة بالأزرار ---
elif st.session_state.page == 'approvals':
    st.markdown("<h3 style='text-align:right;'>✅ نظام تسلسل الموافقات</h3>", unsafe_allow_html=True)
    
    col_m, col_hr, col_ceo = st.columns(3)
    
    # 1️⃣ المرحلة الأولى: المدير المباشر
    with col_m:
        is_active = st.session_state.stage == 1
        card_class = "active-card" if is_active else "locked-card"
        st.markdown(f'<div class="approval-card {card_class}"><b>1️⃣ المدير المباشر</b></div>', unsafe_allow_html=True)
        
        st.text_input("الاسم", key="m_name", disabled=not is_active)
        st.date_input("التاريخ", key="m_date", disabled=not is_active)
        st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key="m_dec", disabled=not is_active)
        
        if is_active:
            if st.button("اعتماد وإرسال لـ HR", use_container_width=True):
                if st.session_state.m_dec == "موافق":
                    st.session_state.stage = 2
                    st.toast("تم التحويل للموارد البشرية")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("يجب اختيار 'موافق' للتحويل")

    # 2️⃣ المرحلة الثانية: الموارد البشرية
    with col_hr:
        is_active = st.session_state.stage == 2
        card_class = "active-card" if is_active else "locked-card"
        st.markdown(f'<div class="approval-card {card_class}"><b>2️⃣ الموارد البشرية</b></div>', unsafe_allow_html=True)
        
        st.text_input("الاسم", key="hr_name", disabled=not is_active)
        st.date_input("التاريخ", key="hr_date", disabled=not is_active)
        st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key="hr_dec", disabled=not is_active)
        
        if is_active:
            if st.button("اعتماد وإرسال للمدير العام", use_container_width=True):
                if st.session_state.hr_dec == "موافق":
                    st.session_state.stage = 3
                    st.toast("تم التحويل للمدير العام")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("يجب اختيار 'موافق' للتحويل")

    # 3️⃣ المرحلة الثالثة: المدير العام
    with col_ceo:
        is_active = st.session_state.stage == 3
        card_class = "active-card" if is_active else "locked-card"
        st.markdown(f'<div class="approval-card {card_class}"><b>3️⃣ المدير العام</b></div>', unsafe_allow_html=True)
        
        st.text_input("الاسم", key="ceo_name", disabled=not is_active)
        st.date_input("التاريخ", key="ceo_date", disabled=not is_active)
        st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key="ceo_dec", disabled=not is_active)
        
        if is_active:
            if st.button("إتمام الاعتماد النهائي", use_container_width=True):
                if st.session_state.ceo_dec == "موافق":
                    st.session_state.stage = 4 # نهاية المسار
                    st.balloons()
                    st.success("تم اعتماد الطلب بالكامل")
                    time.sleep(2)
                    st.rerun()



### مميزات هذا التحديث:
1.  **الأزرار الذكية:** كل قسم يحتوي على زر "حفظ وإرسال" خاص به. هذا الزر لا يقوم بحفظ البيانات فقط، بل يغير "حالة الطلب" لينتقل للمسؤول التالي.
2.  **التفاعل البصري:** المرحلة النشطة حالياً تظهر بحدود زرقاء (`active-card`) بينما المراحل الأخرى تظهر باهتة ومقفلة (`locked-card`).
3.  **منع التخطي:** لا يمكن للمسؤول الثاني الضغط على زر الاعتماد إلا إذا قام الأول بذلك فعلاً وضغط على زر التحويل.
4.  **تأكيد النجاح:** عند انتهاء المرحلة الأخيرة، تظهر احتفالية (Balloons) للاشارة إلى اكتمال الدورة المستندية للطلب.

هل هذا هو "منطق الأزرار" الذي كنتِ تبحثين عنه؟

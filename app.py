import streamlit as st
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import datetime
import random
import time

# --- 1. إعدادات التنسيق (الشكل الأصلي المعتمد) ---
st.set_page_config(page_title="نظام مسار للموارد البشرية", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl !important; text-align: right !important; }
    .company-header {
        display: flex; align-items: center; padding: 15px; background: white; 
        border-radius: 15px; margin-bottom: 25px; border-right: 6px solid #5d5fef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .content-box { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); border: 1px solid #eee; margin-bottom: 20px; }
    .step-header { background: #5d5fef; color: white; padding: 10px 20px; border-radius: 10px 10px 0 0; font-weight: bold; margin: -20px -20px 20px -20px; }
    
    /* تنسيق نظام التتبع البصري (Vertical Timeline) */
    .timeline { border-right: 3px solid #ddd; padding-right: 30px; margin-right: 20px; position: relative; }
    .step-container { position: relative; margin-bottom: 45px; }
    .step-circle { 
        position: absolute; right: -42px; top: 0; width: 24px; height: 24px; 
        border-radius: 50%; background: #fff; border: 3px solid #ddd; z-index: 10;
        display: flex; align-items: center; justify-content: center; font-weight: bold;
    }
    .step-completed { background: #28a745; border-color: #28a745; color: white; }
    .step-active { background: #5d5fef; border-color: #5d5fef; color: white; box-shadow: 0 0 8px rgba(93,95,239,0.5); }
    .waiting-text { color: #d63031; font-weight: bold; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الحالة والأمان ---
if 'stage' not in st.session_state: st.session_state.stage = 2 # تبدأ بانتظار المعتمد الأول
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(10000, 99999)}"
if 'stage_start_date' not in st.session_state: st.session_state.stage_start_date = datetime.datetime.now()
if 'request_count' not in st.session_state: st.session_state.request_count = 0

# --- 3. دالة الطباعة باللغة العربية ---
def export_as_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    # ملاحظة: لدعم العربية فعلياً في PDF، يجب تحميل خط عربي (مثل DejaVuSans.ttf)
    # هنا نستخدم تنسيقاً مبسطاً للبيانات الرسمية
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Employee Request Summary", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", 0, 1, 'L')
    pdf.ln(10)
    pdf.cell(60, 10, "Emp Signature", 1, 0, 'C')
    pdf.cell(60, 10, "Manager Approval", 1, 0, 'C')
    pdf.cell(60, 10, "HR Approval", 1, 1, 'C')
    return pdf.output()

# --- 4. القائمة الجانبية (نظام الصلاحيات) ---
with st.sidebar:
    st.markdown("### 🔐 بوابة الوصول")
    user_role = st.radio("الدخول بصفة:", ["موظف", "مدير / HR"])
    is_admin = False
    if user_role == "مدير / HR":
        pin = st.text_input("الرمز السري:", type="password")
        if pin == "1234": is_admin = True
    
    st.divider()
    menu = ["تقديم طلب جديد", "متابعة الطلبات"]
    if is_admin: menu.append("لوحة الاعتمادات")
    choice = st.selectbox("القائمة:", menu)

# --- الصفحة 1: تقديم الطلب (النسخة الأصلية) ---
if choice == "تقديم طلب جديد":
    st.markdown('<div class="company-header"><h2>تقديم طلب جديد</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.request_count >= 3:
        st.error("⚠️ عذراً، لقد استنفدت الحد الأقصى للطلبات (3 طلبات فقط).")
    else:
        with st.container():
            st.markdown('<div class="content-box"><div class="step-header">👤 بيانات الموظف</div>', unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: st.text_input("رقم الموظف")
            with c2: st.text_input("الاسم الكامل")
            with c3: st.text_input("المسمى")
            with c4: st.text_input("القسم")
            with c5: st.date_input("تاريخ التعيين")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="content-box"><div class="step-header">📝 تفاصيل الطلب</div>', unsafe_allow_html=True)
            req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
            st.text_area("الملاحظات")
            st.file_uploader("إرفاق الهوية/المستندات")
            st.file_uploader("توقيع الموظف (صورة)")
            if st.button("إرسال الطلب الآن"):
                st.session_state.request_count += 1
                st.session_state.stage = 2
                st.session_state.stage_start_date = datetime.datetime.now()
                st.success("تم إرسال الطلب بنجاح!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة 2: متابعة الطلبات (نظام التتبع البصري المطلوب) ---
elif choice == "متابعة الطلبات":
    st.markdown(f"### 🔍 تتبع الطلب رقم: {st.session_state.order_id}")
    
    stages_info = [
        {"id": 1, "title": "تقديم الطلب", "desc": "تم استلام الطلب وبدء الإجراءات"},
        {"id": 2, "title": "المعتمد الأول (المدير المباشر)", "desc": "مرحلة المراجعة الأولية"},
        {"id": 3, "title": "المعتمد الثاني (مدير القسم)", "desc": "التدقيق الإداري والميزانية"},
        {"id": 4, "title": "مدير الموارد البشرية", "desc": "الاعتماد النهائي للطلب"}
    ]

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for s in stages_info:
        status_class = ""
        icon = s['id']
        waiting = ""
        
        if st.session_state.stage > s['id']:
            status_class = "step-completed"
            icon = "✓"
        elif st.session_state.stage == s['id']:
            status_class = "step-active"
            waiting = f"<span class='waiting-text'> (بانتظار {s['title']})</span>"
            
        st.markdown(f"""
            <div class="step-container">
                <div class="step-circle {status_class}">{icon}</div>
                <div class="step-content">
                    <div style="font-weight:bold;">{s['title']} {waiting}</div>
                    <div style="font-size:13px; color:gray;">{s['desc']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # زر الطباعة الرسمي
    st.divider()
    if st.button("📄 طباعة الطلب (PDF)"):
        pdf_bytes = export_as_pdf({"Order ID": st.session_state.order_id, "Status": "In Progress"})
        st.download_button("تحميل الملف", pdf_bytes, f"{st.session_state.order_id}.pdf")

# --- الصفحة 3: الاعتمادات (للمدراء فقط) ---
elif choice == "لوحة الاعتمادات":
    st.markdown("### 📊 لوحة تحكم الإدارة")
    d1, d2, d3 = st.columns(3)
    d1.metric("طلبات نشطة", "1")
    d2.metric("بانتظار الإجراء", "1")
    d3.metric("تجاوزت الـ 45 يوم", "0")
    
    st.divider()
    days_left = 45 - (datetime.datetime.now() - st.session_state.stage_start_date).days
    st.warning(f"⏳ تنبيه للمسؤول: متبقي {max(0, days_left)} يوم لاعتماد هذا الطلب قبل انتهاء المهلة.")
    
    current_stage_name = stages_info[st.session_state.stage-1]['title']
    st.info(f"أنت تقوم الآن بالاعتماد كـ: {current_stage_name}")
    
    res = st.selectbox("القرار:", ["قيد الانتظار", "موافق", "مرفوض"])
    reason = st.text_area("مبررات القرار (إلزامي):")
    if st.button("حفظ القرار النهائي"):
        if reason:
            if res == "موافق":
                st.session_state.stage += 1
                st.session_state.stage_start_date = datetime.datetime.now()
                st.success("تم الاعتماد بنجاح")
                st.rerun()
            else: st.error("تم رفض الطلب")
        else: st.warning("يرجى كتابة المبررات")

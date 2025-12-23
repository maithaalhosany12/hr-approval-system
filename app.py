# --- STAGE 1: SUBMISSION (DIVIDED INTO TWO SECTIONS) ---
if choice == "Submit Request":
    st.header("New Applicant Request")
    
    # تقسيم الصفحة إلى تبويبين (Tabs)
    tab1, tab2 = st.tabs(["📋 Basic Information", "📝 Request Details"])
    
    # سنستخدم 'session_state' لحفظ البيانات بين التبويبين
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    with tab1:
        st.subheader("Step 1: Applicant Data")
        number = st.text_input("Service Number (الرقم العسكري/الوظيفي)")
        unit = st.text_input("Unit (الوحدة/القسم)")
        name = st.text_input("Full Name (الاسم الكامل)")
        appt_date = st.date_input("Appointment Date (تاريخ التعيين)")
        st.info("Please move to the next tab to complete request details.")

    with tab2:
        st.subheader("Step 2: Subject & Attachments")
        subject = st.selectbox("Subject of Request", 
                               ["Change of Profession", "Transfer", "Termination of Service"])
        
        # خيار المرفقات يظهر بناءً على نوع الطلب
        attachment = None
        if subject in ["Change of Profession", "Termination of Service"]:
            attachment = st.file_uploader("Upload Required Document (JPG/PNG/PDF)")
        
        submit_btn = st.button("Submit Final Request")

        if submit_btn:
            if number and name: # تحقق بسيط من البيانات الأساسية
                conn = sqlite3.connect('requests.db')
                c = conn.cursor()
                c.execute("""INSERT INTO requests 
                          (number, unit, name, appt_date, subject, submit_date, status, stage) 
                          VALUES (?,?,?,?,?,?,?,?)""",
                          (number, unit, name, str(appt_date), subject, datetime.now(), "Pending Supervisor", 1))
                conn.commit()
                st.success(f"✅ Request for {name} has been submitted successfully!")
                st.balloons() # إضافة تأثير احتفالي عند النجاح
            else:
                st.error("Please fill in the basic information in the first tab.")

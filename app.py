import streamlit as st
import pandas as pd
import pickle

# 1. تحميل الموديل
with open('bullying_mode (1).pkl', 'rb') as f:
    model = pickle.load(f)

# 2. تصميم واجهة الموقع
st.title("🛡️ منصة أمان - الكشف المبكر عن التنمر")
st.write("أهلاً بكِ في مشروع التخرج. أدخلي البيانات بالأسفل للتوقع:")

# هنا هنضيف خانات للمدخلات 
age = st.number_input("العمر", min_value=10, max_value=20)
gender = st.selectbox("الجنس", ["Male", "Female"])

# 3. زر التوقع
if st.button("تحليل البيانات"):
    
    st.success("تم التحليل بنجاح!")
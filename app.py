import streamlit as st
import pandas as pd
import pickle
import requests
import io

# دالة مطورة لتحميل الموديل من جوجل درايف
@st.cache_resource
def load_model():
    file_id = '1MQDoy1-5vH4spDp0a10S2sVTUZma2mbT'
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return pickle.load(io.BytesIO(response.content))
        else:
            st.error("فشل الاتصال بجوجل درايف")
            return None
    except Exception as e:
        st.error(f"خطأ في التحميل: {e}")
        return None

st.set_page_config(page_title="منصة أمان", layout="centered")

st.title("🛡️ منصة أمان")
st.subheader("الكشف المبكر عن التنمر الإلكتروني")

try:
    model = load_model()
    if model:
        st.success("✅ النظام جاهز للتحليل")
        
        user_input = st.text_area("أدخل النص المراد تحليله هنا:", placeholder="اكتب الرسالة التي تريد فحصها...")
        
        if st.button("تحليل النص"):
            if user_input:
                prediction = model.predict([user_input])
                result = "⚠️ نص يحتوي على تنمر" if prediction[0] == 1 else "✅ نص آمن"
                if prediction[0] == 1:
                    st.warning(f"النتيجة: {result}")
                else:
                    st.info(f"النتيجة: {result}")
            else:
                st.error("من فضلك أدخل نصاً أولاً")

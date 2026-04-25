import streamlit as st
import pandas as pd
import pickle
import requests
import io

# دالة مطورة لتحميل الملفات الكبيرة من جوجل درايف وتخطي رسالة التأكيد
@st.cache_resource
def load_model():
    file_id = '1MQDoy1-5vH4spDp0a10S2sVTUZma2mbT'
    url = "https://docs.google.com/uc?export=download"
    
    session = requests.Session()
    # طلب أول للحصول على توكن التأكيد إذا وجد
    response = session.get(url, params={'id': file_id}, stream=True)
    
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        # طلب ثاني باستخدام توكن التأكيد
        response = session.get(url, params={'id': file_id, 'confirm': token}, stream=True)
    
    if response.status_code == 200:
        return pickle.load(io.BytesIO(response.content))
    else:
        st.error("فشل في تحميل الموديل من جوجل درايف")
        return None

st.set_page_config(page_title="منصة أمان", layout="centered")

st.title("🛡️ منصة أمان")
st.subheader("الكشف المبكر عن التنمر الإلكتروني")

try:
    model = load_model()
    if model:
        st.success("✅ النظام جاهز للتحليل")
        
        user_input = st.text_area("أدخل النص المراد تحليله هنا:", placeholder="اكتب هنا...")
        
        if st.button("تحليل النص"):
            if user_input:
                # تنفيذ التوقع
                prediction = model.predict([user_input])
                result = "⚠️ نص يحتوي على تنمر" if prediction[0] == 1 else "✅ نص آمن"
                
                if prediction[0] == 1:
                    st.warning(f"النتيجة: {result}")
                else:
                    st.info(f"النتيجة: {result}")
            else:
                st.error("من فضلك أدخل نصاً أولاً")
except Exception as e:
    st.error(f"حدث خطأ تقني: {e}")

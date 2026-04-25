import streamlit as st
import pandas as pd
import pickle
import gdown
import os

# دالة تحميل الموديل
@st.cache_resource
def load_model():
    file_id = '1MQDoy1-5vH4spDp0a10S2sVTUZma2mbT'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    with open(output, 'rb') as f:
        return pickle.load(f)

st.set_page_config(page_title="منصة أمان", layout="centered")
st.title("🛡️ منصة أمان")
st.subheader("الكشف المبكر عن التنمر الإلكتروني")

try:
    model = load_model()
    st.success("✅ النظام جاهز للتحليل")
    
    user_input = st.text_area("أدخل النص المراد تحليله هنا:")
    
    if st.button("تحليل النص"):
        if user_input:
            # التعديل هنا: بنبعت النص للموديل كقائمة (List) عشان يفهم إنه نص
            prediction = model.predict([user_input])
            
            # لو الموديل لسه بيطلع خطأ، جربي دي:
            # prediction = model.predict(pd.Series([user_input]))
            
            result = "⚠️ نص يحتوي على تنمر" if prediction[0] == 1 else "✅ نص آمن"
            st.info(f"النتيجة: {result}")
        else:
            st.error("من فضلك أدخل نصاً")
except Exception as e:
    # الرسالة دي هتظهر لو الموديل لسه مش متوافق مع النصوص
    st.error(f"حدث خطأ: الموديل يحتاج لبيانات رقمية. تأكدي من حفظ الموديل الصحيح في Colab.")

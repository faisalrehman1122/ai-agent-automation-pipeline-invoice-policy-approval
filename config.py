import os

def get_openai_api_key():
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and st.secrets and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets['OPENAI_API_KEY']
    except:
        pass
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    return None

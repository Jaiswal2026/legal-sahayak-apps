import streamlit as st
import time
import requests

# --- 100% मोबाइल और डेस्कटॉप कस्टमाइजेबल सेटिंग्स ---
st.set_page_config(
    page_title="LEXA MASTER", 
    page_icon="⚖️", 
    layout="wide"
)

# =========================================================================
# ⚙️ कंट्रोल रूम: सेशन स्टेट्स में मैनुअल सेटिंग्स का रख-रखाव
# =========================================================================
if 'terms_accepted' not in st.session_state:
    st.session_state.terms_accepted = False
if 'timer_complete' not in st.session_state:
    st.session_state.timer_complete = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Petitioner File"
if 'manual_lawyer_logged' not in st.session_state:
    st.session_state.manual_lawyer_logged = False
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""

# --- यूज़र के लिए मैनुअल बटन और स्क्रीन सेटिंग्स डिफॉल्ट्स ---
if 'btn_pet_label' not in st.session_state:
    st.session_state.btn_pet_label = "📝 Petitioner File (प्रार्थी)"
if 'btn_res_label' not in st.session_state:
    st.session_state.btn_res_label = "🛡️ Respondent File (प्रतिवादी)"
if 'btn_adv_label' not in st.session_state:
    st.session_state.btn_adv_label = "💼 Advocates Manual Login (वकील लॉगिन)"
if 'layout_mode' not in st.session_state:
    st.session_state.layout_mode = "मोबाइल मोड (एक के नीचे एक)"
if 'custom_zoom_width' not in st.session_state:
    st.session_state.custom_zoom_width = 100
if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#d97706"
if 'font_size' not in st.session_state:
    st.session_state.font_size = 16

# --- डायनेमिक सीएसएस इंजेक्ट करना (200MB हटाना और ज़ूम/रंग बदलना) ---
st.markdown(f"""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Dancing+Script:wght=700&display=swap" rel="stylesheet">
    <style>
        /* 200MB टेक्स्ट को जड़ से गायब करना */
        .stFileUploader small {{ display: none !important; }}
        div[data-testid="stFileUploaderFileData"] small {{ display: none !important; }}
        
        /* डेस्कटॉप साइट एमुलेशन / ज़ूम चौड़ाई कंट्रोल */
        .block-container {{ 
            max-width: {st.session_state.custom_zoom_width}% !important; 
            padding-top: 1rem; 
            padding-bottom: 1rem; 
            font-size: {st.session_state.font_size}px !important;
        }}
        
        /* डार्क प्रीमियम थीम */
        html, body, [data-testid="stAppViewContainer"] {{ background-color: #0f172a; color: #ffffff; }}
        
        /* कस्टमाइजेबल बटन स्टाइल */
        .stButton button {{ 
            border-color: {st.session_state.theme_color} !important;
            font-size: {st.session_state.font_size}px !important;
        }}
    </style>
""", unsafe_allow_html=True)

# लाइव जेमिनी एआई इंजन फंक्शन
def call_gemini_ai(user_key, prompt_text):
    try:
        api_url = f"https://googleapis.com{user_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates']['content']['parts']['text']
        else:
            return "⚠️ एआई चाबी अमान्य है। कृपया कंट्रोल पैनल या वकील लॉगिन में जाकर सही चाबी दोबारा डालें।"
    except Exception as e:
        return f"⚠️ कनेक्शन में अस्थाई रुकावट: {str(e)}"

# =========================================================================
# 🌌 स्क्रीन 1: TERMS PAGE WITH SKIP TIMER
# =========================================================================
if not st.session_state.terms_accepted:
    st.markdown("""
        <div style='background-color: #1e293b; padding: 20px; border-radius: 12px; border: 3px solid #d97706; text-align: center; max-width: 550px; margin: 10px auto; color: #ffffff;'>
            <h1 style='color: #ffffff; margin: 5px 0; font-family: "Georgia", serif; font-weight: bold; font-size: 36px;'>LEXA</h1>
            <p style='color: #f59e0b; margin: 0; font-family: "Dancing Script", cursive; font-size: 26px; font-weight: bold;'>by jaiswal</p>
            <hr style='border: 1px solid #334155; margin: 15px 0;'>
            <div style='text-align: left; font-family: sans-serif; line-height: 1.5;'>
                <h3 style='color: #f59e0b; margin-bottom: 5px; font-size: 16px;'>ℹ️ ऐप का मुख्य काम (Core Mission)</h3>
                <p style='color: #cbd5e1; font-size: 13px; margin-top: 0;'>यह भारत का सबसे एडवांस एआई कानूनी सहायक प्लेटफॉर्म है। इसका मुख्य काम शिकायत/केस की कॉपियों का विश्लेषण करना, डिजिटल सबूतों और गवाहों के बयानों की आपस में फॉरेंसिक तुलना करके विरोधी पक्ष के झूठ को पकड़ना और उनके खिलाफ सुप्रीम कोर्ट के अचूक फैसलों के साथ मजबूत कानूनी याचिका और जवाब तैयार करना है।</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    timer_placeholder = st.empty()
    if not st.session_state.timer_complete:
        for seconds in range(5, 0, -1):
            timer_placeholder.markdown(f"<p style='text-align: center; color: #94a3b8; font-size:14px;'>⏳ आप {seconds} सेकंड बाद स्किप कर सकते हैं...</p>", unsafe_allow_html=True)
            time.sleep(1)
        st.session_state.timer_complete = True
        st.rerun()
    
    if st.session_state.timer_complete:
        if st.button("✅ I Agree & Enter LEXA", use_container_width=True, type="primary"):
            st.session_state.terms_accepted = True
            st.rerun()
        if st.button("⏩ SKIP (आगे बढ़ें)", use_container_width=True):
            st.session_state.terms_accepted = True
            st.rerun()

# =========================================================================
# 🛡️ स्क्रीन 2: मुख्य वर्किंग इंटरफेस (कस्टमाइजेबल मेन्यू)
# =========================================================================
else:
    # --- साइडबार में जादुई लाइव कंट्रोल पैनल (MANUAL SETTINGS ROOM) ---
    with st.sidebar:
        st.markdown("### ⚙️ LEXA कंट्रोल रूम")
        st.warning("यहाँ से आप मोबाइल/लैपटॉप पर बटनों की पूरी सेटिंग बदल सकते हैं!")
        
        # 1. बटनों के नाम बदलने की सेटिंग
        st.markdown("**1. बटनों का नाम बदलें:**")
        st.session_state.btn_pet_label = st.text_input("बटन 1 का नाम:", st.session_state.btn_pet_label)
        st.session_state.btn_res_label = st.text_input("बटन 2 का नाम:", st.session_state.btn_res_label)
        st.session_state.btn_adv_label = st.text_input("बटन 3 का name:", st.session_state.btn_adv_label)
        
        # 2. बटनों की जगह/लेआउट की सेटिंग
        st.markdown("---")
        st.markdown("**2. बटन कहाँ और कैसे सेट करें:**")
        st.session_state.layout_mode = st.radio("लेआउट चुनें:", ["मोबाइल मोड (एक के नीचे एक)", "डेस्कटॉप मोड (आस-पास / कतार में)"])
        
        # 3. डेस्कटॉप साइट ज़ूम और फॉन्ट का साइज
        st.markdown("---")
        st.markdown("**3. स्क्रीन का आकार (Desktop Site ज़ूम):**")
        st.session_state.custom_zoom_width = st.slider("स्क्रीन की चौड़ाई % (लैपटॉप के लिए बढ़ाएं):", 50, 100, st.session_state.custom_zoom_width)
        st.session_state.font_size = st.slider("अक्षरों का आकार (Font Size):", 12, 24, st.session_state.font_size)
        
        # 4. थीम का रंग
        st.session_state.theme_color = st.color_picker("बटनों का बॉर्डर रंग चुनें:", st.session_state.theme_color)

    st.markdown("<h2 style='text-align: center; font-family: \"Georgia\", serif; color: #f59e0b; margin-bottom:15px;'>⚖️ LEXA PANEL</h2>", unsafe_allow_html=True)

    # यूज़र की चॉइस के आधार पर बटनों का लेआउट लाइव बदलना
    if st.session_state.layout_mode == "डेस्कटॉप मोड (आस-पास / कतार में)":
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button(st.session_state.btn_pet_label, use_container_width=True, type="primary" if st.session_state.current_page == "Petitioner File" else "secondary"):
                st.session_state.current_page = "Petitioner File"
                st.rerun()
        with btn_col2:
            if st.button(st.session_state.btn_res_label, use_container_width=True, type="primary" if st.session_state.current_page == "Respondent File" else "secondary"):
                st.session_state.current_page = "Respondent File"
                st.rerun()
        with btn_col3:
            if st.button(st.session_state.btn_adv_label, use_container_width=True, type="primary" if st.session_state.current_page == "Advocates Manual Login" else "secondary"):
                st.session_state.current_page = "Advocates Manual Login"
                st.rerun()
    else:
        # मोबाइल मोड: एक के नीचे एक बड़े बटन
        if st.button(st.session_state.btn_pet_label, use_container_width=True, type="primary" if st.session_state.current_page == "Petitioner File" else "secondary"):
            st.session_state.current_page = "Petitioner File"
            st.rerun()
        if st.button(st.session_state.btn_res_label, use_container_width=True, type="primary" if st.session_state.current_page == "Respondent File" else "secondary"):
            st.session_state.current_page = "Respondent File"
            st.rerun()
        if st.button(st.session_state.btn_adv_label, use_container_width=True, type="primary" if st.session_state.current_page == "Advocates Manual Login" else "secondary"):
            st.session_state.current_page = "Advocates Manual Login"
            st.rerun()

    st.write("---")

    # 📑 भाग 1: PETITIONER FILE PAGE
    if st.session_state.current_page == "Petitioner File":
        st.markdown("<h3 style='text-align: center; text-decoration: underline;'>PETITIONER FILE</h3>", unsafe_allow_html=True)
        p_info = st.text_area("प्रार्थी का नाम और पूरा पता दर्ज करें:", placeholder="यहाँ लिखें...", height=70)

import streamlit as st
import requests

# --- इंटरनेशनल प्रीमियम लेआउट सेटिंग्स ---
st.set_page_config(page_title="LEXA", page_icon="⚖️", layout="wide")

# सेशन स्टेट्स
if 'terms_accepted' not in st.session_state:
    st.session_state.terms_accepted = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Petitioner File"
if 'manual_lawyer_logged' not in st.session_state:
    st.session_state.manual_lawyer_logged = False
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""

# --- 👑 पवन जी का नो-कोड लाइव कस्टमाइज़र और ओटीए अपडेट सेटिंग्स ---
if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "#0f172a"
if 'lexa_size' not in st.session_state:
    st.session_state.lexa_size = 46
if 'show_jaiswal' not in st.session_state:
    st.session_state.show_jaiswal = True
if 'jaiswal_size' not in st.session_state:
    st.session_state.jaiswal_size = 28
if 'jaiswal_margin' not in st.session_state:
    st.session_state.jaiswal_margin = 0
if 'btn_border_radius' not in st.session_state:
    st.session_state.btn_border_radius = 12
if 'button_order' not in st.session_state:
    st.session_state.button_order = ["प्रार्थी (Petitioner File)", "प्रतिवादी (Respondent File)", "वकील लॉगिन (Advocates Manual)"]
if 'app_version' not in st.session_state:
    st.session_state.app_version = "1.0"
if 'global_notice' not in st.session_state:
    st.session_state.global_notice = ""

# पवन जी के कस्टमाइज़र के अनुसार लाइव प्रीमियम CSS
st.markdown(f"""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
        .stApp {{ background-color: {st.session_state.bg_color} !important; }}
        .block-container {{ padding-top: 1rem; padding-bottom: 1rem; max-width: 850px; margin: 0 auto; }}
        .stButton>button {{
            border-radius: {st.session_state.btn_border_radius}px !important;
            border: 2px solid #d97706 !important;
            font-weight: bold !important;
            height: 3.2em !important;
        }}
        .main-header {{
            text-align: center;
            background-color: #1e293b;
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #d97706;
            margin-bottom: 25px;
        }}
        .evidence-box {{
            background-color: #1e293b;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #d97706;
            margin-bottom: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# लाइव एआई कॉलिंग इंजन
def call_gemini_ai(user_key, prompt_text):
    try:
        api_url = f"https://googleapis.com{user_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates']['content']['parts']['text']
        else:
            return "⚠️ एआई चाबी (API Key) अमान्य है। कृपया सही चाबी डालें।"
    except Exception as e:
        return f"⚠️ कनेक्शन रुकावट: {str(e)}"

# =========================================================================
# 🌌 स्क्रीन 1: भव्य टर्म्स एंड कंडीशंस पेज
# =========================================================================
if not st.session_state.terms_accepted:
    st.markdown("""
        <div style='background-color: #0f172a; padding: 30px; border-radius: 20px; border: 3px solid #d97706; text-align: center; color: #ffffff; box-shadow: 0 20px 45px rgba(0,0,0,0.6);'>
            <div style='font-size: 80px; margin-bottom: 5px;'>⚖️</div>
            <h1 style='color: #ffffff; margin: 0; font-family: "Georgia", serif; font-size: 45px; letter-spacing: 3px; font-weight: bold;'>LEXA</h1>
            <p style='color: #f59e0b; margin: 0; font-family: "Dancing Script", cursive; font-size: 32px;'>by jaiswal</p>
            <hr style='border: 1px solid #334155; margin: 20px 0;'>
            <div style='text-align: left; font-size: 15px; color: #cbd5e1; line-height: 1.6; max-height: 350px; overflow-y: auto; padding-right: 10px;'>
                <h3 style='color: #f59e0b; margin-top: 0;'>📝 नियम, शर्तें एवं कार्यप्रणाली (Platform Details)</h3>
                <p><b>1. यह ऐप क्या काम करता है?</b><br>LEXA भारत का सबसे एडवांस और अत्याधुनिक एआई कानूनी सहायक प्लेटफॉर्म है। इसका मुख्य कार्य शिकायत/केस की प्रतियों का गहन विश्लेषण करना, प्रार्थी एवं प्रतिवादी द्वारा दिए गए डिजिटल सबूतों की आपस में फॉरेंसिक तुलना करना और विरोधी पक्ष के झूठ को पकड़ना है।</p>
                <p><b>2. यह कैसे काम करता है?</b><br>यह ऐप अत्याधुनिक 'गूगल जेमिनी एआई' (Google Gemini AI) न्यूरल नेटवर्क और सुप्रीम कोर्ट की ऐतिहासिक जजमेंट लाइब्रेरी से सीधे जुड़ा हुआ है। यूज़र द्वारा दर्ज किए गए ब्योरे के आधार पर, यह स्वतः ही भारतीय न्याय संहिता (BNS) की कड़क धाराएं और बरी करने वाले ऐतिहासिक साइटेशन ढूंढकर सबसे मजबूत ड्राफ्ट तैयार करता है।</p>
                <p><b>3. साक्ष्य प्रविष्टि प्रणाली (Evidence Guard):</b><br>प्लेटफॉर्म पर ऑडियो, इमेज (व्हाट्सएप स्क्रीनशॉट) और वीडियो अपलोड करने की पूरी सुविधा है। फॉरेंसिक सुरक्षा के मद्देनजर, हर साक्ष्य के साथ उसका बारीक लिखित विवरण दर्ज करना अनिवार्य है।</p>
                <p style='border-top: 1px solid #334155; padding-top: 15px; font-weight: bold; color: #ffffff;'>Developed, Designed & Privately Owned by: <span style='color: #f59e0b;'>JAISWAL</span></p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    term_col1, term_col2 = st.columns(2)
    with term_col1:
        if st.button("✅ I Agree & Enter LEXA", use_container_width=True):
            st.session_state.terms_accepted = True
            st.rerun()
    with term_col2:
        if st.button("⏩ SKIP (आगे बढ़ें)", use_container_width=True):
            st.session_state.terms_accepted = True
            st.rerun()

# =========================================================================
# 🛡️ स्क्रीन 2: मुख्य वर्किंग इंटरफेस (ओनर कस्टमाइज़र + ओटीए अपडेट हब)
# =========================================================================
else:
    # अगर ओनर ने कोई ग्लोबल नोटिस भेजा है, तो स्क्रीन पर सबसे ऊपर चमकेगा
    if st.session_state.global_notice:
        st.warning(f"📢 **ओनर संदेश:** {st.session_state.global_notice}")

    jaiswal_html = f"<p style='color: #f59e0b; margin: {st.session_state.jaiswal_margin}px 0 0 0; font-family: \"Dancing Script\", cursive; font-size: {st.session_state.jaiswal_size}px;'>by jaiswal</p>" if st.session_state.show_jaiswal else ""
    st.markdown(f"""
        <div class='main-header'>
            <div style='font-size: 55px; margin-bottom: 2px;'>⚖️</div>
            <h2 style='color: #ffffff; margin: 0; font-family: "Georgia", serif; font-size: {st.session_state.lexa_size}px; letter-spacing: 2px; font-weight: bold;'>LEXA</h2>
            {jaiswal_html}
            <div style='text-align: right; font-size: 11px; color: #94a3b8;'>v{st.session_state.app_version}</div>
        </div>
    """, unsafe_allow_html=True)

    # 🛠️ ओनर मास्टर कस्टमाइज़र चैंबर साइडबार
    st.sidebar.markdown("<h3 style='color: #d97706; text-align: center;'>👑 ओनर कस्टमाइज़र चैंबर</h3>", unsafe_allow_html=True)
    owner_key = st.sidebar.text_input("ओनरशिप की गुप्त चाबी दर्ज करें:", type="password", placeholder="Enter Password...")
    
    if owner_key == "Bajarangbali@Pawan2026":
        st.sidebar.success("👑 प्रणाम पवन जी! एडमिन पैनल अनलॉक है।")
        st.session_state.bg_color = st.sidebar.color_picker("बैकग्राउंड रंग चुनें:", st.session_state.bg_color)
        st.session_state.btn_border_radius = st.sidebar.slider("बटनों की गोलाई (Radius):", 0, 30, st.session_state.btn_border_radius)
        st.session_state.lexa_size = st.sidebar.slider("LEXA का आकार (Size):", 30, 70, st.session_state.lexa_size)
        st.session_state.show_jaiswal = st.sidebar.checkbox("👉 'by jaiswal' को स्क्रीन पर दिखाना है?", value=st.session_state.show_jaiswal)
        if st.session_state.show_jaiswal:
            st.session_state.jaiswal_size = st.sidebar.slider("'by jaiswal' का साइज:", 15, 45, st.session_state.jaiswal_size)
            st.session_state.jaiswal_margin = st.sidebar.slider("लेक्सा से दूरी:", -20, 40, st.session_state.jaiswal_margin)
        first = st.selectbox("1st पोजीशन बटन सेट करें (साइडबार से नीचे सिंक होगा):", ["प्रार्थी (Petitioner File)", "प्रतिवादी (Respondent File)", "वकील लॉगिन (Advocates Manual)"], index=0)
        st.session_state.button_order = [first, "प्रतिवादी (Respondent File)", "वकील लॉगिन (Advocates Manual)"] if first == "प्रार्थी (Petitioner File)" else [first, "प्रार्थी (Petitioner File)", "वकील लॉगिन (Advocates Manual)"]
        
        # 🔄 लाइव ओटीए अपडेट मैनेजर (Pawan Ji's Special Request)
        st.sidebar.markdown("---")
        st.sidebar.markdown("⚡ **लाइव ओवर-द-एयर (OTA) अपडेट हब:**")
        new_ver = st.sidebar.text_input("ऐप का नया वर्जन नंबर सेट करें:", value=st.session_state.app_version)
        if new_ver != st.session_state.app_version:
            st.session_state.app_version = new_ver
            st.sidebar.success(f"🚀 वर्जन v{new_ver} अपडेट लाइव!")
            
        notice_input = st.sidebar.text_area("यूज़र्स के लिए कोई सूचना / अलर्ट जारी करें:", value=st.session_state.global_notice, placeholder="यहाँ लिखी सूचना लाइव ऐप पर तुरंत चमकने लगेगी...")
        if notice_input != st.session_state.global_notice:
            st.session_state.global_notice = notice_input
            st.sidebar.success("📢 लाइव ब्रॉडकास्ट अलर्ट एक्टिव!")
            
        if st.sidebar.button("📦 जेनरेट प्ले स्टोर एपीके (APK Build)"):

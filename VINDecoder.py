import streamlit as st

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="VIN Decoder",
    layout="centered"
)

# --- STYL GOOGLE (Material Design) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #202124; font-family: 'Roboto', Arial, sans-serif; }
    h1 { color: #202124 !important; font-weight: 400 !important; text-align: center; padding-top: 10px; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #5f6368; font-size: 14px; margin-bottom: 40px; }
    .stRadio label { color: #202124 !important; }
    
    /* TUTAJ WKLEJASZ TE DWIE LINIJKI: */
    .stRadio p { color: #202124 !important; }
    div[role="radiogroup"] p { color: #202124 !important; }
    
    /* Cienka, widoczna ramka dla pola wpisywania VIN */
    .stTextInput input {
        border: 1px solid #dadce0 !important;
        border-radius: 4px !important;
        background-color: #ffffff !important;
        color: #202124 !important;
        padding: 12px !important;
    }
    /* Wygląd pola po kliknięciu (focus) */
    .stTextInput input:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 1px #1a73e8 !important;
        outline: none !important;
    }
    
    .stButton>button { 
        background-color: #1a73e8; 
        color: #ffffff; 
        border: none; 
        border-radius: 4px; 
        font-weight: 500; 
        width: 100%; 
        padding: 10px 24px;
        transition: 0.2s; 
    }
    .stButton>button:hover { 
        background-color: #1765cc; 
        color: #ffffff; 
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15); 
    }
    .footer-link { text-align: center; margin-top: 60px; font-size: 12px; color: #5f6368; border-top: 1px solid #dadce0; padding-top: 20px;}
    .footer-link a { color: #1a73e8; text-decoration: none; }
    
    .clean-error { color: #d93025; padding: 10px 0; font-weight: 500; }
    .clean-success { color: #1e8e3e; padding: 10px 0; font-weight: 500; }
    .clean-warning { color: #ea8600; padding: 10px 0; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)


# --- 1. SAAB DECODER LOGIC ---
def dekoduj_vin_saab(vin):
    vin = vin.strip().upper()
    if len(vin) != 17:
        return {"error": "Error: VIN must be exactly 17 characters long."}
    if not vin.startswith("YS3"):
        return {"error": f"Error: VIN {vin} does not match the 1986+ Saab standard. Expected 'YS3' prefix."}

    modele = {'A': 'Saab 900', 'B': 'Saab 99', 'C': 'Saab 9000', 'D': 'Saab 900 (2nd Generation)'}
    serie = {'B': 'i (Injection)', 'C': 'i16 (16-valve Injection)', 'D': 'Turbo'}
    nadwozia = {'2': '2-door Sedan', '3': '3-door Combi Coupe', '4': '4-door Sedan', '5': '5-door Combi Coupe', '6': '4-door Sedan (Extended / CD)', '7': '2-door Convertible (CV)'}
    skrzynie = {'4': '4-speed manual', '5': '5-speed manual', '6': '3-speed automatic', '8': '4-speed automatic'}
    silniki = {
        'B': 'B234 (2.3L 16v - Naturally Aspirated)', 'D': 'B202 (2.0L 16v - Naturally Aspirated)', 'E': 'B212 (2.1L 16v - Naturally Aspirated)',
        'J': 'B201 (2.0L 8v - Naturally Aspirated)', 'L': 'B202 (2.0L 16v Turbo & Intercooler)', 'M': 'B234 (2.3L Turbo)',
        'N': 'B204 (2.0L 16v Turbo with balance shafts)', 'S': 'B201/B202 (Turbo 8v / LPT 16v)', 'V': '2.5L V6', "T": "B202R - 2.0 FPT, 204bhp",
    }
    roczniki = {'G': '1986', 'H': '1987', 'J': '1988', 'K': '1989', 'L': '1990', 'M': '1991', 'N': '1992', 'P': '1993', 'R': '1994', 'S': '1995', 'T': '1996'}
    fabryki = {'1': 'Trollhättan, Sweden (Line A)', '2': 'Trollhättan, Sweden (Line B)', '3': 'Arlöv, Sweden', '5': 'Malmö, Sweden', '6': 'Nystad, Finland', '7': 'Nystad, Finland', '8': 'Nystad, Finland (For 9000)', '9': 'Trollhättan, Sweden (Line C)'}

    return {
        "Manufacturer": "Sweden, Saab Automobile AB (YS3)",
        "Model": modele.get(vin[3], f"Unknown code ({vin[3]})"),
        "Series / Trim": serie.get(vin[4], "For Internal Manufacturer Use"),
        "Body Type": nadwozia.get(vin[5], f"Unknown code ({vin[5]})"),
        "Transmission": skrzynie.get(vin[6], f"Unknown code ({vin[6]})"),
        "Engine": silniki.get(vin[7], f"Unknown code ({vin[7]})"),
        "Model Year": roczniki.get(vin[9], f"Unknown code ({vin[9]})"),
        "Assembly Plant": fabryki.get(vin[10], f"Unknown code ({vin[10]})"),
        "Serial Number": vin[11:17]
    }

# --- 2. RANGE ROVER CLASSIC DECODER LOGIC ---
def dekoduj_vin_rrc(vin):
    vin = vin.strip().upper()
    if len(vin) != 17:
        return {"error": "Error: VIN must be exactly 17 characters long."}
    if not vin.startswith("SAL"):
        return {"error": f"Error: VIN {vin} does not look like a Land Rover. Expected 'SAL' prefix."}
    if vin[3:5] != "LH":
        return {"error": f"Error: Valid Land Rover VIN, but not a Range Rover Classic (expected 'LH' at positions 4-5). Found: {vin[3:5]}"}

    rozstawy_osi = {'A': '100 inches (Standard)', 'B': '108 inches (LWB - Long Wheel Base)', 'V': '100 inches (US/Canada Specification)', 'C': '108 inches LWB (US/Canada Specification)'}
    nadwozia = {'1': '4-door Station Wagon / 5-door', '2': '2-door / 3-door', '3': '4-door Station Wagon', 'M': '5-door'}
    silniki = {'1': '3.5L V8 (Injection / Catalyst)', '2': '3.9L V8', '3': '4.2L V8', 'E': '3.5L V8 (Carburettor, High Compression)', 'F': '2.5L Tdi (Diesel)', 'G': '2.4L VM (Turbo Diesel)'}
    roczniki = {'A': '1980', 'B': '1981', 'C': '1982', 'D': '1983', 'E': '1984', 'F': '1985', 'G': '1986', 'H': '1987', 'J': '1988', 'K': '1989', 'L': '1990', 'M': '1991', 'N': '1992', 'P': '1993', 'R': '1994', 'S': '1995', 'T': '1996', 'V': '1997'}
    fabryki = {'A': 'Solihull, United Kingdom', 'F': 'CKD Assembly (Completely Knocked Down)'}

    znak_9 = vin[8]
    if vin[5] in ['V', 'C'] and znak_9 in ['X', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        skrzynia = f"US/Canada Market Specification (VIN Check Digit: {znak_9})"
    else:
        skrzynie_kierownice = {'1': 'Right Hand Drive (RHD), Manual transmission', '2': 'Left Hand Drive (LHD), Manual transmission', '3': 'Right Hand Drive (RHD), Automatic transmission', '4': 'Left Hand Drive (LHD), Automatic transmission', '7': 'Right Hand Drive (RHD), 5-speed manual', '8': 'Left Hand Drive (LHD), 5-speed manual'}
        skrzynia = skrzynie_kierownice.get(znak_9, f"Unknown configuration code ({znak_9})")

    return {
        "Manufacturer": "United Kingdom, Land Rover (SAL)",
        "Model": "Range Rover Classic (LH)",
        "Wheelbase / Market": rozstawy_osi.get(vin[5], f"Unknown code ({vin[5]})"),
        "Body Type": nadwozia.get(vin[6], f"Unknown code ({vin[6]})"),
        "Engine": silniki.get(vin[7], f"Unknown code ({vin[7]})"),
        "Transmission / Steering": skrzynia,
        "Model Year": roczniki.get(vin[9], f"Unknown code ({vin[9]})"),
        "Assembly Plant": fabryki.get(vin[10], f"Unknown code ({vin[10]})"),
        "Serial Number": vin[11:17]
    }


# --- 3. UI ---

# Natywne Logo wczytywane bezpośrednio z plików aplikacji
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.image("ZK_01.png", use_container_width=True)

st.markdown("<h1>VIN Decoder</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Select vehicle brand and enter the 17-character VIN.</div>", unsafe_allow_html=True)

# Wybór Marki
car_type = st.radio("Vehicle Brand", ("Saab (1986+)", "Range Rover Classic"), horizontal=True, label_visibility="collapsed")

st.write("") 

# Pole na wpisanie VIN (z ramką dadce0 widoczną na jasnym tle)
vin_input = st.text_input("VIN Number", max_chars=17, placeholder="Enter VIN...", label_visibility="collapsed")

# Przycisk "Decode"
if st.button("Decode"):
    if not vin_input:
        st.markdown("<div class='clean-warning'>Please enter a VIN number first.</div>", unsafe_allow_html=True)
    else:
        # Dekodowanie
        if "Saab" in car_type:
            wynik = dekoduj_vin_saab(vin_input)
        else:
            wynik = dekoduj_vin_rrc(vin_input)
        
        st.write("---")
        
        # Wyświetlanie wyników
        if "error" in wynik:
            st.markdown(f"<div class='clean-error'>{wynik['error']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='clean-success'>VIN decoded successfully.</div>", unsafe_allow_html=True)
            
            # Tabela
            table_md = "| Attribute | Decoded Value |\n|---|---|\n"
            for k, v in wynik.items():
                table_md += f"| **{k}** | {v} |\n"
            
            st.markdown(table_md)

# Stopka
st.markdown("""
    <div class='footer-link'>
        Provided by <a href='http://zkclassics.com/' target='_blank'>ZK Classics</a>
    </div>
""", unsafe_allow_html=True)

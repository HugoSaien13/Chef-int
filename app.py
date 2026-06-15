import streamlit as st
import json
import os
import time
import requests
from recetas import BASE_DE_DATOS_RECETAS, INGREDIENTES_PLATAFORMA

# Configuración de página
st.set_page_config(page_title="Nevera.ai | Cocina Inteligente", page_icon="🔥", layout="wide")

# --- INYECCIÓN DE DISEÑO "MIDNIGHT PREMIUM" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&family=Plus+Jakarta+Sans:wght@500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp {
        background-color: #0B0E14 !important;
        background-image: radial-gradient(circle at 50% 0%, #1D2330 0%, #0B0E14 70%);
        font-family: 'Outfit', sans-serif !important;
        color: #E2E8F0 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    h1, h2, h3, h4, p, label, li {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    .material-symbols-rounded, .stIcon {
        font-family: 'Material Symbols Rounded' !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0B0E14 !important;
        border-right: 1px solid #1D2330 !important;
    }
    
    div[role="radiogroup"] > label {
        background: rgba(29, 35, 48, 0.5) !important;
        padding: 10px 15px !important;
        border-radius: 12px !important;
        border: 1px solid #2A3143 !important;
        margin-bottom: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #FF5722 !important;
        background: rgba(255, 87, 34, 0.08) !important;
        transform: translateX(4px) !important;
    }
    
    div[role="radiogroup"] label p, div[role="radiogroup"] label span {
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #131823 !important;
        border-radius: 16px;
        padding: 5px;
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.4) !important;
    }

    div[data-testid="stVerticalBlock"] > div[border="true"] {
        background: rgba(19, 24, 35, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #2A3143 !important;
        border-radius: 24px !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }

    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, #161B27 0%, #0F131D 100%) !important;
        border: 1px solid #2A3143 !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stExpander"]:hover {
        transform: translateY(-4px) !important;
        border-color: #FF5722 !important;
        box-shadow: 0 10px 25px rgba(255, 87, 34, 0.15) !important;
    }
    div[data-testid="stExpander"] summary {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    
    .stInfo {
        background: #1A2130 !important;
        border-left: 4px solid #00FFA3 !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
    }

    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #2A3143 0%, #1D2330 100%) !important;
        border: 1px solid #3B455D !important;
        border-radius: 10px !important;
        padding: 4px 12px !important;
    }
    span[data-baseweb="tag"] span {
        color: #00FFA3 !important;
        font-weight: 700 !important;
    }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 2rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 25px rgba(255, 87, 34, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(255, 87, 34, 0.6) !important;
        background: linear-gradient(135deg, #FF7043 0%, #FFB74D 100%) !important;
    }
    
    div[data-testid="stHorizontalBlock"] div.stButton > button:first-child {
        background: #1D2330 !important;
        border: 1px solid #3B455D !important;
        color: #94A3B8 !important;
        box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"] div.stButton > button:first-child:hover {
        background: #2A3143 !important;
        color: #FFFFFF !important;
        border-color: #00FFA3 !important;
    }

    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    .b-fuerza { background: rgba(0, 255, 163, 0.1); color: #00FFA3; border: 1px solid rgba(0, 255, 163, 0.3); }
    .b-def { background: rgba(0, 229, 255, 0.1); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3); }
    .b-cardio { background: rgba(255, 214, 0, 0.1); color: #FFD600; border: 1px solid rgba(255, 214, 0, 0.3); }
    .b-cheat { background: rgba(255, 64, 129, 0.1); color: #FF4081; border: 1px solid rgba(255, 64, 129, 0.3); }
    
    img { border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

ARCHIVO_DESPENSA = "despensa.json"
ARCHIVO_RECETAS_USUARIO = "mis_recetas_usuario.json"

# --- DICCIONARIO PARA LA API ---
TRADUCTOR_API = {
    "huevos": "eggs", "champiñones": "mushrooms", "pechuga de pavo": "turkey", 
    "avena": "oats", "leche": "milk", "platano": "banana", "pechuga de pollo": "chicken breast", 
    "cebolla": "onion", "base de pizza": "pizza crust", "nata ligera": "cream", 
    "bacon de pavo": "turkey bacon", "arroz": "rice", "pan integral": "wheat bread", 
    "atun en lata": "canned tuna", "aguacate": "avocado", "miel": "honey", 
    "espinacas": "spinach", "lomo de cerdo": "pork", "lentejas en bote": "lentils", 
    "garbanzos en bote": "chickpeas", "filete de merluza": "white fish", "pasta": "pasta", 
    "tortillas de trigo": "tortillas", "queso batido": "cream cheese", "queso rallado": "cheese", 
    "tomate": "tomato"
}

# --- LÓGICA DE ALMACENAMIENTO ---
def cargar_despensa_guardada():
    if os.path.exists(ARCHIVO_DESPENSA):
        with open(ARCHIVO_DESPENSA, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def guardar_despensa_en_disco(lista_ingredientes):
    with open(ARCHIVO_DESPENSA, "w", encoding="utf-8") as f:
        json.dump(lista_ingredientes, f, ensure_ascii=False, indent=4)

def cargar_recetas_usuario():
    if os.path.exists(ARCHIVO_RECETAS_USUARIO):
        with open(ARCHIVO_RECETAS_USUARIO, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def guardar_receta_usuario(nueva_receta):
    recetas_actuales = cargar_recetas_usuario()
    recetas_actuales.append(nueva_receta)
    with open(ARCHIVO_RECETAS_USUARIO, "w", encoding="utf-8") as f:
        json.dump(recetas_actuales, f, ensure_ascii=False, indent=4)

# --- CONEXIÓN A LA API ---
def buscar_recetas_en_internet(lista_ingredientes):
    # ⚠️ PEGA AQUÍ TU CLAVE REAL DE SPOONACULAR
    API_KEY = "TU_API_KEY_AQUI" 
    
    if API_KEY == "TU_API_KEY_AQUI":
        return {"error": "Falta la API Key. Regístrate en spoonacular.com/food-api y pon tu clave en el código."}
        
    # TRADUCIR Y LIMITAR: Solo cogemos los 3 primeros ingredientes para no bloquear la búsqueda
    ingredientes_ingles = [TRADUCTOR_API.get(ing, ing) for ing in lista_ingredientes[:3]]
    ingredientes_query = ",".join(ingredientes_ingles)
    
    url_servidor = f"https://api.spoonacular.com/recipes/complexSearch?includeIngredients={ingredientes_query}&addRecipeInformation=true&fillIngredients=true&number=4&apiKey={API_KEY}"
    
    try:
        respuesta = requests.get(url_servidor)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return datos.get("results", [])
        else:
            return {"error": f"Error del servidor: {respuesta.status_code}"}
    except Exception as e:
        return {"error": f"Error de conexión: {e}"}

recetas_totales = BASE_DE_DATOS_RECETAS.copy()
recetas_totales.extend(cargar_recetas_usuario())

if "mis_ingredientes" not in st.session_state:
    st.session_state["mis_ingredientes"] = cargar_despensa_guardada()

# --- HERO BANNER ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%); 
                padding: 40px 30px; 
                border-radius: 24px; 
                margin-bottom: 30px;
                box-shadow: 0 15px 35px rgba(255, 87, 34, 0.3);
                display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: white !important; font-size: 3.5rem; margin: 0; font-weight: 900; letter-spacing: -1px;">🔥 NEVERA.AI</h1>
            <p style="color: rgba(255,255,255,0.9) !important; font-size: 1.2rem; margin: 5px 0 0 0; font-weight: 500;">
                El primer asistente de cocina que exprime tu despensa al 100%.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.markdown("### 📊 RESUMEN DE TU APP")
col_s1, col_s2 = st.sidebar.columns(2)
col_s1.metric(label="RECETAS LOC.", value=len(recetas_totales))
col_s2.metric(label="EN NEVERA", value=len(st.session_state["mis_ingredientes"]))

st.sidebar.divider()

with st.sidebar.expander("🎯 OBJETIVO FITNESS", expanded=False):
    filtro_fitness = st.radio(
        "Selecciona tu enfoque:",
        ["✨ Mostrar todo", "💪 Alta en Proteína", "🔥 Definición", "⚡ Cardio", "🍪 Cheat Meal"],
        label_visibility="collapsed"
    )

filtro_limpio = filtro_fitness.split(" ", 1)[1] if " " in filtro_fitness else filtro_fitness
mapa_filtros = {
    "Mostrar todo": "Mostrar todo",
    "Alta en Proteína": "Alta en Proteína / Fuerza",
    "Definición": "Bajo en Carbohidratos / Definición",
    "Cardio": "Energía / Cardio",
    "Cheat Meal": "Permitido / Cheat Meal Sano"
}
filtro_interno = mapa_filtros.get(filtro_limpio, "Mostrar todo")

# --- 3 PESTAÑAS ---
pestaña_buscar, pestaña_nube, pestaña_añadir = st.tabs(["🔍 MOTOR LOCAL", "🌐 BÚSQUEDA MUNDIAL (API)", "➕ AÑADIR RECETA"])

with pestaña_buscar:
    st.write("")
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #00FFA3 !important;'>[ 01 ] TU INVENTARIO ACTUAL</h3>", unsafe_allow_html=True)
        st.write("Selecciona tus alimentos base para buscar en el sistema local:")
        
        ingredientes_usuario = st.multiselect(
            "Selecciona tus ingredientes:",
            INGREDIENTES_PLATAFORMA,
            default=st.session_state["mis_ingredientes"],
            label_visibility="collapsed"
        )
        
        st.write("")
        col_btn1, col_btn2, _ = st.columns([2.5, 3.5, 6])
        with col_btn1:
            if st.button("💾 GUARDAR ESTADO", use_container_width=True):
                st.session_state["mis_ingredientes"] = ingredientes_usuario
                guardar_despensa_en_disco(ingredientes_usuario)
                st.toast("Inventario sincronizado", icon="✅")
        with col_btn2:
            btn_buscar = st.button("⚡ GENERAR MENÚ LOCAL", type="primary", use_container_width=True)

    st.write("")

    if btn_buscar:
        with st.spinner("🔥 Procesando combinaciones algorítmicas locales..."):
            time.sleep(0.7)
        
        recetas_listas = []
        recetas_casi_listas = []
        ingredientes_tengo = set(ingredientes_usuario)
        
        for receta in recetas_totales:
            if filtro_interno != "Mostrar todo" and receta["categoria"] != filtro_interno:
                continue
            
            ingredientes_receta = set(receta["ingredientes"])
            ingredientes_faltantes = ingredientes_receta.difference(ingredientes_tengo)
            datos_resultado = {"receta": receta, "faltan": list(ingredientes_faltantes)}
            
            if len(ingredientes_faltantes) == 0:
                recetas_listas.append(datos_resultado)
            elif len(ingredientes_faltantes) <= 2:
                recetas_casi_listas.append(datos_resultado)
        
        col_izq, col_der = st.columns(2)
        with col_izq:
            st.markdown("### 🟢 LISTOS PARA COCINAR")
            if recetas_listas:
                for item in recetas_listas:
                    r = item["receta"]
                    badge_class = "b-fuerza" if "Fuerza" in r['categoria'] else "b-def" if "Definición" in r['categoria'] else "b-cardio" if "Cardio" in r['categoria'] else "b-cheat"
                    with st.expander(f"✨ {r['nombre']}"):
                        st.markdown(f"<span class='badge {badge_class}'>{r['categoria']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #94A3B8 !important;'><b>INGREDIENTES:</b> <span style='color: #F8FAFC !important;'>{', '.join(r['ingredientes'])}</span></p>", unsafe_allow_html=True)
                        st.info(r["instrucciones"])
            else:
                st.info("No tienes ingredientes suficientes en la base local.")

        with col_der:
            st.markdown("### 🟡 TE FALTA MUY POCO")
            if recetas_casi_listas:
                for item in recetas_casi_listas:
                    r = item["receta"]
                    badge_class = "b-fuerza" if "Fuerza" in r['categoria'] else "b-def" if "Definición" in r['categoria'] else "b-cardio" if "Cardio" in r['categoria'] else "b-cheat"
                    faltantes_texto = ", ".join(item["faltan"])
                    with st.expander(f"⚠️ {r['nombre']} (Faltan {len(item['faltan'])})"):
                        st.markdown(f"<span class='badge {badge_class}'>{r['categoria']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #94A3B8 !important;'><b>LLEVA:</b> <span style='color: #F8FAFC !important;'>{', '.join(r['ingredientes'])}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #FF5722 !important; font-weight: 700;'>🛒 COMPRAR: {faltantes_texto.upper()}</p>", unsafe_allow_html=True)
                        st.text(r["instrucciones"])

# --- PESTAÑA DE CONEXIÓN A INTERNET (API) ---
with pestaña_nube:
    st.write("")
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #00FFA3 !important;'>🌐 CONEXIÓN A BASE MUNDIAL (SPOONACULAR)</h3>", unsafe_allow_html=True)
        st.write("Tu inventario actual se enviará a un servidor externo para buscar recetas detalladas. (Se usarán los 3 ingredientes principales).")
        
        if st.button("🌍 BUSCAR EN INTERNET CON MI NEVERA ACTUAL", type="primary", use_container_width=True):
            if len(st.session_state["mis_ingredientes"]) == 0:
                st.warning("Guarda ingredientes en tu nevera primero en la pestaña 'MOTOR LOCAL'.")
            else:
                with st.spinner("Descargando instrucciones y fotografías..."):
                    resultados_api = buscar_recetas_en_internet(st.session_state["mis_ingredientes"])
                    
                if isinstance(resultados_api, dict) and "error" in resultados_api:
                    st.error(resultados_api["error"])
                elif len(resultados_api) == 0:
                    st.info("La API no ha encontrado recetas completas con esos ingredientes.")
                else:
                    st.success(f"¡Éxito! Se han descargado {len(resultados_api)} recetas de la nube.")
                    
                    for receta_api in resultados_api:
                        with st.container(border=True):
                            col_foto, col_datos = st.columns([1, 3])
                            with col_foto:
                                st.image(receta_api["image"], use_container_width=True)
                            with col_datos:
                                st.markdown(f"### {receta_api['title']}")
                                
                                usados = [ing["name"] for ing in receta_api.get("usedIngredients", [])]
                                faltan = [ing["name"] for ing in receta_api.get("missedIngredients", [])]
                                
                                st.markdown(f"<p style='color: #00FFA3 !important;'><b>✓ Ingredientes que tienes que usa:</b> {', '.join(usados)}</p>", unsafe_allow_html=True)
                                if faltan:
                                    st.markdown(f"<p style='color: #FF5722 !important;'><b>✗ Te faltaría comprar:</b> {', '.join(faltan)}</p>", unsafe_allow_html=True)
                                
                                instrucciones = receta_api.get("instructions")
                                if instrucciones:
                                    st.markdown("<p style='color:#F8FAFC !important; font-weight:bold; margin-top:15px;'>// PROTOCOLO DE PREPARACIÓN:</p>", unsafe_allow_html=True)
                                    st.markdown(f"<div style='background-color: #1A2130; padding: 15px; border-radius: 8px; border-left: 4px solid #00FFA3; color: #E2E8F0; font-family: \"JetBrains Mono\", monospace; font-size: 0.9rem;'>{instrucciones}</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown("<p style='color:#94A3B8; font-style:italic;'>El autor de esta receta no proporcionó pasos detallados.</p>", unsafe_allow_html=True)

with pestaña_añadir:
    st.write("")
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #00FFA3 !important;'>[ 02 ] COLABORAR CON LA RED</h3>", unsafe_allow_html=True)
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            nuevo_nombre = st.text_input("NOMBRE DEL PLATO:", placeholder="Ej: Bowl proteico de atún")
            nueva_categoria = st.selectbox(
                "OBJETIVO:",
                ["Alta en Proteína / Fuerza", "Bajo en Carbohidratos / Definición", "Energía / Cardio", "Permitido / Cheat Meal Sano"]
            )
        with col_form2:
            nuevos_ingredientes = st.multiselect(
                "INGREDIENTES QUE LLEVA:",
                INGREDIENTES_PLATAFORMA
            )
        
        nuevas_instrucciones = st.text_area("INSTRUCCIONES:", placeholder="Explica cómo se prepara...")
        
        if st.button("🚀 SUBIR AL SERVIDOR", type="primary"):
            if nuevo_nombre and nuevos_ingredientes and nuevas_instrucciones:
                receta_nueva_dict = {
                    "nombre": nuevo_nombre,
                    "ingredientes": nuevos_ingredientes,
                    "categoria": nueva_categoria,
                    "instrucciones": nuevas_instrucciones
                }
                guardar_receta_usuario(receta_nueva_dict)
                st.balloons()
                st.success("¡Receta procesada y guardada en la base de datos!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Rellena todos los campos para continuar.")
import streamlit as st
import json
import os
import time
import requests
from recetas import BASE_DE_DATOS_RECETAS, INGREDIENTES_PLATAFORMA

# Configuración de página
st.set_page_config(page_title="Nevera.ai | Cocina Inteligente", page_icon="🔥", layout="wide")

# --- INYECCIÓN DE DISEÑO PREMIUM ADAPTADO A MÓVILES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&family=Plus+Jakarta+Sans:wght@500;700&display=swap');

    /* Fondo oscuro inmersivo */
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

    /* BARRA LATERAL compacta */
    [data-testid="stSidebar"] {
        background-color: #0B0E14 !important;
        border-right: 1px solid #1D2330 !important;
    }
    
    /* FILTRO FITNESS */
    div[role="radiogroup"] > label {
        background: rgba(29, 35, 48, 0.5) !important;
        padding: 10px 15px !important;
        border-radius: 12px !important;
        border: 1px solid #2A3143 !important;
        margin-bottom: 8px !important;
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #131823 !important;
        border-radius: 16px;
        padding: 5px;
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%) !important;
        color: #FFFFFF !important;
    }

    /* Contenedor Principal */
    div[data-testid="stVerticalBlock"] > div[border="true"] {
        background: rgba(19, 24, 35, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #2A3143 !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* Tarjetas de Recetas unificadas (Ancho completo) */
    .receta-card {
        background: linear-gradient(145deg, #161B27 0%, #0F131D 100%) !important;
        border: 1px solid #2A3143 !important;
        border-radius: 16px !important;
        padding: 20px;
        margin-bottom: 20px;
    }
    .receta-card:hover {
        border-color: #FF5722 !important;
    }
    
    /* Bloque de instrucciones limpio */
    .instrucciones-box {
        background-color: #1A2130 !important;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #00FFA3;
        margin-top: 10px;
        font-size: 0.95rem;
    }

    /* BOTONES COMPLETOS PARA EL PULGAR */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 900 !important;
        width: 100% !important;
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.3) !important;
    }
    
    div[data-testid="stHorizontalBlock"] div.stButton > button:first-child {
        background: #1D2330 !important;
        border: 1px solid #3B455D !important;
        color: #94A3B8 !important;
        box-shadow: none !important;
    }

    /* Badges de categorías */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .b-fuerza { background: rgba(0, 255, 163, 0.1); color: #00FFA3; border: 1px solid rgba(0, 255, 163, 0.3); }
    .b-def { background: rgba(0, 229, 255, 0.1); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3); }
    .b-cardio { background: rgba(255, 214, 0, 0.1); color: #FFD600; border: 1px solid rgba(255, 214, 0, 0.3); }
    .b-cheat { background: rgba(255, 64, 129, 0.1); color: #FF4081; border: 1px solid rgba(255, 64, 129, 0.3); }

    /* MEDIA QUERY RESPONSIVA */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2rem !important; }
        .hero-subtitle { font-size: 1rem !important; }
        div[data-testid="stVerticalBlock"] > div[border="true"] { padding: 15px !important; }
        .stTabs [data-baseweb="tab"] { padding: 6px 10px !important; font-size: 0.8rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

ARCHIVO_DESPENSA = "despensa.json"
ARCHIVO_RECETAS_USUARIO = "mis_recetas_usuario.json"

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

def buscar_recetas_en_internet(lista_ingredientes):
    API_KEY = "ecab73f0fc0049828ba7f97537a20e77" 
    if API_KEY == "TU_API_KEY_AQUI":
        return {"error": "Falta la API Key."}
        
    ingredientes_ingles = [TRADUCTOR_API.get(ing.lower(), ing.lower()) for ing in lista_ingredientes[:3]]
    ingredientes_query = ",".join(ingredientes_ingles)
    
    url_servidor = f"https://api.spoonacular.com/recipes/complexSearch?includeIngredients={ingredientes_query}&addRecipeInformation=true&fillIngredients=true&number=4&apiKey={API_KEY}"
    try:
        respuesta = requests.get(url_servidor)
        if respuesta.status_code == 200:
            return respuesta.json().get("results", [])
        return {"error": f"Error del servidor: {respuesta.status_code}"}
    except Exception as e:
        return {"error": f"Error de conexión: {e}"}

recetas_totales = BASE_DE_DATOS_RECETAS.copy()
recetas_totales.extend(cargar_recetas_usuario())

if "mis_ingredientes" not in st.session_state:
    st.session_state["mis_ingredientes"] = cargar_despensa_guardada()

# --- HERO BANNER ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%); padding: 25px 20px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 12px 30px rgba(255, 87, 34, 0.25);">
        <h1 class="hero-title" style="color: white !important; font-size: 2.8rem; margin: 0; font-weight: 900; letter-spacing: -1px;">🔥 NEVERA.AI</h1>
        <p class="hero-subtitle" style="color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin: 5px 0 0 0; font-weight: 500;">
            El asistente que exprime tu despensa al 100%.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.markdown("### 📊 RESUMEN")
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

# --- PESTAÑAS ---
pestaña_buscar, pestaña_nube, pestaña_añadir = st.tabs(["🔍 MOTOR LOCAL", "🌐 BASE MUNDIAL", "➕ AÑADIR PLATO"])

with pestaña_buscar:
    st.write("")
    with st.container(border=True):
        st.markdown("<h4 style='margin-top: 0; color: #00FFA3 !important;'>[ 01 ] TU INVENTARIO ACTUAL</h4>", unsafe_allow_html=True)
        st.write("Escribe aquí abajo cualquier alimento nuevo que tengas:")
        
        # Entrada libre de texto con botón dedicado para inyectar alimentos
        col_input, col_add_btn = st.columns([8, 2])
        with col_input:
            nuevo_alimento_libre = st.text_input("Añadir alimento extra:", placeholder="Ej: hummus, rebozuelos, salsa sriracha...", label_visibility="collapsed")
        with col_add_btn:
            if st.button("➕", use_container_width=True):
                if nuevo_alimento_libre:
                    alimento_limpio = nuevo_alimento_libre.strip().lower()
                    if alimento_limpio not in st.session_state["mis_ingredientes"]:
                        st.session_state["mis_ingredientes"].append(alimento_limpio)
                        guardar_despensa_en_disco(st.session_state["mis_ingredientes"])
                        st.toast(f"¡{alimento_limpio} añadido!", icon="🧺")
                        st.rerun()

        st.write("---")
        st.write("Gestiona o elimina los alimentos guardados en tu stock:")

        opciones_dinamicas = list(set(INGREDIENTES_PLATAFORMA + st.session_state["mis_ingredientes"]))
        ingredientes_usuario = st.multiselect(
            "Tus alimentos activos:",
            options=opciones_dinamicas,
            default=st.session_state["mis_ingredientes"],
            label_visibility="collapsed"
        )
        
        st.write("")
        if st.button("💾 CONFIRMAR Y GUARDAR NEVERA"):
            st.session_state["mis_ingredientes"] = ingredientes_usuario
            guardar_despensa_en_disco(ingredientes_usuario)
            st.toast("Nevera sincronizada", icon="✅")
            st.rerun()
            
        btn_buscar = st.button("⚡ GENERAR MENÚ RESPONSIVO")

    st.write("")

    if btn_buscar:
        recetas_listas = []
        recetas_casi_listas = []
        ingredientes_tengo = set([i.lower() for i in ingredientes_usuario])
        
        for receta in recetas_totales:
            if filtro_interno != "Mostrar todo" and receta["categoria"] != filtro_interno:
                continue
            
            ingredientes_receta = set([i.lower() for i in receta["ingredientes"]])
            ingredientes_faltantes = ingredientes_receta.difference(ingredientes_tengo)
            
            if len(ingredientes_faltantes) == 0:
                recetas_listas.append(receta)
            elif len(ingredientes_faltantes) <= 2:
                recetas_casi_listas.append({"receta": receta, "faltan": list(ingredientes_faltantes)})
        
        st.markdown("### 🟢 LISTOS PARA COCINAR YA")
        if recetas_listas:
            for r in recetas_listas:
                badge_class = "b-fuerza" if "Fuerza" in r['categoria'] else "b-def" if "Definición" in r['categoria'] else "b-cardio" if "Cardio" in r['categoria'] else "b-cheat"
                st.markdown(f"""
                    <div class="receta-card">
                        <span class="badge {badge_class}">{r['categoria']}</span>
                        <h3 style="margin: 5px 0 12px 0; color:#FFFFFF;">✨ {r['nombre']}</h3>
                        <p style="color: #94A3B8; font-size:0.9rem; margin-bottom:10px;"><b>LLEVA:</b> {', '.join(r['ingredientes'])}</p>
                        <div class="instrucciones-box"><b>PASOS:</b> {r['instrucciones']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay recetas locales exactas con tus ingredientes.")

        st.markdown("### 🟡 TE FALTA MUY POCO (MÁX. 2 FALTANTES)")
        if recetas_casi_listas:
            for item in recetas_casi_listas:
                r = item["receta"]
                badge_class = "b-fuerza" if "Fuerza" in r['categoria'] else "b-def" if "Definición" in r['categoria'] else "b-cardio" if "Cardio" in r['categoria'] else "b-cheat"
                faltan_str = ", ".join(item['faltan']).upper()
                st.markdown(f"""
                    <div class="receta-card" style="border-left: 4px solid #FF5722;">
                        <span class="badge {badge_class}">{r['categoria']}</span>
                        <h3 style="margin: 5px 0 12px 0; color:#FFFFFF;">⚠️ {r['nombre']}</h3>
                        <p style="color: #94A3B8; font-size:0.9rem; margin-bottom:4px;"><b>LLEVA:</b> {', '.join(r['ingredientes'])}</p>
                        <p style="color: #FF5722; font-size:0.95rem; font-weight:700; margin-bottom:12px;">🛒 FALTA COMPRAR: {faltan_str}</p>
                        <div class="instrucciones-box" style="border-left-color:#FF5722;"><b>PASOS:</b> {r['instrucciones']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay platos locales cercanos.")

# --- PESTAÑA NUBE ---
with pestaña_nube:
    st.write("")
    with st.container(border=True):
        st.markdown("<h4 style='margin-top: 0; color: #00FFA3 !important;'>🌐 BÚSQUEDA MUNDIAL (API)</h4>", unsafe_allow_html=True)
        st.write("Se buscará en la red externa usando tus 3 primeros alimentos.")
        
        if st.button("🌍 LANZAR CONSULTA EN LA RED"):
            if len(st.session_state["mis_ingredientes"]) == 0:
                st.warning("Añade algún ingrediente primero.")
            else:
                with st.spinner("Conectando con servidores..."):
                    resultados_api = buscar_recetas_en_internet(st.session_state["mis_ingredientes"])
                    
                if isinstance(resultados_api, dict) and "error" in resultados_api:
                    st.error(resultados_api["error"])
                elif len(resultados_api) == 0:
                    st.info("No se encontraron platos en la API.")
                else:
                    for receta_api in resultados_api:
                        with st.container(border=True):
                            st.image(receta_api["image"], use_container_width=True)
                            st.markdown(f"### {receta_api['title']}")
                            
                            usados = [ing["name"] for ing in receta_api.get("usedIngredients", [])]
                            faltan = [ingimientos["name"] for ingimientos in receta_api.get("missedIngredients", [])]
                            
                            st.markdown(f"<p style='color: #00FFA3;'><b>✓ Tienes:</b> {', '.join(usados)}</p>", unsafe_allow_html=True)
                            if faltan:
                                st.markdown(f"<p style='color: #FF5722;'><b>✗ Falta comprar:</b> {', '.join(faltan)}</p>", unsafe_allow_html=True)
                            
                            instrucciones = receta_api.get("instructions")
                            if instrucciones:
                                st.markdown(f"<div class='instrucciones-box'>{instrucciones}</div>", unsafe_allow_html=True)

# --- PESTAÑA AÑADIR ---
with pestaña_añadir:
    st.write("")
    with st.container(border=True):
        st.markdown("<h4 style='margin-top: 0; color: #00FFA3 !important;'>[ 02 ] COLABORAR CON LA RED</h4>", unsafe_allow_html=True)
        
        nuevo_nombre = st.text_input("NOMBRE DEL PLATO:", placeholder="Ej: Wok de pollo express")
        nueva_categoria = st.selectbox(
            "OBJETIVO FITNESS:",
            ["Alta en Proteína / Fuerza", "Bajo en Carbohidratos / Definición", "Energía / Cardio", "Permitido / Cheat Meal Sano"]
        )
        
        opciones_crear = list(set(INGREDIENTES_PLATAFORMA + st.session_state["mis_ingredientes"]))
        nuevos_ingredientes = st.multiselect("INGREDIENTES QUE LLEVA:", options=opciones_crear)
        nuevas_instrucciones = st.text_area("INSTRUCCIONES DE PREPARACIÓN:")
        
        if st.button("🚀 SUBIR AL SERVIDOR LOCAL"):
            if nuevo_nombre and nuevos_ingredientes and nuevas_instrucciones:
                receta_nueva_dict = {
                    "nombre": nuevo_nombre,
                    "ingredientes": nuevos_ingredientes,
                    "categoria": nueva_categoria,
                    "instrucciones": nuevas_instrucciones
                }
                guardar_receta_usuario(receta_nueva_dict)
                st.balloons()
                st.success("¡Plato guardado!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Por favor, rellena todos los campos.")
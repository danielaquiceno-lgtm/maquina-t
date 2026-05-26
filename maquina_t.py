import streamlit as st

# ─── CONFIGURACIÓN DE PÁGINA ───────────────────────────────────────────────
st.set_page_config(
    page_title="Máquina de Puntuación - Letra T",
    page_icon="🎀",
    layout="wide"
)

# ─── ESTILOS FEMENINOS ─────────────────────────────────────────────────────
st.markdown("""
    <style>
        body { background-color: #fff0f5; }
        .stApp { background-color: #fff0f5; }
        h1, h2, h3 { color: #c2185b; }
        .stSlider > div > div > div { background: #f48fb1; }
        div[data-testid="metric-container"] {
            background-color: #fce4ec;
            border: 1px solid #f48fb1;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ─── DATOS ─────────────────────────────────────────────────────────────────
imagenes_T = [
    {"nombre": "T clásica",  "grid": [[1,1,1],[0,1,0],[0,1,0]]},
    {"nombre": "T ancha",    "grid": [[1,1,1],[0,1,0],[0,1,0]]},
    {"nombre": "T con base", "grid": [[1,1,1],[0,1,0],[0,1,0]]},
]

imagenes_noT = [
    {"nombre": "Cruz (+)",  "grid": [[0,1,0],[1,1,1],[0,1,0]]},
    {"nombre": "Diagonal",  "grid": [[1,0,0],[0,1,0],[0,0,1]]},
    {"nombre": "L",         "grid": [[1,0,0],[1,0,0],[1,1,1]]},
    {"nombre": "Cuadro",    "grid": [[1,1,1],[1,1,1],[1,1,1]]},
    {"nombre": "Esquinas",  "grid": [[1,0,1],[0,0,0],[1,0,1]]},
    {"nombre": "Vacío",     "grid": [[0,0,0],[0,0,0],[0,0,0]]},
]

# ─── FUNCIÓN DE PUNTUACIÓN ─────────────────────────────────────────────────
def calcular_puntaje(grid, pesos):
    total = 0
    pixeles = [px for fila in grid for px in fila]
    pesos_flat = [p for fila in pesos for p in fila]
    for i in range(9):
        total += pixeles[i] * pesos_flat[i]
    return total

# ─── FUNCIÓN PARA DIBUJAR GRID ─────────────────────────────────────────────
def mostrar_grid(grid, es_T=True):
    color = "#e91e63" if es_T else "#9e9e9e"
    html = "<div style='display:inline-block;'>"
    for fila in grid:
        html += "<div style='display:flex;'>"
        for px in fila:
            bg = color if px == 1 else "#fce4ec"
            html += f"<div style='width:28px;height:28px;background:{bg};margin:2px;border-radius:4px;border:1px solid #f48fb1;'></div>"
        html += "</div>"
    html += "</div>"
    return html

# ─── TÍTULO ────────────────────────────────────────────────────────────────
st.markdown("# 🎀 Máquina de Puntuación — Letra T")
st.markdown("**Autómatas, Gramática y Lenguaje** · Sistema interactivo de reconocimiento de patrones")
st.divider()

# ─── SECCIÓN 1: GALERÍA DE IMÁGENES ───────────────────────────────────────
st.markdown("## 🖼️ Galería de imágenes")

col_t, col_no = st.columns(2)

with col_t:
    st.markdown("### ✅ Imágenes que SÍ son T")
    cols = st.columns(3)
    for i, img in enumerate(imagenes_T):
        with cols[i % 3]:
            st.markdown(f"**{img['nombre']}**")
            st.markdown(mostrar_grid(img["grid"], es_T=True), unsafe_allow_html=True)

with col_no:
    st.markdown("### ❌ Imágenes que NO son T")
    cols = st.columns(3)
    for i, img in enumerate(imagenes_noT):
        with cols[i % 3]:
            st.markdown(f"**{img['nombre']}**")
            st.markdown(mostrar_grid(img["grid"], es_T=False), unsafe_allow_html=True)

st.divider()

# ─── SECCIÓN 2: SELECCIÓN DE IMAGEN ───────────────────────────────────────
st.markdown("## 🎯 Selecciona una imagen para evaluar")

todas = [(img["nombre"] + " ✅", img) for img in imagenes_T] + \
        [(img["nombre"] + " ❌", img) for img in imagenes_noT]

nombres = [t[0] for t in todas]
seleccion = st.selectbox("Elige una imagen:", nombres)
imagen_activa = dict(todas)[seleccion]

st.divider()

# ─── SECCIÓN 3: AJUSTE DE PESOS ───────────────────────────────────────────
st.markdown("## 🎛️ Paso 1: Ajusta los pesos de cada posición")
st.caption("Cada control deslizante controla el peso de un píxel en la cuadrícula 3x3. Muévelos para ver cómo cambia el puntaje.")

pesos = []
col1, col2, col3 = st.columns(3)

columnas = [col1, col2, col3]
etiquetas = ["Fila 1", "Fila 2", "Fila 3"]
valores_default = [
    [2.0, -1.0, -1.0],
    [2.0,  3.0,  3.0],
    [2.0, -1.0, -1.0],
]

for j, col in enumerate(columnas):
    with col:
        st.markdown(f"**{etiquetas[j]}**")
        fila_pesos = []
        for i in range(3):
            peso = st.slider(
                f"Pos ({i+1},{j+1})",
                min_value=-5.0,
                max_value=5.0,
                value=valores_default[i][j],
                step=0.5,
                key=f"peso_{i}_{j}"
            )
            fila_pesos.append(peso)
        pesos.append(fila_pesos)

st.markdown("")
umbral = st.slider(
    "🎀 Umbral (umbral): puntaje mínimo para considerar que ES una T",
    min_value=-10.0,
    max_value=20.0,
    value=5.0,
    step=0.5,
    key="umbral"
)

st.divider()

# ─── SECCIÓN 4: CÁLCULO PASO A PASO ───────────────────────────────────────
st.markdown("## 🧮 Cálculo paso a paso")

pixeles_flat = [px for fila in imagen_activa["grid"] for px in fila]
pesos_flat   = [p  for fila in pesos for p in fila]

terminos = " + ".join([f"({pixeles_flat[i]}×{pesos_flat[i]:.1f})" for i in range(9)])
puntaje  = calcular_puntaje(imagen_activa["grid"], pesos)

st.markdown(f"**Fórmula:** <span style='color:#2e7d32; font-family:monospace;'>y = {terminos}</span>", unsafe_allow_html=True)
st.markdown(f"**Puntaje total:** <span style='color:#2e7d32; font-size:1.1em;'>{puntaje:.2f}</span>", unsafe_allow_html=True)
st.markdown(f"**Umbral:** <span style='color:#2e7d32;'>{umbral}</span>", unsafe_allow_html=True)

if puntaje >= umbral:
    st.success(f"✅ Puntaje {puntaje:.2f} ≥ {umbral} → La máquina dice: **ES una T**")
else:
    st.error(f"❌ Puntaje {puntaje:.2f} < {umbral} → La máquina dice: **NO es una T**")

st.divider()

# ─── SECCIÓN 5: MARCADOR ──────────────────────────────────────────────────
st.markdown("## 🏆 Marcador: ¿Qué tan bien están calibrados tus pesos?")

t_correctas   = sum(1 for img in imagenes_T   if calcular_puntaje(img["grid"], pesos) >= umbral)
not_correctas = sum(1 for img in imagenes_noT if calcular_puntaje(img["grid"], pesos) <  umbral)
total_correctas = t_correctas + not_correctas
total = len(imagenes_T) + len(imagenes_noT)

c1, c2, c3 = st.columns(3)
c1.metric("✅ T reconocidas correctamente",   f"{t_correctas} / {len(imagenes_T)}")
c2.metric("❌ No-T rechazadas correctamente", f"{not_correctas} / {len(imagenes_noT)}")
c3.metric("🎀 Precisión total",               f"{total_correctas} / {total}")

if total_correctas == total:
    st.success("🏆 ¡Perfecto! Tus pesos clasifican correctamente todas las imágenes.")
elif total_correctas >= total * 0.75:
    st.warning("🌸 ¡Casi! Ajusta un poco más los pesos para mejorar la precisión.")
else:
    st.error("💪 Sigue intentando, mueve los pesos y observa cómo cambian los resultados.")


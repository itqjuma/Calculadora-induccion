import math
import streamlit as st

# Configuración inicial de la página
st.set_page_config(page_title="Calculadora de Inducción - Luzars", layout="centered")

st.title("🔥 Calculadora de Potencia para Inducción")
st.write("Selecciona el material y define los parámetros geométricos y térmicos:")

# Base de datos de materiales: [Densidad (g/cm3), Calor Específico (J/g°C), Eficiencia base]
materiales = {
    'Acero (Ferroso)': [7.85, 0.62, 0.506],
    'Cobre (No Ferroso)': [8.96, 0.385, 0.212],
    'Aluminio (No Ferroso)': [2.70, 1.02, 0.212]
}

# --- ENTRADAS DE LA APLICACIÓN (Sidebar o Panel Principal) ---
material = st.selectbox("Material de la pieza:", list(materiales.keys()))

# Extraemos los valores por defecto según el material seleccionado
rho_default, cp_default, ef_default = materiales[material]

col1, col2 = st.columns(2)

with col1:
    diametro_cm = st.number_input("Diámetro (cm):", value=2.54, step=0.1)
    longitud_cm = st.number_input("Longitud (cm):", value=10.0, step=0.5)
    temp_inicial = st.number_input("Temperatura Inicial (°C):", value=20, step=1)

with col2:
    temp_final = st.number_input("Temperatura Final (°C):", value=1100, step=10)
    tiempo_seg = st.number_input("Tiempo de calentamiento (s):", value=15.0, step=1.0)
    eficiencia = st.number_input("Eficiencia del sistema:", value=ef_default, step=0.01, format="%.3f")

# --- LÓGICA DE CÁLCULO ---
rho, cp, _ = materiales[material]

radio = diametro_cm / 2.0
volumen_cm3 = math.pi * (radio**2) * longitud_cm
masa_g = volumen_cm3 * rho
masa_kg = masa_g / 1000.0

delta_t = temp_final - temp_inicial
q_ideal_joules = masa_g * cp * delta_t

p_ideal_kw = (q_ideal_joules / tiempo_seg) / 1000.0

if eficiencia <= 0:
    eficiencia = 0.01

prn_kw = p_ideal_kw / eficiencia
capex_kw = prn_kw * 1.20  # CapEx con 20% de margen

# --- RESULTADOS ---
st.markdown("---")
st.subheader("📊 Resultados del Cálculo")

st.info(f"**Masa de la pieza:** {masa_kg:.3f} kg ({masa_g:.1f} g)")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="Energía Ideal", value=f"{q_ideal_joules:,.2f} J")
    st.metric(label="Potencia Ideal Neta", value=f"{p_ideal_kw:.2f} kW")

with col_res2:
    st.metric(label="Potencia Real Necesaria (PRN)", value=f"{prn_kw:.2f} kW")
    st.metric(label="Equipo Recomendado (CapEx +20%)", value=f"{capex_kw:.2f} kW")
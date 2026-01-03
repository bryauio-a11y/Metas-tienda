import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Control de Metas - Tienda", page_icon="👕")

# --- CONSTANTES ---
META_TOTAL = 5525.00
DIAS_TOTALES = 13
ARCHIVO_DATOS = "ventas_data.json"

# --- FUNCIONES DE DATOS ---
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r') as f:
            return json.load(f)
    return []

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w') as f:
        json.dump(datos, f, indent=4)

# --- LÓGICA DE NEGOCIO ---
ventas = cargar_datos()
total_vendido = sum(d['monto'] for d in ventas)
dias_transcurridos = len(ventas)
dias_restantes = DIAS_TOTALES - dias_transcurridos
falta_para_meta = round(META_TOTAL - total_vendido, 2)

# --- DISEÑO DE LA INTERFAZ ---
st.title("🚀 Panel de Metas Diarias")
st.subheader("Tienda de Ropa Americana")

# --- BLOQUE DE MÉTRICAS VISUALES ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Vendido", f"${total_vendido:,.2f}")
with col2:
    st.metric("Falta para Meta", f"${max(0, falta_para_meta):,.2f}")
with col3:
    if dias_restantes > 0:
        nueva_meta = round(falta_para_meta / dias_restantes, 2)
        st.metric("Nueva Meta Diaria", f"${max(0, nueva_meta):,.2f}", delta_color="inverse")
    else:
        st.write("Periodo finalizado")

# --- BARRA DE PROGRESO VISUAL ---
progreso = min(total_vendido / META_TOTAL, 1.0)
st.write(f"**Progreso hacia el objetivo de ${META_TOTAL:,.2f}:**")
st.progress(progreso)

# --- FORMULARIO PARA REGISTRAR VENTA ---
with st.sidebar:
    st.header("Registrar Venta")
    fecha_input = st.text_input("Fecha (ej. 31/12/25)", datetime.now().strftime("%d/%m/%y"))
    monto_input = st.number_input("Monto vendido hoy ($)", min_value=0.0, step=0.01, format="%.2f")
    
    if st.button("Guardar Venta"):
        if dias_transcurridos < DIAS_TOTALES:
            ventas.append({"fecha": fecha_input, "monto": round(monto_input, 2)})
            guardar_datos(ventas)
            st.success("¡Venta registrada!")
            st.rerun()
        else:
            st.error("Ya se completaron los 13 días.")

    if st.button("Reiniciar Todo"):
        if os.path.exists(ARCHIVO_DATOS):
            os.remove(ARCHIVO_DATOS)
            st.rerun()

# --- GRÁFICA DE VENTAS ---
if ventas:
    st.divider()
    st.subheader("📈 Evolución de Ventas")
    df = pd.DataFrame(ventas)
    st.line_chart(df.set_index('fecha')['monto'])
    
    st.subheader("📋 Historial de Días")
    st.table(df)
else:
    st.info("Aún no hay ventas registradas. Usa el panel lateral para empezar.")
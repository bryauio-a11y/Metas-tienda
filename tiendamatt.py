import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Meta Tienda 2 - $4,550", page_icon="🛍️", layout="wide")

# --- PARÁMETROS FIJOS ---
META_TOTAL = 4550.00  # <--- META ACTUALIZADA: $4,550
DIAS_TOTALES = 13
ARCHIVO_DATOS = "ventas_tienda_2.json" 

# --- FUNCIONES DE DATOS ---
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r') as f:
            return json.load(f)
    return []

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w') as f:
        json.dump(datos, f, indent=4)

# --- LÓGICA DE CÁLCULOS ---
ventas = cargar_datos()
total_vendido = sum(d['monto'] for d in ventas)
dias_transcurridos = len(ventas)
dias_restantes = DIAS_TOTALES - dias_transcurridos
falta_para_meta = round(META_TOTAL - total_vendido, 2)

# --- DISEÑO DE LA INTERFAZ WEB ---
st.title("🛍️ Control de Ventas: TIENDA 2")
st.markdown(f"**Objetivo Total: ${META_TOTAL:,.2f}** | **Meta Diaria Inicial: $350.00**")

# --- BLOQUE DE MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Acumulado", f"${total_vendido:,.2f}")

with col2:
    st.metric("Restante", f"${max(0, falta_para_meta):,.2f}")

with col3:
    if dias_restantes > 0:
        # Aquí se calcula cuánto deben vender cada día de los que quedan
        meta_ajustada = round(falta_para_meta / dias_restantes, 2)
        st.metric("Meta Hoy (Ajustada)", f"${max(0, meta_ajustada):,.2f}")
    else:
        st.metric("Días", "Finalizado")

with col4:
    if ventas:
        mejor_dia = max(ventas, key=lambda x: x['monto'])
        st.metric("🏆 Récord", f"${mejor_dia['monto']:,.2f}")
    else:
        st.metric("🏆 Récord", "$0.00")

# --- BARRA DE PROGRESO ---
progreso = min(total_vendido / META_TOTAL, 1.0)
st.write(f"**Progreso: {progreso*100:.1f}%**")
st.progress(progreso)

# --- GRÁFICA Y REGISTRO ---
st.divider()
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 Rendimiento Diario")
    if ventas:
        df = pd.DataFrame(ventas)
        st.area_chart(df.set_index('fecha')['monto'], color="#29b5e8")
    else:
        st.info("Registra tu primera venta para ver la gráfica.")

with c2:
    st.subheader("⚙️ Registrar Venta")
    fecha = st.text_input("Fecha", datetime.now().strftime("%d/%m/%y"))
    monto = st.number_input("Monto de hoy ($)", min_value=0.0, format="%.2f")
    
    if st.button("Guardar Registro"):
        if dias_transcurridos < DIAS_TOTALES:
            ventas.append({"fecha": fecha, "monto": round(monto, 2)})
            guardar_datos(ventas)
            st.success("¡Venta guardada!")
            st.rerun()
        else:
            st.warning("Se han completado los 13 días.")

    if st.button("Reiniciar Tienda 2"):
        if os.path.exists(ARCHIVO_DATOS):
            os.remove(ARCHIVO_DATOS)
            st.rerun()
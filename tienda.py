import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Control de Ventas Cloud", layout="wide")

# URL de tu Google Sheet (Copia y pega la dirección de tu navegador aquí)
# Ejemplo: "https://docs.google.com/spreadsheets/d/tu-id-aqui/edit"
URL_HOJA = "TU_URL_DE_GOOGLE_SHEETS_AQUI"

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar datos
df = conn.read(spreadsheet=URL_HOJA)

st.title("📈 Control de Ventas Indestructible")

# Formulario
with st.sidebar:
    st.header("Nueva Venta")
    f = st.date_input("Fecha", datetime.now())
    m = st.number_input("Monto ($)", min_value=0.0)
    if st.button("Registrar en la Nube"):
        # Crear nueva fila y limpiar datos vacíos
        nueva_fila = pd.DataFrame([{"fecha": str(f), "monto": m, "tienda": "Tienda 1"}])
        df_final = pd.concat([df, nueva_fila], ignore_index=True).dropna(how='all')
        
        # Enviar a Google
        conn.update(spreadsheet=URL_HOJA, data=df_final)
        st.success("¡Venta guardada en Google Sheets!")
        st.rerun()

# Métricas
total = df['monto'].sum() if not df.empty else 0.0
st.metric("Total Acumulado", f"${total:,.2f}")
st.dataframe(df, use_container_width=True)

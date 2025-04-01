import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuración de la página (Título y Favicon)
st.set_page_config(page_title="Análisis de Sentimientos", page_icon="🧠", layout="wide")

# URL de la API
API_URL = "https://sentimentanalizer-production.up.railway.app/"

# Título del Proyecto
st.markdown("<h1 style='text-align: center;'>🔍 Análisis de Sentimientos con IA</h1>", unsafe_allow_html=True)

# Variables de sesión
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "texto_usuario" not in st.session_state:
    st.session_state.texto_usuario = ""

# Si el usuario ha iniciado sesión
if st.session_state.usuario:
    st.subheader(f"Bienvenido, {st.session_state.usuario} 👋")
    
    # Input para escribir texto
    st.session_state.texto_usuario = st.text_area("✍️ Escribe tu texto:", 
                                                  value=st.session_state.texto_usuario, 
                                                  height=150, 
                                                  placeholder="Escribe algo para analizar...")

    # Botón de análisis de sentimiento
    if st.button("🔍 Analizar Sentimiento"):
        if st.session_state.texto_usuario:
            try:
                response = requests.post(f"{API_URL}/analizar/", 
                                         json={"username": st.session_state.usuario, "texto": st.session_state.texto_usuario})
                response.raise_for_status()  # Capturar errores HTTP
                
                resultado = response.json()
                st.success("✅ Análisis completado")
                st.write(f"**Sentimiento:** {resultado['sentimiento']}")
                st.write(f"**Confianza:** {float(resultado['confianza']):.2f} 🔥")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error al conectar con la API: {e}")
        else:
            st.warning("⚠️ Por favor, ingresa un texto para analizar.")
    
    # Mostrar historial de análisis
    st.subheader("📊 Historial de Análisis")
    try:
        historial_response = requests.get(f"{API_URL}/historial/{st.session_state.usuario}")
        historial_response.raise_for_status()
        datos = historial_response.json()
        if datos:
            df = pd.DataFrame(datos)
            df["fecha"] = pd.to_datetime(df["fecha"])  # Convertir fecha a formato datetime

            st.dataframe(df[["fecha", "texto", "sentimiento"]].sort_values(by="fecha", ascending=False))

            # Gráfica de evolución de la confianza
            fig = px.line(df, x="fecha", y="confianza", title="Evolución de la Confianza en el Sentimiento", markers=True)
            st.plotly_chart(fig)
        else:
            st.info("📌 Aún no has realizado análisis.")
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ No se pudo cargar el historial: {e}")
    
    # Cerrar sesión
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.usuario = None
        st.session_state.texto_usuario = ""
        st.rerun()

# Si no ha iniciado sesión, mostrar opciones de inicio/registro
else:
    opcion = st.radio("📌 ¿Qué deseas hacer?", ["Iniciar Sesión", "Registrarse"], index=0)
    
    if opcion == "Iniciar Sesión":
        st.subheader("🔐 Iniciar Sesión")
        login_username = st.text_input("👤 Nombre de usuario")
        login_password = st.text_input("🔑 Contraseña", type="password")
        
        if st.button("🚀 Iniciar Sesión"):
            if login_username and login_password:
                try:
                    response = requests.post(f"{API_URL}/login/", 
                                             json={"username": login_username, "password": login_password})
                    response.raise_for_status()
                    
                    st.success("✅ Inicio de sesión exitoso.")
                    st.session_state.usuario = login_username
                    st.session_state.texto_usuario = ""
                    st.rerun()
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Usuario o contraseña incorrectos: {e}")
            else:
                st.warning("⚠️ Por favor, completa todos los campos.")
    
    elif opcion == "Registrarse":
        st.subheader("📌 Crear una nueva cuenta")
        register_username = st.text_input("👤 Nombre de usuario")
        register_password = st.text_input("🔑 Contraseña", type="password")
        
        if st.button("✅ Registrarse"):
            if register_username and register_password:
                try:
                    response = requests.post(f"{API_URL}/register/", 
                                             json={"username": register_username, "password": register_password})
                    response.raise_for_status()
                    
                    st.success("🎉 Usuario registrado correctamente. Ahora puedes iniciar sesión.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ No se pudo registrar el usuario: {e}")
            else:
                st.warning("⚠️ Por favor, completa todos los campos.")

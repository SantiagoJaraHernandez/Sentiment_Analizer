import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 🔹 Configuración de la página (Título y Favicon)
st.set_page_config(page_title="Análisis de Sentimientos", page_icon="🧠", layout="wide")

# 🎨 Estilos personalizados (ahora responsive)
st.markdown("""
    <style>
        /* Fondo y estilos generales */
        body {
            background-color: #121212;
            color: white;
        }

        /* Ajustar tamaño en móviles */
        @media screen and (max-width: 600px) {
            .stTextInput input, .stTextArea textarea {
                font-size: 16px !important;
                padding: 10px;
            }
            .stButton>button {
                font-size: 18px !important;
            }
        }

        /* Botones más grandes y centrados */
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }

        /* Inputs oscuros */
        .stTextInput input, .stTextArea textarea {
            background-color: #222;
            color: white;
            border-radius: 5px;
        }

        /* Titulos y etiquetas en color blanco */
        .stTextInput label, .stTextArea label, .stRadio label, .stPassword label {
            color: #fff;
            font-weight: bold;
        }

        /* Ajustar tablas en pantallas pequeñas */
        .dataframe {
            width: 100% !important;
            overflow-x: auto;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# 🌍 URL de la API
API_URL = "sentimentanalizer-production.up.railway.app"

# 🔹 Título del Proyecto
st.markdown("<h1 style='text-align: center;'>🔍 Análisis de Sentimientos en textos con IA</h1>", unsafe_allow_html=True)

# 📌 Variables de sesión
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "texto_usuario" not in st.session_state:
    st.session_state.texto_usuario = ""

# 🟢 Si el usuario ha iniciado sesión
if st.session_state.usuario:
    st.subheader(f"Bienvenido, {st.session_state.usuario} 👋")

    # 📝 Input para escribir texto
    st.session_state.texto_usuario = st.text_area("✍️ Escribe tu texto aquí:", 
                                                  value=st.session_state.texto_usuario, 
                                                  height=150, 
                                                  placeholder="Escribe algo para analizar...")

    # 🔍 Botón de análisis de sentimiento
    if st.button("🔍 Analizar Sentimiento"):
        if st.session_state.texto_usuario:
            response = requests.post(f"{API_URL}/analizar/", 
                                     json={"username": st.session_state.usuario, "texto": st.session_state.texto_usuario})

            if response.status_code == 200:
                resultado = response.json()
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.success("✅ Análisis completado")
                    st.write(f"**Sentimiento:** {resultado['sentimiento']}")
                    st.write(f"**Confianza:** {float(resultado['confianza']):.2f} 🔥")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("⚠️ Error al conectar con la API.")
        else:
            st.warning("⚠️ Por favor, ingresa un texto para analizar.")

    # 📊 Mostrar historial de análisis
    st.subheader("📊 Historial de Análisis")

    historial_response = requests.get(f"{API_URL}/historial/{st.session_state.usuario}")
    if historial_response.status_code == 200:
        datos = historial_response.json()

        if datos:
            df = pd.DataFrame(datos)
            df["fecha"] = pd.to_datetime(df["fecha"])  # Convertir fecha a formato datetime

            # 🟢 Tabla de historial con tarjeta
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.dataframe(df[["fecha", "texto", "sentimiento"]].sort_values(by="fecha", ascending=False))
                st.markdown("</div>", unsafe_allow_html=True)

            # 📈 Gráfica de evolución del sentimiento
            fig = px.line(df, x="fecha", y="sentimiento", title="Evolución del Sentimiento", markers=True)
            fig.update_layout(yaxis=dict(tickmode="array", tickvals=[1, 2, 3, 4, 5], 
                                         ticktext=["Muy Negativo", "Negativo", "Neutral", "Positivo", "Muy Positivo"]))
            st.plotly_chart(fig)
        else:
            st.info("📌 Aún no has realizado análisis.")
    else:
        st.error("⚠️ No se pudo cargar el historial.")

    # 🔴 Cerrar sesión con botón estilizado
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.usuario = None
        st.session_state.texto_usuario = ""  # Limpiar el texto al cerrar sesión
        st.rerun()

# 🔹 Si no ha iniciado sesión, mostrar opciones de inicio/registro
else:
    opcion = st.radio("📌 ¿Qué deseas hacer?", ["Iniciar Sesión", "Registrarse"], index=0)

    if opcion == "Iniciar Sesión":
        st.subheader("🔐 Iniciar Sesión")
        login_username = st.text_input("👤 Nombre de usuario")
        login_password = st.text_input("🔑 Contraseña", type="password")

        if st.button("🚀 Iniciar Sesión"):
            if login_username and login_password:
                response = requests.post(f"{API_URL}/login/", json={"username": login_username, "password": login_password})

                if response.status_code == 200:
                    st.success("✅ Inicio de sesión exitoso.")
                    st.session_state.usuario = login_username  # Guarda el usuario en la sesión
                    st.session_state.texto_usuario = ""  # Limpiar cualquier texto previo
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos.")
            else:
                st.warning("⚠️ Por favor, completa todos los campos.")
    
    elif opcion == "Registrarse":
        st.subheader("📌 Crear una nueva cuenta")
        register_username = st.text_input("👤 Nombre de usuario")
        register_password = st.text_input("🔑 Contraseña", type="password")

        if st.button("✅ Registrarse"):
            if register_username and register_password:
                response = requests.post(f"{API_URL}/register/", json={"username": register_username, "password": register_password})

                if response.status_code == 200:
                    st.success("🎉 Usuario registrado correctamente. Ahora puedes iniciar sesión.")
                else:
                    st.error("❌ No se pudo registrar el usuario.")
            else:
                st.warning("⚠️ Por favor, completa todos los campos.")

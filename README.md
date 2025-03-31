
# **FeelingsAI 🎭 - Análisis de Sentimientos con IA**  

[![Streamlit](https://img.shields.io/badge/Deployed-Streamlit-blue?style=flat&logo=streamlit)](https://feelingsai.streamlit.app/)  

📌 **FeelingsAI** es una aplicación web que utiliza inteligencia artificial para analizar el sentimiento de textos ingresados por los usuarios.  

🔗 **Accede a la app aquí:**  
👉 [https://feelingsai.streamlit.app/](https://feelingsai.streamlit.app/)  

---

## 🚀 **Características**  

✅ Análisis de sentimientos (positivo, negativo, neutro).  
✅ Interfaz intuitiva con **Streamlit**.  
✅ Uso de modelos **Transformers** para el procesamiento de lenguaje natural.  
✅ Visualización de datos con **Matplotlib** y **Plotly**.  
✅ API backend con **FastAPI**.  

---

## 🛠️ **Tecnologías Utilizadas**  

- **Python 3.12**  
- **Streamlit** (Interfaz web)  
- **FastAPI** (Backend)  
- **Uvicorn** (Servidor ASGI)  
- **Transformers** (Modelo de análisis de sentimientos)  
- **Matplotlib y Plotly** (Visualización de datos)  
- **Requests y Pandas** (Procesamiento de datos)  

---

## 📦 **Instalación y Uso Local**  

### **1️⃣ Clona el repositorio**  
```bash
git clone https://github.com/tu-usuario/FeelingsAI.git
cd FeelingsAI
```

### **2️⃣ Crea un entorno virtual e instala dependencias**  
```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt
```

### **3️⃣ Ejecuta la API (FastAPI)**  
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### **4️⃣ Ejecuta la app en Streamlit**  
```bash
streamlit run app.py
```

🔹 **La aplicación estará disponible en:** `http://localhost:8501`  

---

## 🔄 **Despliegue en Railway**  

Para desplegar en Railway:  
1️⃣ Crea un nuevo proyecto en **[Railway](https://railway.app/)**  
2️⃣ Sube el código y define las variables necesarias  
3️⃣ Usa el comando de inicio adecuado en `Railway`:
```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```
4️⃣ 🚀 ¡Tu app estará en producción!  

---

## 📜 **Licencia**  
MIT License.  

💡 **¡Contribuciones y sugerencias son bienvenidas!** 🚀  

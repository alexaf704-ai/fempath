# 🚀 FemPath — Deploy en 10 minutos (Streamlit Cloud)

## Lo que necesitas
- Cuenta en GitHub (gratis)
- Cuenta en Streamlit Cloud (gratis)
- API Key de Google Gemini (100% gratis, solo necesitas cuenta de Google)

---

## PASO 1 — Obtén tu API Key de Gemini (2 min) — ES GRATIS

1. Ve a **aistudio.google.com**
2. Inicia sesión con tu cuenta de Google (la que ya tienes)
3. Clic en **Get API Key** → **Create API key**
4. Copia la key (empieza con `AIza...`)
5. Guárdala — la necesitas en el Paso 3

> ✅ Sin tarjeta de crédito. Sin límite de tiempo. Gemini 1.5 Flash es gratis.

---

## PASO 2 — Sube los archivos a GitHub (3 min)

1. Ve a **github.com** → **New repository**
2. Nombre: `fempath` → **Create repository**
3. Sube estos 3 archivos (arrastra y suelta):
   - `fempath_app.py`
   - `requirements.txt`
   - (opcional) `fempath.html`
4. **Commit changes**

---

## PASO 3 — Deploy en Streamlit Cloud (5 min)

1. Ve a **share.streamlit.io**
2. Inicia sesión con tu cuenta de GitHub
3. Clic en **New app**
4. Selecciona:
   - **Repository:** `tu-usuario/fempath`
   - **Branch:** `main`
   - **Main file path:** `fempath_app.py`
5. Clic en **Advanced settings** → **Secrets**
6. Agrega esto (reemplaza con tu key real):

```toml
GEMINI_API_KEY = "AIzaTU_KEY_AQUI"
```

7. Clic en **Deploy!**

---

## RESULTADO

En 2-3 minutos tendrás tu URL pública:
```
https://tu-usuario-fempath-fempath-app-XXXXX.streamlit.app
```

✅ Esta es tu **functional link** para entregar en el challenge.

---

## Para el video (evidencia de AI)

Muestra en pantalla:
1. El formulario de FemPath con tus respuestas
2. El spinner "Claude AI está analizando tu perfil…"
3. El resultado generado en tiempo real por Claude
4. Las 3 acciones concretas personalizadas

Esto demuestra AI real integrada, no simulada.

---

## Herramientas de AI usadas en el proyecto

| Herramienta | Para qué |
|-------------|----------|
| **Gemini AI (Google)** | Genera roadmaps personalizados en tiempo real |
| **ChatGPT** | Diseño UX y testeo de usuarios simulados |
| **Gamma** | Deck visual del proyecto |
| **Streamlit** | Deploy de la app web |
| **Claude (este chat)** | Arquitectura, código y estrategia |

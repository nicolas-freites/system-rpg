# ============================================================
# app.py — Archivo principal de la aplicación
# Acá se construye toda la interfaz visual que ve el usuario.
# Streamlit lee este archivo y genera la página web automáticamente.
# ============================================================

import streamlit as st          # Librería que convierte código Python en una app web.
from datetime import datetime   # Para trabajar con fechas y horas.
import pytz                     # Para manejar zonas horarias de distintos países.
import plotly.graph_objects as go  # Para crear gráficos interactivos.

# Importamos funciones propias del archivo data.py.
# En vez de escribir toda la lógica acá, la separamos en otro archivo para mantener orden.
from data import cargar_jugador, guardar_jugador, verificar_nuevo_dia, guardar_historial, PAISES_TIMEZONES

# ── Configuración general de la página ──
# Esto define el título que aparece en la pestaña del navegador y el ícono.
st.set_page_config(
    page_title="SISTEMA",
    page_icon="⚔️",
    layout="centered"   # Centra el contenido en la pantalla
)

# ── Estilos visuales (CSS) ──
# Streamlit permite inyectar CSS para personalizar el aspecto visual.
# unsafe_allow_html=True le dice a Streamlit que confíe en nuestro HTML/CSS
st.markdown("""
    <style>
        /* Caja azul de notificaciones (pantallas de bienvenida) */
        .notification-box {
            border: 2px solid #00aaff;
            border-radius: 10px;
            padding: 30px;
            background-color: #000820;
            box-shadow: 0 0 20px #00aaff;
            text-align: center;
        }
        /* Título dentro de la caja de notificación */
        .notif-title {
            color: #00aaff;
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 4px;
        }
        /* Texto dentro de la caja de notificación */
        .notif-text {
            color: #ffffff;
            font-size: 18px;
            margin-top: 15px;
            line-height: 2;
        }
        /* Caja roja de penalizaciones */
        .penalty-box {
            border: 2px solid #ff2200;
            border-radius: 10px;
            padding: 20px;
            background-color: #1a0000;
            box-shadow: 0 0 20px #ff2200;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Título de la caja de penalización */
        .penalty-title {
            color: #ff2200;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 4px;
        }
        /* Texto de la caja de penalización */
        .penalty-text {
            color: #ff6666;
            font-size: 16px;
            margin-top: 10px;
            line-height: 2;
        }
        /* Caja individual de estadísticas (Rango, Nivel, XP, Días) */
        .stat-box {
            border: 1px solid #00aaff;
            border-radius: 8px;
            padding: 15px;
            background-color: #000820;
            text-align: center;
            box-shadow: 0 0 10px #00aaff55;
            height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        /* Etiqueta de la estadística (ej: "NIVEL") */
        .stat-label {
            color: #00aaff;
            font-size: 13px;
            letter-spacing: 2px;
        }
        /* Valor de la estadística (ej: "5") */
        .stat-value {
            color: #ffffff;
            font-size: 26px;
            font-weight: bold;
        }
        /* Estilo de todos los botones de la app */
        .stButton > button {
            background-color: #000820;
            color: #00aaff;
            border: 1px solid #00aaff;
            padding: 10px;
            font-size: 16px;
            letter-spacing: 2px;
        }
        /* Efecto hover: cuando pasás el mouse por encima del botón */
        .stButton > button:hover {
            background-color: #00aaff;
            color: #000000;
        }
        /* Animación de glitch (efecto visual para el Level Up) */
        @keyframes glitch {
            0%   { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
            25%  { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
            50%  { text-shadow: 2px 2px #ff00ff, -2px -2px #00ffff; }
            75%  { text-shadow: -2px 2px #ff00ff, 2px -2px #00ffff; }
            100% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
        }
        /* Animación de parpadeo para el Level Up */
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.3; }
        }
        /* Título del Level Up con las dos animaciones aplicadas */
        .levelup-title {
            color: #ffffff;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 6px;
            animation: glitch 0.4s infinite, blink 1s infinite;
        }
        /* Reloj digital que muestra la hora actual */
        .clock-display {
            font-family: monospace;
            font-size: 28px;
            color: #00aaff;
            letter-spacing: 4px;
            text-align: center;
            padding: 10px;
            border: 1px solid #00aaff33;
            border-radius: 8px;
            background-color: #000820;
        }
    </style>
""", unsafe_allow_html=True)

# ── Estado de sesión ──
# st.session_state es la "memoria" de la app mientras el usuario está en la página.
# Streamlit recarga la página cada vez que el usuario hace algo, así que necesitamos
# guardar en qué pantalla estamos y qué eventos ocurrieron.
# El operador "not in" verifica si la variable ya existe; si no existe, la crea.

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "notificacion_1"  # Pantalla inicial al abrir la app.

if "subio_nivel" not in st.session_state:
    st.session_state.subio_nivel = False  # Indica si el jugador subió de nivel hoy.

if "penalizo" not in st.session_state:
    st.session_state.penalizo = False  # Indica si el jugador recibió penalización hoy.


# ════════════════════════════════════════
# PANTALLA 1 — Primera notificación
# Es la primera pantalla que ve el usuario al abrir la app por primera vez
# ════════════════════════════════════════
if st.session_state.pantalla == "notificacion_1":
    st.markdown("""
        <div class="notification-box">
            <div class="notif-title">⚠ NOTIFICACION ⚠</div>
            <div class="notif-text">
                [ Misión Secreta. ]<br><br>
                <b>「 Valor de los Debiles 」</b><br><br>
                El Sistema te eligió.
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")

    # Creamos 3 columnas para centrar el botón (columna del medio es más ancha)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ACEPTAR", use_container_width=True):
            # Al aceptar, cambiamos la pantalla y recargamos la app
            st.session_state.pantalla = "notificacion_2"
            st.rerun()  # Fuerza la recarga de la página para mostrar la nueva pantalla


# ════════════════════════════════════════
# PANTALLA 2 — Segunda notificación
# Pregunta al usuario si acepta convertirse en Jugador.
# ════════════════════════════════════════
elif st.session_state.pantalla == "notificacion_2":
    st.markdown("""
        <div class="notification-box">
            <div class="notif-title">⚠ NOTIFICACION ⚠</div>
            <div class="notif-text">
                [ Análisis completado. ]<br><br>
                Posees las cualidades necesarias<br>
                para convertirte en un <b>Jugador</b>.<br><br>
                ¿Aceptás el desafio?
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ACEPTO", use_container_width=True):
            st.session_state.pantalla = "registro"
            st.rerun()


# ════════════════════════════════════════
# PANTALLA 3 — Registro del jugador
# El usuario ingresa su nombre y país para personalizar la experiencia.
# ════════════════════════════════════════
elif st.session_state.pantalla == "registro":
    st.markdown("""
        <div class="notification-box">
            <div class="notif-title">⚔ REGISTRO DE JUGADOR ⚔</div>
            <div class="notif-text">
                [ El Sistema requiere identificacion. ]<br><br>
                ¿Cual es tu nombre, Hunter?
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Campo de texto para el nombre
        nombre = st.text_input("", placeholder="Ingresa tu nombre...", key="input_nombre")
        # Menú desplegable con los países disponibles (importado de data.py)
        pais = st.selectbox("Tu pais:", list(PAISES_TIMEZONES.keys()), key="select_pais")
        if st.button("CONFIRMAR", use_container_width=True):
            # Validamos que el nombre no esté vacío
            if nombre.strip() == "":
                st.error("El Sistema requiere un nombre, Hunter.")
            else:
                # Cargamos los datos del jugador y actualizamos nombre y zona horaria
                jugador = cargar_jugador()
                jugador["nombre"] = nombre.strip()
                jugador["timezone"] = PAISES_TIMEZONES[pais]  # Guardamos la zona horaria según el país
                guardar_jugador(jugador)
                st.session_state.pantalla = "sistema"
                st.rerun()


# ════════════════════════════════════════
# PANTALLA 4 — Sistema principal
# Acá está todo: stats, misiones, buffs, penalizaciones e historial
# ════════════════════════════════════════
elif st.session_state.pantalla == "sistema":

    # Cargamos los datos del jugador desde el archivo JSON
    jugador = cargar_jugador()

    # Verificamos si cambió el día desde la última vez que entró
    # Esto activa penalizaciones o sube de nivel automáticamente
    resultado = verificar_nuevo_dia(jugador)

    # Recargamos el jugador porque verificar_nuevo_dia pudo haberlo modificado
    jugador = cargar_jugador()

    # Si subió de nivel, guardamos eso en session_state para mostrar la animación
    if resultado["subio_nivel"]:
        st.session_state.subio_nivel = True
        st.session_state.nuevo_nivel = jugador["nivel"]
        st.session_state.nuevo_rango = jugador["rango"]

    # Si fue penalizado (no completó misiones ayer), guardamos eso también
    if resultado["penalizo"]:
        st.session_state.penalizo = True

    # ── Animación de Level Up ──
    # Solo se muestra si el jugador subió de nivel (flag en session_state)
    if st.session_state.subio_nivel:
        st.markdown(f"""
            <div style="border: 2px solid #ffffff; border-radius: 10px; padding: 30px;
                        background-color: #000000; box-shadow: 0 0 30px #ffffff33;
                        text-align: center; margin-bottom: 20px;">
                <div class="levelup-title">[ LEVEL UP ]</div>
                <div style="color:#aaaaaa; font-size:16px; margin-top:15px; letter-spacing:3px;">
                    NIVEL <b style="color:#ffffff;">{st.session_state.nuevo_nivel}</b>
                    &nbsp;|&nbsp;
                    RANGO <b style="color:#ffffff;">{st.session_state.nuevo_rango}</b>
                </div>
                <div style="color:#555555; font-size:13px; margin-top:10px; letter-spacing:2px;">
                    El Sistema ha reconocido tu progreso.
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("CONTINUAR", use_container_width=True):
            st.session_state.subio_nivel = False  # Apagamos el flag para no mostrarla de nuevo
            st.rerun()

    # ── Pantalla de Penalización ──
    # Solo se muestra si el jugador no completó sus misiones el día anterior
    if st.session_state.penalizo and jugador.get("penalizacion_activa"):
        # Construimos la lista de misiones de castigo en formato HTML
        misiones_str = "".join([f"▸ {m}<br>" for m in jugador["penalizacion_activa"]])
        # La pérdida de XP depende de cuántos días seguidos falló (1 día = -30, 2 días = -60, 3+ = -100)
        perdida = {1: 30, 2: 60}.get(jugador["dias_sin_completar"], 100)
        st.markdown(f"""
            <div class="penalty-box">
                <div class="penalty-title">⚠ PENALIZACION ⚠</div>
                <div class="penalty-text">
                    [ No completaste tus misiones. ]<br><br>
                    <b style="color:#ff2200;">— {perdida} XP</b><br><br>
                    Misiones de castigo asignadas:<br><br>
                    {misiones_str}
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ENTENDIDO", use_container_width=True):
            st.session_state.penalizo = False  # Apagamos el flag
            st.rerun()

    # ── Notificación de Buff ──
    # Se muestra cuando el jugador alcanza exactamente 3, 7 o 30 días consecutivos
    racha = jugador["dias_consecutivos"]
    if racha in [3, 7, 30]:
        # Determinamos qué buff corresponde según la racha
        if racha == 3:
            buff_nombre = "CONCENTRACION"
            buff_desc = "Tu determinacion ha sido reconocida."
            buff_bonus = "+10% XP en todas las misiones"
        elif racha == 7:
            buff_nombre = "DETERMINACION"
            buff_desc = "El Sistema observa tu progreso."
            buff_bonus = "+25% XP en todas las misiones"
        else:
            buff_nombre = "MODO CAZADOR"
            buff_desc = "Pocos llegan hasta aqui, Hunter."
            buff_bonus = "+50% XP en todas las misiones"

        st.markdown(f"""
            <div style="border: 2px solid #ffd700; border-radius: 10px; padding: 20px;
                        background-color: #1a1400; box-shadow: 0 0 20px #ffd700;
                        text-align: center; margin-bottom: 20px;">
                <div style="color:#ffd700; font-size:22px; font-weight:bold; letter-spacing:4px;">
                    [ BUFF ACTIVADO ]
                </div>
                <div style="color:#ffd700; font-size:18px; margin-top:10px; font-weight:bold; letter-spacing:3px;">
                    {buff_nombre}
                </div>
                <div style="color:#aaaaaa; font-size:14px; margin-top:8px; letter-spacing:2px;">
                    {buff_desc}<br><br>
                    <b style="color:#ffd700;">{buff_bonus}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ── Reloj ──
    # Muestra la hora actual según la zona horaria del jugador
    tz = pytz.timezone(jugador.get("timezone", "America/Argentina/Buenos_Aires"))
    ahora = datetime.now(tz)                    # Hora actual en la zona horaria del jugador
    hora_str = ahora.strftime("%H:%M:%S")       # Formato: 14:30:00
    fecha_str = ahora.strftime("%d/%m/%Y")      # Formato: 13/03/2026

    st.markdown(f"""
        <div class="clock-display">
            {hora_str}
            <div style="font-size:13px; color:#00aaff88; letter-spacing:2px; margin-top:4px;">
                {fecha_str}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Script que recarga la página cada 60 segundos para actualizar el reloj
    st.markdown("""
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 60000);
        </script>
    """, unsafe_allow_html=True)

    st.write("")

    # ── Header principal ──
    # Muestra el nombre del sistema y saluda al jugador por su nombre
    st.markdown(f"""
        <div style="text-align:center; padding: 10px 0;">
            <div style="color:#00aaff; font-size:36px; font-weight:bold; letter-spacing:6px;">
                ⚔ SISTEMA ⚔
            </div>
            <div style="color:#ffffff; font-size:18px; margin-top:8px;">
                Bienvenido, <b>{jugador['nombre']}</b>.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()  # Línea separadora visual

    # ── Panel de estadísticas ──
    # Muestra Rango, Nivel, XP y Días consecutivos en 4 columnas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">RANGO</div>
                <div class="stat-value">{jugador['rango']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">NIVEL</div>
                <div class="stat-value">{jugador['nivel']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">XP</div>
                <div class="stat-value">{jugador['xp']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        # Determinamos qué buff tiene activo según la racha
        racha = jugador["dias_consecutivos"]
        if racha >= 30:
            buff_texto = "MODO CAZADOR +50%"
            buff_color = "#ffd700"
        elif racha >= 7:
            buff_texto = "DETERMINACION +25%"
            buff_color = "#ffd700"
        elif racha >= 3:
            buff_texto = "CONCENTRACION +10%"
            buff_color = "#ffd700"
        else:
            buff_texto = "—"
            buff_color = "#ffffff"
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">DIAS</div>
                <div class="stat-value">{jugador['dias_consecutivos']}/{jugador['dias_requeridos']}</div>
                <div style="color:{buff_color}; font-size:12px; letter-spacing:2px; margin-top:4px;">{buff_texto}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ── Barra de progreso de nivel ──
    # Calcula el porcentaje de días completados respecto a los requeridos para subir de nivel
    dias_progress = jugador['dias_consecutivos'] / jugador['dias_requeridos'] if jugador['dias_requeridos'] > 0 else 0
    st.markdown(f"<div style='color:#00aaff; letter-spacing:2px; font-size:13px;'>PROGRESO NIVEL — {jugador['dias_consecutivos']} / {jugador['dias_requeridos']} dias</div>", unsafe_allow_html=True)
    st.progress(min(dias_progress, 1.0))  # min() evita que supere el 100%

    st.divider()

    # ════════════════════════════════════════
    # SECCIÓN: MISIONES DIARIAS
    # Lista todas las misiones del jugador con checkboxes para marcarlas
    # ════════════════════════════════════════
    st.markdown("<div style='color:#00aaff; font-size:20px; font-weight:bold; letter-spacing:3px;'>[ MISIONES DIARIAS ]</div>", unsafe_allow_html=True)
    st.write("")

    # Verificamos si todas las misiones están completadas para mostrar un mensaje especial
    todas_completas = all(m["completada"] for m in jugador["misiones"])
    if todas_completas:
        st.markdown("""
            <div style="border: 1px solid #00ff88; border-radius: 8px; padding: 12px;
                        background-color: #001a0d; text-align:center; margin-bottom:15px;">
                <div style="color:#00ff88; letter-spacing:3px; font-size:14px;">
                    MISIONES DEL DIA COMPLETADAS
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Recorremos la lista de misiones con enumerate para tener el índice (i) y la misión
    for i, mision in enumerate(jugador["misiones"]):
        # Cada misión ocupa una fila con 3 columnas: checkbox | nombre | XP
        col_check, col_nombre, col_xp = st.columns([1, 6, 2])
        with col_check:
            # Checkbox interactivo — su estado inicial viene del JSON guardado
            completada = st.checkbox("", value=mision["completada"], key=f"mision_{i}")

            # Si el usuario cambió el estado del checkbox...
            if completada != mision["completada"]:
                jugador["misiones"][i]["completada"] = completada

                if completada:
                    # Calculamos el multiplicador de XP según la racha activa
                    racha = jugador["dias_consecutivos"]
                    if racha >= 30:
                        multiplicador = 1.5    # +50% XP
                    elif racha >= 7:
                        multiplicador = 1.25   # +25% XP
                    elif racha >= 3:
                        multiplicador = 1.10   # +10% XP
                    else:
                        multiplicador = 1.0    # Sin bonus

                    xp_ganado = int(mision["xp"] * multiplicador)
                    jugador["xp"] += xp_ganado  # Sumamos el XP al total
                else:
                    # Si desmarca la misión, le restamos el XP (sin bajar de 0)
                    jugador["xp"] = max(0, jugador["xp"] - mision["xp"])

                guardar_jugador(jugador)  # Guardamos los cambios en el JSON
                st.rerun()               # Recargamos para reflejar los cambios visualmente

        with col_nombre:
            # El nombre aparece en verde si está completada, blanco si no
            color = "#00ff88" if mision["completada"] else "#ffffff"
            st.markdown(f"<div style='color:{color}; padding-top:5px;'>{mision['nombre']}</div>", unsafe_allow_html=True)
        with col_xp:
            st.markdown(f"<div style='color:#00aaff; padding-top:5px; text-align:right;'>+{mision['xp']} XP</div>", unsafe_allow_html=True)

    st.divider()

    # ════════════════════════════════════════
    # SECCIÓN: GESTIÓN DE MISIONES
    # Permite agregar, editar y eliminar misiones
    # ════════════════════════════════════════
    st.markdown("<div style='color:#00aaff; font-size:20px; font-weight:bold; letter-spacing:3px;'>[ GESTION DE MISIONES ]</div>", unsafe_allow_html=True)
    st.write("")

    # Formulario para agregar una nueva misión (dentro de un expander para no ocupar espacio)
    with st.expander("+ AGREGAR MISIÓN"):
        col_n, col_xp = st.columns([3, 1])
        with col_n:
            nueva_nombre = st.text_input("Nombre de la mision", key="nueva_mision_nombre")
        with col_xp:
            # number_input es un campo numérico con límites mínimo y máximo
            nueva_xp = st.number_input("XP", min_value=10, max_value=500, value=50, step=10, key="nueva_mision_xp")
        if st.button("AGREGAR", use_container_width=True, key="btn_agregar"):
            if nueva_nombre.strip() == "":
                st.error("El Sistema requiere un nombre para la misión.")
            else:
                # Agregamos la nueva misión a la lista del jugador
                jugador["misiones"].append({
                    "nombre": nueva_nombre.strip(),
                    "xp": nueva_xp,
                    "completada": False  # Toda misión nueva empieza sin completar
                })
                guardar_jugador(jugador)
                st.rerun()

    st.write("")
    st.markdown("<div style='color:#00aaff88; font-size:13px; letter-spacing:2px;'>MODIFICAR MISIONES EXISTENTES</div>", unsafe_allow_html=True)
    st.write("")

    # Para cada misión existente, mostramos un expander con opciones de editar o eliminar
    for i, mision in enumerate(jugador["misiones"]):
        with st.expander(f"EDITAR: {mision['nombre']} — {mision['xp']} XP"):
            col_nom, col_xp2 = st.columns([3, 1])
            with col_nom:
                nuevo_nombre = st.text_input("Nombre", value=mision["nombre"], key=f"edit_nombre_{i}")
            with col_xp2:
                nuevo_xp = st.number_input("XP", min_value=10, max_value=500, value=mision["xp"], step=10, key=f"edit_xp_{i}")
            col_guardar, col_eliminar = st.columns(2)
            with col_guardar:
                if st.button("GUARDAR", key=f"btn_guardar_{i}", use_container_width=True):
                    # Actualizamos los datos de la misión en la lista
                    jugador["misiones"][i]["nombre"] = nuevo_nombre.strip()
                    jugador["misiones"][i]["xp"] = nuevo_xp
                    guardar_jugador(jugador)
                    st.rerun()
            with col_eliminar:
                if st.button("ELIMINAR", key=f"btn_eliminar_{i}", use_container_width=True):
                    # pop(i) elimina el elemento en la posición i de la lista
                    jugador["misiones"].pop(i)
                    guardar_jugador(jugador)
                    st.rerun()

    st.divider()

    # ════════════════════════════════════════
    # SECCIÓN: HISTORIAL
    # Muestra gráficos del progreso del jugador a lo largo del tiempo
    # ════════════════════════════════════════
    st.markdown("<div style='color:#00aaff; font-size:20px; font-weight:bold; letter-spacing:3px;'>[ HISTORIAL ]</div>", unsafe_allow_html=True)
    st.write("")

    historial = jugador.get("historial", [])  # Si no existe el historial, usamos lista vacía

    if len(historial) == 0:
        # Mensaje cuando todavía no hay datos históricos
        st.markdown("""
            <div style="border: 1px solid #00aaff33; border-radius: 8px; padding: 20px;
                        background-color: #000820; text-align:center;">
                <div style="color:#00aaff88; letter-spacing:2px; font-size:14px;">
                    [ SIN DATOS — Completá tu primer dia para ver el historial ]
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Extraemos los datos del historial para los gráficos
        fechas = [e["fecha"] for e in historial]
        xp_vals = [e["xp"] for e in historial]
        misiones_vals = [e["misiones_completadas"] for e in historial]
        total_vals = [e["total_misiones"] for e in historial]

        # ── Gráfico de XP por día ──
        # go.Figure() crea un gráfico vacío de Plotly
        fig_xp = go.Figure()
        fig_xp.add_trace(go.Scatter(
            x=fechas, y=xp_vals,
            mode="lines+markers",           # Línea con puntos
            line=dict(color="#00aaff", width=2),
            marker=dict(color="#00aaff", size=6),
            fill="tozeroy",                 # Rellena el área debajo de la línea
            fillcolor="rgba(0, 170, 255, 0.1)",
            name="XP"
        ))
        # Configuración visual del gráfico (fondo oscuro, colores del sistema)
        fig_xp.update_layout(
            title=dict(text="XP POR DIA", font=dict(color="#00aaff", size=14), x=0.5),
            paper_bgcolor="#000820",
            plot_bgcolor="#000820",
            font=dict(color="#ffffff"),
            xaxis=dict(gridcolor="#00aaff22", color="#00aaff88"),
            yaxis=dict(gridcolor="#00aaff22", color="#00aaff88"),
            margin=dict(l=20, r=20, t=40, b=20),
            height=250,
        )
        st.plotly_chart(fig_xp, use_container_width=True)

        # ── Gráfico de misiones por día (barras apiladas) ──
        fig_mis = go.Figure()
        # Barras verdes: misiones completadas
        fig_mis.add_trace(go.Bar(
            x=fechas, y=misiones_vals,
            marker_color="#00ff88",
            name="Completadas"
        ))
        # Barras rojas: misiones pendientes (total - completadas)
        fig_mis.add_trace(go.Bar(
            x=fechas,
            y=[t - m for t, m in zip(total_vals, misiones_vals)],  # zip combina las dos listas
            marker_color="#ff2200",
            name="Pendientes"
        ))
        fig_mis.update_layout(
            barmode="stack",  # Las barras se apilan una sobre otra
            title=dict(text="MISIONES POR DIA", font=dict(color="#00aaff", size=14), x=0.5),
            paper_bgcolor="#000820",
            plot_bgcolor="#000820",
            font=dict(color="#ffffff"),
            xaxis=dict(gridcolor="#00aaff22", color="#00aaff88"),
            yaxis=dict(gridcolor="#00aaff22", color="#00aaff88"),
            margin=dict(l=20, r=20, t=40, b=20),
            height=250,
            legend=dict(font=dict(color="#ffffff"))
        )
        st.plotly_chart(fig_mis, use_container_width=True)

        # Guardamos el historial actualizado al final de cada sesión
        guardar_historial(jugador)
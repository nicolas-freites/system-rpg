import streamlit as st
from datetime import datetime
import pytz
from data import cargar_jugador, guardar_jugador, verificar_nuevo_dia, guardar_historial, PAISES_TIMEZONES
import plotly.graph_objects as go

st.set_page_config(
    page_title="SISTEMA",
    page_icon="⚔️",
    layout="centered"
)

st.markdown("""
    <style>
        .notification-box {
            border: 2px solid #00aaff;
            border-radius: 10px;
            padding: 30px;
            background-color: #000820;
            box-shadow: 0 0 20px #00aaff;
            text-align: center;
        }
        .notif-title {
            color: #00aaff;
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 4px;
        }
        .notif-text {
            color: #ffffff;
            font-size: 18px;
            margin-top: 15px;
            line-height: 2;
        }
        .penalty-box {
            border: 2px solid #ff2200;
            border-radius: 10px;
            padding: 20px;
            background-color: #1a0000;
            box-shadow: 0 0 20px #ff2200;
            text-align: center;
            margin-bottom: 20px;
        }
        .penalty-title {
            color: #ff2200;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 4px;
        }
        .penalty-text {
            color: #ff6666;
            font-size: 16px;
            margin-top: 10px;
            line-height: 2;
        }
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
        .stat-label {
            color: #00aaff;
            font-size: 13px;
            letter-spacing: 2px;
        }
        .stat-value {
            color: #ffffff;
            font-size: 26px;
            font-weight: bold;
        }
        .stButton > button {
            background-color: #000820;
            color: #00aaff;
            border: 1px solid #00aaff;
            padding: 10px;
            font-size: 16px;
            letter-spacing: 2px;
        }
        .stButton > button:hover {
            background-color: #00aaff;
            color: #000000;
        }
        @keyframes glitch {
            0%   { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
            25%  { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
            50%  { text-shadow: 2px 2px #ff00ff, -2px -2px #00ffff; }
            75%  { text-shadow: -2px 2px #ff00ff, 2px -2px #00ffff; }
            100% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.3; }
        }
        .levelup-title {
            color: #ffffff;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 6px;
            animation: glitch 0.4s infinite, blink 1s infinite;
        }
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

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "notificacion_1"
if "subio_nivel" not in st.session_state:
    st.session_state.subio_nivel = False
if "penalizo" not in st.session_state:
    st.session_state.penalizo = False

# ─── Pantalla 1 ───
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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ACEPTAR", use_container_width=True):
            st.session_state.pantalla = "notificacion_2"
            st.rerun()

# ─── Pantalla 2 ───
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

# ─── Pantalla 3 — Registro ───
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
        nombre = st.text_input("", placeholder="Ingresa tu nombre...", key="input_nombre")
        pais = st.selectbox("Tu pais:", list(PAISES_TIMEZONES.keys()), key="select_pais")
        if st.button("CONFIRMAR", use_container_width=True):
            if nombre.strip() == "":
                st.error("El Sistema requiere un nombre, Hunter.")
            else:
                jugador = cargar_jugador()
                jugador["nombre"] = nombre.strip()
                jugador["timezone"] = PAISES_TIMEZONES[pais]
                guardar_jugador(jugador)
                st.session_state.pantalla = "sistema"
                st.rerun()

# ─── Pantalla 4 — Sistema principal ───
elif st.session_state.pantalla == "sistema":

    jugador = cargar_jugador()
    resultado = verificar_nuevo_dia(jugador)
    jugador = cargar_jugador()

    if resultado["subio_nivel"]:
        st.session_state.subio_nivel = True
        st.session_state.nuevo_nivel = jugador["nivel"]
        st.session_state.nuevo_rango = jugador["rango"]
    if resultado["penalizo"]:
        st.session_state.penalizo = True

    # ── Subida de Nivel ──
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
            st.session_state.subio_nivel = False
            st.rerun()

    # ── Penalización ──
    if st.session_state.penalizo and jugador.get("penalizacion_activa"):
        misiones_str = "".join([f"▸ {m}<br>" for m in jugador["penalizacion_activa"]])
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
            st.session_state.penalizo = False
            st.rerun()

    # ── Buff de racha ──
    racha = jugador["dias_consecutivos"]
    if racha in [3, 7, 30]:
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
    tz = pytz.timezone(jugador.get("timezone", "America/Argentina/Buenos_Aires"))
    ahora = datetime.now(tz)
    hora_str = ahora.strftime("%H:%M:%S")
    fecha_str = ahora.strftime("%d/%m/%Y")

    st.markdown(f"""
        <div class="clock-display">
            {hora_str}
            <div style="font-size:13px; color:#00aaff88; letter-spacing:2px; margin-top:4px;">
                {fecha_str}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 60000);
        </script>
    """, unsafe_allow_html=True)

    st.write("")

    # ── Header ──
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

    st.divider()

    # ── Stats ──
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

    dias_progress = jugador['dias_consecutivos'] / jugador['dias_requeridos'] if jugador['dias_requeridos'] > 0 else 0
    st.markdown(f"<div style='color:#00aaff; letter-spacing:2px; font-size:13px;'>PROGRESO NIVEL — {jugador['dias_consecutivos']} / {jugador['dias_requeridos']} dias</div>", unsafe_allow_html=True)
    st.progress(min(dias_progress, 1.0))

    st.divider()

    # ── Misiones ──
    st.markdown("<div style='color:#00aaff; font-size:20px; font-weight:bold; letter-spacing:3px;'>[ MISIONES DIARIAS ]</div>", unsafe_allow_html=True)
    st.write("")

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

    for i, mision in enumerate(jugador["misiones"]):
        col_check, col_nombre, col_xp = st.columns([1, 6, 2])
        with col_check:
            completada = st.checkbox("", value=mision["completada"], key=f"mision_{i}")
            if completada != mision["completada"]:
                jugador["misiones"][i]["completada"] = completada
                if completada:
                    racha = jugador["dias_consecutivos"]
                    if racha >= 30:
                        multiplicador = 1.5
                    elif racha >= 7:
                        multiplicador = 1.25
                    elif racha >= 3:
                        multiplicador = 1.10
                    else:
                        multiplicador = 1.0
                    xp_ganado = int(mision["xp"] * multiplicador)
                    jugador["xp"] += xp_ganado
                else:
                    jugador["xp"] = max(0, jugador["xp"] - mision["xp"])
                guardar_jugador(jugador)
                st.rerun()
        with col_nombre:
            color = "#00ff88" if mision["completada"] else "#ffffff"
            st.markdown(f"<div style='color:{color}; padding-top:5px;'>{mision['nombre']}</div>", unsafe_allow_html=True)
        with col_xp:
            st.markdown(f"<div style='color:#00aaff; padding-top:5px; text-align:right;'>+{mision['xp']} XP</div>", unsafe_allow_html=True)

    st.divider()

    # ── Gestión de Misiones ──
    st.markdown("<div style='color:#00aaff; font-size:20px; font-weight:bold; letter-spacing:3px;'>[ GESTION DE MISIONES ]</div>", unsafe_allow_html=True)
    st.write("")

    with st.expander("+ AGREGAR MISIÓN"):
        col_n, col_xp = st.columns([3, 1])
        with col_n:
            nueva_nombre = st.text_input("Nombre de la mision", key="nueva_mision_nombre")
        with col_xp:
            nueva_xp = st.number_input("XP", min_value=10, max_value=500, value=50, step=10, key="nueva_mision_xp")
        if st.button("AGREGAR", use_container_width=True, key="btn_agregar"):
            if nueva_nombre.strip() == "":
                st.error("El Sistema requiere un nombre para la misión.")
            else:
                jugador["misiones"].append({
                    "nombre": nueva_nombre.strip(),
                    "xp": nueva_xp,
                    "completada": False
                })
                guardar_jugador(jugador)
                st.rerun()

    st.write("")
    st.markdown("<div style='color:#00aaff88; font-size:13px; letter-spacing:2px;'>MODIFICAR MISIONES EXISTENTES</div>", unsafe_allow_html=True)
    st.write("")

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
                    jugador["misiones"][i]["nombre"] = nuevo_nombre.strip()
                    jugador["misiones"][i]["xp"] = nuevo_xp
                    guardar_jugador(jugador)
                    st.rerun()
            with col_eliminar:
                if st.button("ELIMINAR", key=f"btn_eliminar_{i}", use_container_width=True):
                    jugador["misiones"].pop(i)
                    guardar_jugador(jugador)
                    st.rerun()

    st.divider()

    # ── Historial ──
    st.markdown("<div style='color:#00aaff; font-size:20px; font-weight:bold; letter-spacing:3px;'>[ HISTORIAL ]</div>", unsafe_allow_html=True)
    st.write("")

    historial = jugador.get("historial", [])

    if len(historial) == 0:
        st.markdown("""
            <div style="border: 1px solid #00aaff33; border-radius: 8px; padding: 20px;
                        background-color: #000820; text-align:center;">
                <div style="color:#00aaff88; letter-spacing:2px; font-size:14px;">
                    [ SIN DATOS — Completá tu primer dia para ver el historial ]
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        fechas = [e["fecha"] for e in historial]
        xp_vals = [e["xp"] for e in historial]
        misiones_vals = [e["misiones_completadas"] for e in historial]
        total_vals = [e["total_misiones"] for e in historial]

        fig_xp = go.Figure()
        fig_xp.add_trace(go.Scatter(
            x=fechas, y=xp_vals,
            mode="lines+markers",
            line=dict(color="#00aaff", width=2),
            marker=dict(color="#00aaff", size=6),
            fill="tozeroy",
            fillcolor="rgba(0, 170, 255, 0.1)",
            name="XP"
        ))
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

        fig_mis = go.Figure()
        fig_mis.add_trace(go.Bar(
            x=fechas, y=misiones_vals,
            marker_color="#00ff88",
            name="Completadas"
        ))
        fig_mis.add_trace(go.Bar(
            x=fechas,
            y=[t - m for t, m in zip(total_vals, misiones_vals)],
            marker_color="#ff2200",
            name="Pendientes"
        ))
        fig_mis.update_layout(
            barmode="stack",
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

        guardar_historial(jugador)
import streamlit as st

def evaluar_readiness():
    st.title("🚦 Autocontrol Carga entrenamiento")
    
    st.write("---")
    
    # 1. FILTRO ESTRUCTURAL (Daño tisular)
    st.write("### Nivel 1: Integridad Estructural")
    lesion = st.selectbox("Lesión / Molestia Articular", ["Ninguna", "Molestia", "Pobre", "Lesionado"])
    val_lesion = {"Ninguna": 4, "Molestia": 3, "Pobre": 2, "Lesionado": 1}[lesion]
    
    # 2. FILTRO PERIFÉRICO (Recuperación metabólica y muscular)
    st.write("### Nivel 2: Recuperación Periférica")
    col1, col2, col3 = st.columns(3)
    with col1:
        sueno = st.selectbox("Calidad de sueño", ["Genial", "Bueno", "Promedio", "Pobre"])
    with col2:
        dolor = st.selectbox("Dolor muscular", ["Bajo", "Promedio", "Alto", "Extremo"])
    with col3:
        fatiga = st.selectbox("Fatiga sistémica", ["Bajo", "Promedio", "Alto", "Extremo"])

    # 3. FILTRO CENTRAL (Carga alostática y predisposición neuroendocrina)
    st.write("### Nivel 3: Predisposición Central")
    col4, col5, col6 = st.columns(3)
    with col4:
        motiv = st.selectbox("Motivación", ["Extremo", "Alto", "Promedio", "Bajo"])
    with col5:
        estres = st.selectbox("Estrés psicosocial", ["Bajo", "Promedio", "Alto", "Extremo"])
    with col6:
        animo = st.selectbox("Estado anímico", ["Genial", "Bueno", "Aceptar", "Gruñón"])

    st.write("**Tendencia Global del IRS (Máx 28 pts)**")
    sensacion_general = st.radio(
        "Evaluando los puntos anteriores, ¿te encuentras igual, peor o mejor que ayer?", 
        ["Mejor", "Igual", "Peor"]
    )
    
    # 4. FILTRO FISIOLÓGICO OBJETIVO (HRV / FCR)
    st.write("### Nivel 4: Marcador Fisiológico Objetivo")
    tipo_medicion = st.radio(
        "Selecciona tu método de monitorización de hoy:",
        ["Variabilidad de la Frecuencia Cardíaca (HRV)", "Frecuencia Cardíaca en Reposo (FCR)", "Ninguno (Solo evaluación subjetiva)"]
    )
    
    marcador_alterado = False
    dias_alerta = 0
    
    if tipo_medicion == "Variabilidad de la Frecuencia Cardíaca (HRV)":
        hrv_rango = st.radio("Gráfica de HRV (Intervals.icu) respecto a la línea base:", ["Dentro del rango normal", "Fuera del rango (por debajo o por encima)"])
        dias_alerta = st.number_input("Días consecutivos con HRV fuera de rango:", min_value=0, max_value=10, value=0)
        marcador_alterado = "Fuera" in hrv_rango
        
    elif tipo_medicion == "Frecuencia Cardíaca en Reposo (FCR)":
        fcr_rango = st.radio("FCR matutina respecto a tu media histórica:", ["Normal (estable)", "Elevada (>5 lpm sobre la media basal)"])
        dias_alerta = st.number_input("Días consecutivos con FCR elevada:", min_value=0, max_value=10, value=0)
        marcador_alterado = "Elevada" in fcr_rango
    
    st.write("---")
    ayer_rojo = st.checkbox("¿El entrenamiento de ayer fue ROJO (Series Z5 / Carga Severa)?")

    if st.button("Generar Semáforo Diario"):
        irs_empeora = sensacion_general == "Peor"
        
        # 1. Veto Estructural
        if val_lesion <= 2: 
            st.error("🔵 **CELESTE (Descanso):** Veto inmediato por lesión o molestia limitante. Se altera el patrón de zancada. Sesión a carga baja o descanso.")
            return
            
        # 2. Veto Fisiológico Sostenido
        if tipo_medicion != "Ninguno (Solo evaluación subjetiva)" and dias_alerta >= 3:
            st.error(f"🔵 **CELESTE (Descanso):** Alerta de 3 días con desviación en {tipo_medicion}. La sesión pasa automáticamente a descanso o baja intensidad[cite: 1, 3].")
            return
            
        # 3. Matriz de Decisión
        if tipo_medicion == "Ninguno (Solo evaluación subjetiva)":
            if irs_empeora:
                decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** ¡REGLA DE VETO SUBJETIVO! Musculatura fatigada o estrés mental. Prohibido Amarillo/Rojo. Carga máxima permitida: regenerativa o ligera."
            else:
                decision = "🔴/🟡/🟢/🔵 **ROJO, AMARILLO, VERDE, CELESTE o DESCANSO:** Predisposición subjetiva óptima. Atleta al 100% para realizar series intensas y vaciar reserva D'[cite: 1]."
        else:
            if marcador_alterado and irs_empeora:
                decision = "🔵 **CELESTE o DESCANSO:** Fatiga sistémica y fisiológica combinada. Veto total de carga. Solo descanso o regenerativo ligero[cite: 1, 3]."
            elif marcador_alterado and not irs_empeora:
                decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** Alteración fisiológica (HRV/FCR) sin molestias musculares graves. Como máximo un rodaje suave sin vaciar D'[cite: 1, 3]."
            elif not marcador_alterado and irs_empeora:
                decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** ¡REGLA DE VETO SUBJETIVO! Signos vitales normales, pero musculatura fatigada o estrés mental. Prohibido Amarillo/Rojo[cite: 1]."
            else:
                decision = "🔴/🟡/🟢/🔵 **ROJO, AMARILLO, VERDE, CELESTE o DESCANSO:** Sincronización perfecta. Atleta al 100% para realizar series intensas[cite: 1, 3]."
            
        # 4. Modulación por Carga Aguda Previa
        if ayer_rojo and ("ROJO" in decision):
            st.warning("🟡/🟢/🔵 **AMARILLO, VERDE, CELESTE o DESCANSO:** Por la regla de 'No Dobles Rojas', queda prohibido realizar dos entrenamientos ROJOS en días consecutivos[cite: 1, 3]. Intensidad máxima permitida hoy: Amarilla.")
        else:
            st.success(decision)

if __name__ == "__main__":
    evaluar_readiness()

import streamlit as st

def evaluar_readiness():
    st.title("Semáforo de Carga: HRV + Readiness")
    
    # 1. Datos Objetivos (HRV visual de Intervals.icu)
    st.write("**1. Variabilidad de la Frecuencia Cardíaca (HRV)**")
    
    hrv_rango = st.radio(
        "Observa tu gráfica de HRV en Intervals.icu. ¿Dónde se sitúa la barra de hoy respecto a la zona sombreada (línea base)?", 
        ["Dentro del rango normal (zona sombreada verde)", "Fuera del rango (por debajo o por encima)"]
    )
    
    hrv_tendencia = st.radio(
        "Tendencia de la HRV:", 
        ["Mayor o igual que ayer", "Menor que ayer"]
    )
    
    dias_hrv_baja = st.number_input(
        "¿Cuántos días consecutivos llevas con la barra de HRV por debajo de la zona sombreada?", 
        min_value=0, max_value=10, value=0
    )
    
    # 2. Cuestionario Subjetivo (IRS)
    st.write("**2. Índice de Readiness Subjetivo (IRS)**")
    
    col1, col2 = st.columns(2)
    with col1:
        sueno = st.selectbox("Calidad de sueño", ["Genial", "Bueno", "Promedio", "Pobre"])
        dolor = st.selectbox("Dolor muscular (Pre-entrenamiento)", ["Bajo", "Promedio", "Alto", "Extremo"])
        fatiga = st.selectbox("Fatiga (Pre-entrenamiento)", ["Bajo", "Promedio", "Alto", "Extremo"])
        estres = st.selectbox("Estrés", ["Bajo", "Promedio", "Alto", "Extremo"])
    with col2:
        animo = st.selectbox("Estado anímico", ["Genial", "Bueno", "Aceptar", "Gruñón"])
        motiv = st.selectbox("Motivación", ["Extremo", "Alto", "Promedio", "Bajo"])
        lesion = st.selectbox("Lesión", ["Ninguna", "Molestia", "Pobre", "Lesionado"])

    # Diccionarios de conversión para la regla de veto estructural por lesión
    val_lesion = {"Ninguna": 4, "Molestia": 3, "Pobre": 2, "Lesionado": 1}[lesion]
        
    st.write("**Tendencia Subjetiva**")
    sensacion_general = st.radio(
        "Sensación general, ¿te encuentras igual, peor o mejor que ayer?", 
        ["Mejor", "Igual", "Peor"]
    )
    
    # 3. Reglas de Entrenamiento
    st.write("**3. Contexto de Entrenamiento**")
    ayer_rojo = st.checkbox("¿El entrenamiento de ayer fue ROJO (Series Z5 / Carga Severa)?")

    if st.button("Generar Semáforo Diario"):
        # Evaluaciones lógicas
        hrv_fuera_rango = "Fuera" in hrv_rango
        irs_empeora = sensacion_general == "Peor"
        
        # Regla de Veto por Lesión
        if val_lesion <= 2: 
            st.error("🔵 **CELESTE (Descanso):** Veto inmediato por lesión o molestia limitante. Se altera el patrón de zancada. Sesión a carga baja o descanso[cite: 1].")
            return
            
        # Regla de 3 Días HRV
        if dias_hrv_baja >= 3:
            st.error("🔵 **CELESTE (Descanso):** Alerta de 3 días con desviación de HRV a la baja. La sesión pasa automáticamente a descanso o baja intensidad[cite: 1].")
            return
            
        # Matriz de Decisión Híbrida (indicando siempre el techo máximo y las opciones inferiores)
        if hrv_fuera_rango and irs_empeora:
            decision = "🔵 **CELESTE o DESCANSO:** Fatiga central y sistémica combinada. Veto total de carga. Solo descanso o regenerativo ligero[cite: 1]."
        elif hrv_fuera_rango and not irs_empeora:
            decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** Fatiga autónoma ligera. No hay molestias musculares graves. Como máximo un rodaje suave sin vaciar D'[cite: 1]."
        elif not hrv_fuera_rango and irs_empeora:
            decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** ¡REGLA DE VETO SUBJETIVO! Musculatura fatigada o estrés mental. Prohibido Amarillo/Rojo. Carga máxima permitida: regenerativa o ligera[cite: 1]."
        else:
            decision = "🔴/🟡/🟢/🔵 **ROJO, AMARILLO, VERDE, CELESTE o DESCANSO:** Sincronización perfecta. El atleta está al 100% para realizar series intensas y vaciar la reserva D' (pudiendo elegir cualquier intensidad inferior)[cite: 1]."
            
        # Regla No dobles rojas
        if ayer_rojo and ("ROJO" in decision):
            st.warning("🟡/🟢/🔵 **AMARILLO, VERDE, CELESTE o DESCANSO:** Por la regla de 'No Dobles Rojas', queda estrictamente prohibido realizar dos entrenamientos de intensidad ROJA en días consecutivos[cite: 1]. La intensidad máxima permitida hoy es Amarilla, pudiendo optar por sesiones más suaves (Verde, Celeste o Descanso).")
        else:
            st.success(decision)

if __name__ == "__main__":
    evaluar_readiness()

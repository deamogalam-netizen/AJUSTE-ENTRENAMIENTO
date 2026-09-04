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
        lesion = st.selectbox("Lesión", ["Ninguna", "Niggle (Molestia)", "Pobre", "Lesionado"])

    # Diccionarios de conversión a valores numéricos (4 = Óptimo, 1 = Pésimo)
    # Se unifican los criterios para poder sumar un IRS total
    val_sueno = {"Genial": 4, "Bueno": 3, "Promedio": 2, "Pobre": 1}[sueno]
    val_dolor = {"Bajo": 4, "Promedio": 3, "Alto": 2, "Extremo": 1}[dolor]
    val_fatiga = {"Bajo": 4, "Promedio": 3, "Alto": 2, "Extremo": 1}[fatiga]
    val_estres = {"Bajo": 4, "Promedio": 3, "Alto": 2, "Extremo": 1}[estres]
    val_animo = {"Genial": 4, "Bueno": 3, "Aceptar": 2, "Gruñón": 1}[animo]
    val_motiv = {"Extremo": 4, "Alto": 3, "Promedio": 2, "Bajo": 1}[motiv]
    val_lesion = {"Ninguna": 4, "Niggle (Molestia)": 3, "Pobre": 2, "Lesionado": 1}[lesion]
        
    irs_actual = val_sueno + val_dolor + val_fatiga + val_estres + val_animo + val_motiv + val_lesion
        
    irs_previo = st.number_input("Puntuación total IRS de ayer (para calcular si empeoras)", value=20, min_value=7, max_value=28)
    
    # 3. Reglas de Entrenamiento
    st.write("**3. Contexto de Entrenamiento**")
    ayer_rojo = st.checkbox("¿El entrenamiento de ayer fue ROJO (Series Z5 / Carga Severa)?")

    if st.button("Generar Semáforo Diario"):
        # Evaluaciones lógicas
        hrv_fuera_rango = "Fuera" in hrv_rango
        irs_empeora = irs_actual < irs_previo
        
        # Regla de Veto por Lesión
        if val_lesion <= 2: 
            st.error("🔵 **CELESTE (Descanso):** Veto inmediato por lesión o molestia limitante. Se altera el patrón de zancada. Sesión a carga baja o descanso[cite: 1].")
            return
            
        # Regla de 3 Días HRV
        if dias_hrv_baja >= 3:
            st.error("🔵 **CELESTE (Descanso):** Alerta de 3 días con desviación de HRV a la baja. Sesión pasa automáticamente a descanso/baja intensidad[cite: 1].")
            return
            
        # Matriz de Decisión Híbrida
        if hrv_fuera_rango and irs_empeora:
            decision = "🔵 **CELESTE:** Fatiga central y sistémica combinada. Veto total de carga. Solo descanso o regenerativo ligero[cite: 1]."
        elif hrv_fuera_rango and not irs_empeora:
            decision = "🟢 **VERDE:** Fatiga autónoma ligera. No hay molestias musculares graves. Rodaje suave sin vaciar D'[cite: 1]."
        elif not hrv_fuera_rango and irs_empeora:
            decision = "🔵/🟢 **CELESTE o VERDE:** ¡REGLA DE VETO SUBJETIVO! Musculatura fatigada o estrés mental. Prohibido Amarillo/Rojo[cite: 1]."
        else:
            decision = "🟡/🔴 **AMARILLO o ROJO:** Sincronización perfecta. El atleta está al 100% para realizar series intensas y vaciar la reserva D'[cite: 1]."
            
        # Regla No dobles rojas
        if ayer_rojo and ("AMARILLO o ROJO" in decision):
            st.warning("🟡 **AMARILLO:** Por la regla de 'No Dobles Rojas', queda estrictamente prohibido realizar dos entrenamientos de intensidad ROJA consecutivos[cite: 1].")
        else:
            st.success(decision)

if __name__ == "__main__":
    evaluar_readiness()

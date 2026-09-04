import streamlit as st

def evaluar_readiness():
    st.title("Semáforo de Carga: IRS + HRV")
    
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
        
    val_sueno = {"Genial": 4, "Bueno": 3, "Promedio": 2, "Pobre": 1}[sueno]
    val_dolor = {"Bajo": 4, "Promedio": 3, "Alto": 2, "Extremo": 1}[dolor]
    val_fatiga = {"Bajo": 4, "Promedio": 3, "Alto": 2, "Extremo": 1}[fatiga]

    # 3. FILTRO CENTRAL (Carga alostática y predisposición neuroendocrina)
    st.write("### Nivel 3: Predisposición Central")
    col4, col5, col6 = st.columns(3)
    with col4:
        motiv = st.selectbox("Motivación", ["Extremo", "Alto", "Promedio", "Bajo"])
    with col5:
        estres = st.selectbox("Estrés psicosocial", ["Bajo", "Promedio", "Alto", "Extremo"])
    with col6:
        animo = st.selectbox("Estado anímico", ["Genial", "Bueno", "Aceptar", "Gruñón"])
        
    val_motiv = {"Extremo": 4, "Alto": 3, "Promedio": 2, "Bajo": 1}[motiv]
    val_estres = {"Bajo": 4, "Promedio": 3, "Alto": 2, "Extremo": 1}[estres]
    val_animo = {"Genial": 4, "Bueno": 3, "Aceptar": 2, "Gruñón": 1}[animo]

    # Tendencia subjetiva global (IRS)
    st.write("**Tendencia Global del IRS (Máx 28 pts)**")
    sensacion_general = st.radio(
        "Evaluando los puntos anteriores, ¿te encuentras igual, peor o mejor que ayer?", 
        ["Mejor", "Igual", "Peor"]
    )
    
    # 4. FILTRO AUTONÓMICO (HRV objetiva)
    st.write("### Nivel 4: Marcador Autonómico (HRV)")
    hrv_rango = st.radio(
        "Gráfica de HRV (Intervals.icu) respecto a la línea base:", 
        ["Dentro del rango normal (zona sombreada verde)", "Fuera del rango (por debajo o por encima)"]
    )
    dias_hrv_baja = st.number_input(
        "Días consecutivos con HRV por debajo de la zona sombreada:", 
        min_value=0, max_value=10, value=0
    )
    
    # Contexto previo
    st.write("---")
    ayer_rojo = st.checkbox("¿El entrenamiento de ayer fue ROJO (Series Z5 / Carga Severa)?")

    if st.button("Generar Semáforo Diario"):
        hrv_fuera_rango = "Fuera" in hrv_rango
        irs_empeora = sensacion_general == "Peor"
        
        # Evaluación Jerárquica
        # 1. Veto Estructural
        if val_lesion <= 2: 
            st.error("🔵 **CELESTE (Descanso):** Veto inmediato por lesión o molestia limitante. Se altera el patrón de zancada. Sesión a carga baja o descanso.")
            return
            
        # 2. Veto Autonómico Sostenido
        if dias_hrv_baja >= 3:
            st.error("🔵 **CELESTE (Descanso):** Alerta de 3 días con desviación de HRV a la baja. La sesión pasa automáticamente a descanso o baja intensidad.")
            return
            
        # 3. Matriz de Decisión Híbrida
        if hrv_fuera_rango and irs_empeora:
            decision = "🔵 **CELESTE o DESCANSO:** Fatiga central y sistémica combinada. Veto total de carga. Solo descanso o regenerativo ligero."
        elif hrv_fuera_rango and not irs_empeora:
            decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** Fatiga autónoma ligera. No hay molestias musculares graves. Como máximo un rodaje suave sin vaciar D'[cite: 1]."
        elif not hrv_fuera_rango and irs_empeora:
            decision = "🟢/🔵 **VERDE, CELESTE o DESCANSO:** ¡REGLA DE VETO SUBJETIVO! Musculatura fatigada o estrés mental. Prohibido Amarillo/Rojo. Carga máxima permitida: regenerativa o ligera[cite: 1]."
        else:
            decision = "🔴/🟡/🟢/🔵 **ROJO, AMARILLO, VERDE, CELESTE o DESCANSO:** Sincronización perfecta. El atleta está al 100% para realizar series intensas y vaciar la reserva anaeróbica D' (pudiendo elegir cualquier intensidad inferior)[cite: 1]."
            
        # 4. Modulación por Carga Aguda Previa
        if ayer_rojo and ("ROJO" in decision):
            st.warning("🟡/🟢/🔵 **AMARILLO, VERDE, CELESTE o DESCANSO:** Por la regla de 'No Dobles Rojas', queda estrictamente prohibido realizar dos entrenamientos de intensidad ROJA en días consecutivos[cite: 1]. La intensidad máxima permitida hoy es Amarilla, pudiendo optar por sesiones más suaves.")
        else:
            st.success(decision)

if __name__ == "__main__":
    evaluar_readiness()

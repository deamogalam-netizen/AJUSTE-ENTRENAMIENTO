import streamlit as st

def evaluar_readiness():
    st.title("Algoritmo Híbrido de Autorregulación: HRV + Readiness")
    
    # Entradas Objetivas (HRV)
    hrv_actual = st.number_input("HRV de hoy (Ln rMSSD)", value=60.0)
    hrv_media = st.number_input("Media HRV 7 días", value=65.0)
    hrv_baja = hrv_actual < (hrv_media - 5) # Umbral simplificado
    dias_hrv_baja = st.number_input("Días consecutivos con HRV baja", min_value=0, max_value=10, value=0)
    
    # Entradas Subjetivas (IRS)
    st.write("Cuestionario de Readiness Subjetivo (1 = Muy mal, 5 = Excelente)")
    lesion = st.slider("Ausencia de Lesión/Molestia", 1, 5, 5)
    fatiga = st.slider("Nivel de Energía (Fatiga General)", 1, 5, 5)
    dolor_muscular = st.slider("Ausencia de Dolor Muscular", 1, 5, 5)
    
    irs_actual = fatiga + dolor_muscular # Simplificación del sumatorio
    irs_previo = st.number_input("Puntuación IRS del día anterior", value=10)
    irs_empeora = irs_actual < irs_previo
    
    # Reglas de Carga
    dias_rojos = st.checkbox("¿El entrenamiento de ayer fue de intensidad ROJA (Carga Severa)?")

    if st.button("Calcular Semáforo de Carga"):
        # Regla de Veto por Lesión
        if lesion <= 2:
            st.error("🔵 CELESTE: Veto inmediato por lesión o molestia limitante. Solo carga baja/descanso para evitar lesiones estructurales.")
            return
            
        # Regla de 3 Días
        if dias_hrv_baja >= 3:
            st.error("🔵 CELESTE: Alerta de 3 días con desviación de HRV a la baja. Sesión automática de descanso.")
            return
            
        # Matriz de Decisiones
        if hrv_baja and irs_empeora:
            resultado = "🔵 CELESTE: Fatiga central y sistémica combinada. Veto total de carga."
        elif hrv_baja and not irs_empeora:
            resultado = "🟢 VERDE: Fatiga autónoma ligera sin molestias musculares graves. Rodaje suave."
        elif not hrv_baja and irs_empeora:
            resultado = "🔵/🟢 CELESTE o VERDE: Regla de Veto Subjetivo. Musculatura fatigada. Prohibido series intensas."
        else:
            resultado = "🟡/🔴 AMARILLO o ROJO: Sincronización perfecta. Atleta al 100% para series intensas."
            
        # Regla No Dobles Rojas
        if dias_rojos and ("ROJO" in resultado):
            st.warning("🟡 AMARILLO: Estrictamente prohibido realizar dos entrenamientos ROJOS consecutivos. Se reduce la intensidad de hoy.")
        else:
            st.success(resultado)

if __name__ == "__main__":
    evaluar_readiness()

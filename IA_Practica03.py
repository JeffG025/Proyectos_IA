class ReporteEmergencia:
    """Representa los 'Hechos' de entrada del sistema."""
    def __init__(self, id_reporte, tipo_desastre, personas_riesgo, vias_bloqueadas, nivel_agua_metros=0.0):
        self.id_reporte = id_reporte
        self.tipo_desastre = tipo_desastre.capitalize()
        self.personas_riesgo = personas_riesgo
        self.vias_bloqueadas = vias_bloqueadas
        self.nivel_agua_metros = nivel_agua_metros
        
        self.prioridad = 99  
        self.recurso_asignado = "Pendiente de evaluación"

    def __str__(self):
        # Formatear la salida para que se vea como un panel de control real
        estado_via = "Cerrada" if self.vias_bloqueadas else "Abierta"
        return f"[Prioridad {self.prioridad}] {self.id_reporte} | {self.tipo_desastre} | Vías: {estado_via} | Vidas en riesgo: {self.personas_riesgo}\n    -> ACCIÓN: {self.recurso_asignado}\n"


class SistemaExpertoDesastres:
    """Motor de Inferencia y Base de Conocimiento."""
    def __init__(self):
        self.cola_emergencias = []

    def evaluar_reporte(self, reporte):
        # REGLA 1: Derrumbes críticos
        if reporte.tipo_desastre == "Derrumbe" and reporte.personas_riesgo > 0:
            reporte.prioridad = 1
            if reporte.vias_bloqueadas:
                reporte.recurso_asignado = "HELICÓPTERO y equipo de rescate USAR (Vías colapsadas)."
            else:
                reporte.recurso_asignado = "AMBULANCIAS y equipo USAR vía terrestre."
                
        # REGLA 2: Inundaciones severas
        elif reporte.tipo_desastre in ["Inundacion", "Inundación"] and reporte.nivel_agua_metros >= 1.0 and reporte.personas_riesgo > 0:
            reporte.prioridad = 1
            reporte.recurso_asignado = "LANCHAS de rescate rápido de Protección Civil."
            
        # REGLA 3: Inundaciones leves o preventivas
        elif reporte.tipo_desastre in ["Inundacion", "Inundación"] and 0.3 < reporte.nivel_agua_metros < 1.0:
            reporte.prioridad = 3
            reporte.recurso_asignado = "Vehículos 4x4 pesados para evacuación preventiva."
            
        # REGLA 4: Vías bloqueadas sin riesgo humano
        elif reporte.tipo_desastre == "Deslave" and reporte.personas_riesgo == 0 and reporte.vias_bloqueadas:
            reporte.prioridad = 4
            reporte.recurso_asignado = "MAQUINARIA PESADA para liberar vialidad."
            
        # REGLA 5: Daños materiales menores
        elif reporte.tipo_desastre in ["Arbol caido", "Árbol caído"] and reporte.personas_riesgo == 0:
            reporte.prioridad = 5
            reporte.recurso_asignado = "CUADRILLA DE LIMPIEZA en cuanto haya unidades."
            
        else:
            reporte.prioridad = 99
            reporte.recurso_asignado = "Evaluar manualmente. No coincide con reglas críticas."

        self.cola_emergencias.append(reporte)
        self.reordenar_triaje()

    def reordenar_triaje(self):
        self.cola_emergencias.sort(key=lambda r: r.prioridad)

    def mostrar_panel_control(self):
        print("\n" + "="*50)
        print("🚨 PANEL DE TRIAJE Y ASIGNACIÓN DE RECURSOS 🚨")
        print("="*50)
        for emergencia in self.cola_emergencias:
            print(emergencia)
        print("="*50 + "\n")


# ==========================================
# INTERFAZ DINÁMICA DE TERMINAL
# ==========================================
def iniciar_sistema():
    centro_mando = SistemaExpertoDesastres()
    contador = 1
    
    print("Iniciando Sistema Experto Centinela...")
    
    while True:
        print(f"\n--- NUEVO REPORTE (ID: REP-{contador:03d}) ---")
        
        # 1. Entrada de texto
        tipo = input("Tipo de emergencia (Derrumbe, Inundación, Deslave, Árbol caído): ").strip()
        
        # 2. Entrada numérica con validación
        try:
            personas = int(input("¿Cuántas personas están en riesgo vital? (Número): "))
        except ValueError:
            print("Error: Debes ingresar un número válido. Se asumirá 0.")
            personas = 0
            
        # 3. Entrada booleana
        vias = input("¿Las vías de acceso están bloqueadas? (s/n): ").strip().lower()
        vias_bloqueadas = True if vias == 's' else False
        
        # 4. Entrada condicional (Solo si es inundación)
        nivel_agua = 0.0
        if tipo.lower() in ["inundacion", "inundación"]:
            try:
                nivel_agua = float(input("¿Cuál es el nivel del agua estimado en metros? (Ej. 0.5): "))
            except ValueError:
                print("Error: Formato incorrecto. Se asumirá 0.0")
        
        # Crear reporte, evaluar y mostrar
        nuevo_reporte = ReporteEmergencia(f"REP-{contador:03d}", tipo, personas, vias_bloqueadas, nivel_agua)
        centro_mando.evaluar_reporte(nuevo_reporte)
        
        # Mostrar la sala de espera actualizada
        centro_mando.mostrar_panel_control()
        
        # Preguntar si se desea continuar
        continuar = input("¿Ingresar otro reporte? (s/n): ").strip().lower()
        if continuar != 's':
            print("\nCerrando sistema. Triaje finalizado.")
            break
            
        contador += 1

if __name__ == "__main__":
    iniciar_sistema()
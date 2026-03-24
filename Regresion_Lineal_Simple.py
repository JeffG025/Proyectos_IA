import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ==========================================
# PASO 1: RECOPILACIÓN DINÁMICA DE DATOS
# ==========================================
print("=====================================================")
print("📊 SISTEMA PREDICTIVO DE VENTAS Y MARKETING 📊")
print("=====================================================\n")

print("Primero, vamos a entrenar a la IA con el historial de tu negocio.")
print("La IA necesita saber cuánto invertiste en publicidad y cuánto vendiste en meses anteriores.\n")

# Preguntamos cuántos datos quiere ingresar el usuario
while True:
    try:
        n_meses = int(input("¿De cuántos meses tienes registro? (Ejemplo: 4, 5, 10): "))
        if n_meses >= 2:
            break
        else:
            print("  -> Ingresa al menos 2 meses para poder trazar una línea.")
    except ValueError:
        print("  -> Por favor, ingresa un número entero válido.")

X_lista = [] # Aquí guardaremos la inversión en publicidad (Causa)
y_lista = [] # Aquí guardaremos las ventas (Efecto)

print("\n--- INGRESA TUS DATOS (Pueden ser miles de pesos, ej: 1500) ---")
for i in range(n_meses):
    while True:
        try:
            inversion = float(input(f"Mes {i+1} - Inversión en Publicidad ($): "))
            ventas = float(input(f"Mes {i+1} - Ventas Totales generadas ($): "))
            
            # X necesita ser un arreglo de 2 dimensiones, por eso ponemos corchetes extra
            X_lista.append([inversion]) 
            y_lista.append(ventas)
            break
        except ValueError:
            print("  -> Error: Ingresa solo números. Intenta de nuevo ese mes.")

# Convertimos las listas normales a arreglos de numpy que la IA puede entender
X = np.array(X_lista)
y = np.array(y_lista)


# ==========================================
# PASO 2: ENTRENAR EL ALGORITMO
# ==========================================
print("\n⚙️ Entrenando modelo con TUS datos...")
modelo_marketing = LinearRegression()
modelo_marketing.fit(X, y)

print("✅ ¡Modelo entrenado!")
print(f"   Tu negocio genera aprox: ${modelo_marketing.coef_[0]:.2f} de ventas por cada $1 extra que inviertes en publicidad.")


# ==========================================
# PASO 3: PREDICCIÓN DINÁMICA E INTERACTIVA
# ==========================================
print("\n--- PREDICE EL FUTURO ---")
while True:
    try:
        nueva_inversion = float(input("¿Cuánto planeas invertir en publicidad el próximo mes? (o teclea 0 para salir): $"))
        
        if nueva_inversion == 0:
            print("Saliendo de las predicciones...")
            break
            
        # Hacemos la predicción con el dato que acaba de teclear el usuario
        prediccion_ventas = modelo_marketing.predict([[nueva_inversion]])
        print(f"  💸 -> La IA estima que tus VENTAS serán de: ${prediccion_ventas[0]:.2f}\n")
        
    except ValueError:
        print("  -> Por favor, ingresa una cantidad válida.")


# ==========================================
# PASO 4: VISUALIZACIÓN DE TUS DATOS
# ==========================================
print("\nGenerando tu gráfica personalizada... (Cierra la ventana de la gráfica para finalizar el script)")

plt.figure(figsize=(10, 6))

# Dibujar tus datos reales
plt.scatter(X, y, color='blue', s=80, label='Historial de tu Negocio')

# Dibujar la línea de tendencia de la IA
X_linea = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_linea = modelo_marketing.predict(X_linea)
plt.plot(X_linea, y_linea, color='red', linewidth=3, linestyle='--', label='Tendencia Aprendida')

plt.title('📈 Impacto de la Publicidad en las Ventas')
plt.xlabel('Inversión en Publicidad ($)')
plt.ylabel('Ventas Totales ($)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# Mostrar la gráfica
plt.show()     
# Pick and place using PS5 Controller for a Phantom X Pincher
## Participants:
- Jonathan Andrés Jimenez Trujillo
- Daniel Mauricio Rivero Lozada
- Yeira Liseth Rodriguez Rodriguez
- Daniel Felipe Valbuena Reyes

# Pasos

## Cinématica directa e inversa
Para abordar la cinemática directa, se inicia con la toma de una imagen del robot Phantom Pincher en una posición en forma de "L", como se observa en la figura. Este enfoque se elige con el objetivo de simplificar los cálculos y el análisis de la cinemática directa. A continuación, se procedió a dibujar los sistemas de coordenadas correspondientes a cada una de las articulaciones, siguiendo el marco de referencia establecido por Denavit-Hartenberg. Posteriormente, se construye la matriz DH para la cinemática directa, analizando cada uno de los eslabones y articulaciones, tal como se ilustra en las imágenes a continuación.

<img src="https://github.com/user-attachments/assets/6cbf92c4-93fd-450c-b00a-3b559d2b2505" width="300"/> ![image](https://github.com/user-attachments/assets/aeba4fe4-343d-4f64-9a35-3c4469fd515f)


Con la matriz DH definida, se continúa el desarrollo en MATLAB utilizando el Toolbox de Peter Corke. Este se emplea para crear el modelo del robot Pincher con la matriz de cinemática directa y para generar los enlaces (links). Gracias a este mismo Toolbox, es posible calcular la matriz que relaciona la base con la primera articulación. Luego, se obtiene la matriz que vincula la primera articulación con la segunda. Al multiplicar las matrices 𝐴01 y 𝐴12, se obtiene 𝐴02, y así sucesivamente, hasta llegar al TCP. Este proceso será útil en etapas posteriores para el cálculo del Jacobiano, que será fundamental para la manipulación de las articulaciones del robot.

El gráfico del robot generado permite confirmar que el modelo está correctamente definido y coincide con la imagen obtenida previamente.

![image](https://github.com/user-attachments/assets/3f20b5a6-bd70-4beb-a13a-f27a63d80870) ![image](https://github.com/user-attachments/assets/9ed7f17d-e433-48a7-ac6d-42354f548d64)

En cuanto a la cinemática inversa, se optó por no realizar el cálculo, ya que no se utilizará esta técnica en la implementación del proyecto. La estrategia elegida para la manipulación del efector final se basa en movimientos lineales en los que se considera que el desplazamiento en 𝑥,𝑦 y 𝑧, es un Δ𝑥. Al operar este desplazamiento con el Jacobiano, se puede obtener un vector Δ𝑞, que corresponde a los cambios que deben realizar las articulaciones para cumplir con los desplazamientos solicitados. Este enfoque se considera más sencillo, eficiente y directo, y es la solución adoptada para abordar el problema de manera efectiva.

## Cálculo del Jacobiano




## Configuración Joystick --- Botones (Control)

## Visualización Coppelia

## Configuración de la cámara
## Hacer mover el robot

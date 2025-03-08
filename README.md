# Pick and place using PS5 Controller for a Phantom X Pincher
## Participants:
- Jonathan Andrés Jimenez Trujillo
- Daniel Mauricio Rivero Lozada
- Yeira Liseth Rodriguez Rodriguez
- Daniel Felipe Valbuena Reyes

# Pasos

## Cinématica directa e inversa
Para abordar la cinemática directa, se inicia con la toma de una imagen del robot Phantom Pincher en una posición en forma de "L", como se observa en la figura. Este enfoque se elige con el objetivo de simplificar los cálculos y el análisis de la cinemática directa. A continuación, se procedió a dibujar los sistemas de coordenadas correspondientes a cada una de las articulaciones, siguiendo el marco de referencia establecido por Denavit-Hartenberg. Posteriormente, se construye la matriz DH para la cinemática directa, analizando cada uno de los eslabones y articulaciones, tal como se ilustra en las imágenes a continuación.

<img src="https://github.com/user-attachments/assets/6cbf92c4-93fd-450c-b00a-3b559d2b2505" width="300"/> ![image](https://github.com/user-attachments/assets/aeba4fe4-343d-4f64-9a35-3c4469fd515f) ![image](https://github.com/user-attachments/assets/19ce62ca-894a-4908-aa8c-52978fb34ae9)


Con la matriz DH definida, se continúa el desarrollo en MATLAB utilizando el Toolbox de Peter Corke. Este se emplea para crear el modelo del robot Pincher con la matriz de cinemática directa y para generar los enlaces (links). Gracias a este mismo Toolbox, es posible calcular la matriz que relaciona la base con la primera articulación. Luego, se obtiene la matriz que vincula la primera articulación con la segunda. Al multiplicar las matrices 𝐴01 y 𝐴12, se obtiene 𝐴02, y así sucesivamente, hasta llegar al TCP. Este proceso será útil en etapas posteriores para el cálculo del Jacobiano, que será fundamental para la manipulación de las articulaciones del robot.

El gráfico del robot generado permite confirmar que el modelo está correctamente definido y coincide con la imagen obtenida previamente.

![image](https://github.com/user-attachments/assets/3f20b5a6-bd70-4beb-a13a-f27a63d80870) ![image](https://github.com/user-attachments/assets/9ed7f17d-e433-48a7-ac6d-42354f548d64)

En cuanto a la cinemática inversa, se optó por no realizar el cálculo, ya que no se utilizará esta técnica en la implementación del proyecto. La estrategia elegida para la manipulación del efector final se basa en movimientos lineales en los que se considera que el desplazamiento en 𝑥,𝑦 y 𝑧, es un Δ𝑥. Al operar este desplazamiento con el Jacobiano, se puede obtener un vector Δ𝑞, que corresponde a los cambios que deben realizar las articulaciones para cumplir con los desplazamientos solicitados. Este enfoque se considera más sencillo, eficiente y directo, y es la solución adoptada para abordar el problema de manera efectiva.

## Cálculo del Jacobiano
El cálculo del jacobiano se realizó de dos maneras:

Método semi-manual:
1. Primero, se multiplicaron las matrices que relacionan las articulaciones con las bases del robot. Para cada matriz obtenida, se tomaron los vectores 𝑧𝑖 y 𝑜𝑖, correspondientes a cada articulación. Al tener únicamente articulaciones rotacionales, la matriz jacobiana se construyó en dos partes:
   - Las primeras tres filas se calcularon utilizando el producto cruz de 𝑧𝑖−1 con la diferencia (𝑜𝑛−𝑜𝑖−1).
   - Las siguientes tres filas se construyeron tomando cada columna como 𝑧𝑖−1.
Esto dio como resultado una matriz jacobiana geométrica completa de tamaño 6×4.

![image](https://github.com/user-attachments/assets/213e8eac-2d07-4190-bf5a-cbb5abe1ea86) ![image](https://github.com/user-attachments/assets/9e1734e4-310e-454c-a727-11a9a73f5fa6)

2. Método automático con Peter Corke Toolbox:
La segunda forma de obtener la matriz jacobiana fue utilizando la función jacob0 del toolbox de Peter Corke en MATLAB 'J_g = (Pincher.jacob0(q))'. Se verificó que los resultados obtenidos con ambos métodos fueran consistentes, lo que validó la precisión de ambos enfoques.

Aunque la función jacob0 proporcionó la matriz jacobiana, se decidió dejar la matriz expresada de manera simbólica para que pueda cambiar dinámicamente con respecto al vector 𝑞, que corresponde a la posición actual de las articulaciones del robot. Esto es crucial para la implementación, ya que en cada momento se reciben las posiciones actuales del robot y, por lo tanto, se recalcula el jacobiano en tiempo real.



Para completar los cálculos, se necesitan dos vectores de entrada:
  - Un vector 𝑞 de tamaño 4×1, que representa los valores de las articulaciones del robot.
  - Un vector Δ𝑥 de tamaño 6×1, que representa los cambios en las coordenadas 𝑥, 𝑦 y 𝑧.
    
Con estos vectores, se calcula el jacobiano bajo la configuración articular actual. Luego, se multiplica el vector Δ𝑥 por la pseudo-inversa de la matriz jacobiana para obtener el vector Δ𝑞, que indica los cambios que deben realizarse en las articulaciones para alcanzar la posición deseada.

### Implementación en Python con ROS2
La implementación de los paquetes y nodos de ROS2 se realizó en Python. Se creó un archivo .py que se convierte en el nodo del jacobiano. En este archivo, se incorpora la matriz jacobiana en su forma simbólica utilizando la librería sympy, lo que permite calcularla dinámicamente para cada posición.

Este nodo tiene dos roles:
- Subscriber: Recibe dos vectores Float64:
    - 𝑞 (la posición actual de las articulaciones) y Δ𝑥 (el cambio deseado en la posición). Al recibir estos vectores, se llama a las funciones internas para calcular la matriz jacobiana y el vector Δ𝑞.
- Publisher: Publica el vector Δ𝑞, que es utilizado por otro nodo para modificar las articulaciones del robot Phantom Pincher.
  
### Resultados y Pruebas
Se realizaron pruebas en MATLAB con vectores de prueba y en el nodo de ROS2. Ambos métodos generaron los mismos resultados, lo que confirmó la correcta ejecución de los cálculos y el tratamiento adecuado de los vectores. Este enfoque asegura que el cálculo del jacobiano y el ajuste de las articulaciones se realicen de manera precisa y eficiente durante la operación del robot.

![image](https://github.com/user-attachments/assets/15f25ea2-f42a-4849-a6e5-9cdadc402d2d) ![image](https://github.com/user-attachments/assets/219fa95e-96cf-4b3f-aaec-4c8e0d0101f5)

## Diagrama de Flujo 

<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/images/flow_diagram.png" width="400">

El diagrama de flujo, describe de forma integrada el proceso de teleoperación y simulación del robot Phantom X Pincher. El sistema se inicia mediante un archivo de lanzamiento (launch file) que pone en marcha el nodo maestro y todos los componentes esenciales, tales como el nodo de hardware que gestiona el robot, el nodo que se suscribe a los estados articulares (a través del tópico /joint_states) y los nodos o servicios de cinemática inversa, los cuales son responsables de traducir las posiciones deseadas en ángulos articulares adecuados. En este punto, se verifica la conexión y la operatividad del robot; si se detecta alguna anomalía, se reintenta la conexión o se detiene la ejecución del sistema.

Posteriormente, el flujo contempla la opción de seleccionar el modo de operación mediante la integración del joystick, administrado por un nodo que publica en el tópico /joy. Si se opta por el control manual, los datos del joystick se procesan para generar comandos de velocidad o de posición, que posteriormente se convierten en ángulos articulares mediante un nuevo cálculo de cinemática inversa. Alternativamente, en el modo automático se emplean rutinas preprogramadas que definen trayectorias específicas para la ejecución de tareas, eliminando la necesidad de entrada manual. Los comandos resultantes, ya sea derivados de la entrada del joystick o de las trayectorias automáticas, se publican en tópicos correspondientes (por ejemplo, /cmd_vel o un tópico de comandos articulares) para controlar el movimiento del robot.

El flujo culmina con la integración de la simulación en CoppeliaSim, donde un nodo puente o plugin se encarga de traducir los comandos recibidos a acciones en el entorno virtual, garantizando que la simulación refleje de manera precisa el comportamiento del robot. Este ciclo se repite de forma continua mientras el sistema esté en operación, permitiendo la actualización en tiempo real de los estados del robot y de la simulación, hasta que se emita una orden de parada o finalice la rutina programada. En conjunto, el diagrama de flujo representa un sistema de teleoperación robusto y dinámico, en el que la interconexión entre nodos y tópicos de ROS permite una comunicación fluida entre la interfaz de usuario, el cálculo de la cinemática y la ejecución en entornos tanto reales como simulados.

## Configuración Joystick --- Botones (Control)

## Visualización Coppelia

## Configuración de la cámara
## Hacer mover el robot

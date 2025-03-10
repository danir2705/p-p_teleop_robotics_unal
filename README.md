# Pick and place using PS5 Controller for a Phantom X Pincher

## Participantes:
- Jonathan Andrés Jimenez Trujillo
- Daniel Mauricio Rivero Lozada
- Yeira Liseth Rodriguez Rodriguez
- Daniel Felipe Valbuena Reyes

### Teleoperación del Robot Phantom X Pincher mediante Cinemática Diferencial

Este repositorio contiene la implementación de un sistema de teleoperación para el robot **Phantom X Pincher**, basado en **ROS2**.

#### Características del Proyecto

- Implementación de la **cinemática directa**.
- Cálculo simbólico del **jacobiano** en **Python**.
- Uso de **ROS2** para la comunicación entre nodos.
- Integración con un **joystick** para la teleoperación manual.
- Validación en **MATLAB**.

#### Instalación y Configuración

##### Requisitos Previos

- **ROS2 Foxy/Humble**
- Python 3.8+

##### Clonación y Configuración del Espacio de Trabajo

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/danir2705/p-p_teleop_robotics_unal/tree/main/src
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```
#### Pruebas y Validación

1. **Verificación en MATLAB**: Se usó el Robotics Toolbox de Peter Corke para comparar resultados.
2. **Simulación en ROS2**: Se probó la teleoperación con modelos virtuales.
3. **Pruebas en Hardware**: Se conectó al Phantom X Pincher y se validaron movimientos suaves y precisos.

# Cálculos posición y orientación

## Cinématica directa e inversa
Para abordar la cinemática directa, se inicia con la toma de una imagen del robot Phantom Pincher en una posición en forma de "L", como se observa en la figura. Este enfoque se elige con el objetivo de simplificar los cálculos y el análisis de la cinemática directa. A continuación, se procedió a dibujar los sistemas de coordenadas correspondientes a cada una de las articulaciones, siguiendo el marco de referencia establecido por Denavit-Hartenberg. Posteriormente, se construye la matriz DH para la cinemática directa, analizando cada uno de los eslabones y articulaciones.

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/PincherX-100_page-0001.jpg" width="400">
</p>

Con la matriz DH definida, se continúa el desarrollo en MATLAB utilizando el Toolbox de Peter Corke. Este se emplea para crear el modelo del robot Pincher con la matriz de cinemática directa y para generar los enlaces (links). Gracias a este mismo Toolbox, es posible calcular la matriz que relaciona la base con la primera articulación. Luego, se obtiene la matriz que vincula la primera articulación con la segunda. Al multiplicar las matrices 𝐴01 y 𝐴12, se obtiene 𝐴02, y así sucesivamente, hasta llegar al TCP. Este proceso será útil en etapas posteriores para el cálculo del Jacobiano, que será fundamental para la manipulación de las articulaciones del robot.

Esta tabla representa los parámetros Denavit-Hartenberg (DH) del robot.

| Junta | \( $$\theta$$ \) (°) | \( d \) (mm) | \( a \) (mm) | \( $$\alpha$$ \) (rad) | Offset |
|-------|------------|----------|--------|---------------|--------|
| \( $$q_1$$ \) | Variable | 89.45 | 0 | \( $$\frac{\pi}{2}$$ \) | 0 |
| \( $$q_2$$ \) | Variable | 0 | 105.95 | 0 | 1.2341 |
| \( $$q_3$$ \) | Variable | 0 | 100 | 0 | -1.23 |
| \( $$q_4$$ \) | Variable | 0 | 86.05 | 0 | 0 |

Nota: Los valores de \( $$\theta$$ \) son variables, mientras que los desplazamientos y longitudes de enlace están dadas en milímetros.

El gráfico del robot generado permite confirmar que el modelo está correctamente definido y coincide con la imagen obtenida previamente.

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/imagenDH.png" width="400">
</p>

En cuanto a la cinemática inversa, se optó por no realizar el cálculo, ya que no se utilizará esta técnica en la implementación del proyecto. La estrategia elegida para la manipulación del efector final se basa en movimientos lineales en los que se considera que el desplazamiento en 𝑥,𝑦 y 𝑧, es un Δ𝑥. Al operar este desplazamiento con el Jacobiano, se puede obtener un vector Δ𝑞, que corresponde a los cambios que deben realizar las articulaciones para cumplir con los desplazamientos solicitados. Este enfoque se considera más sencillo, eficiente y directo, y es la solución adoptada para abordar el problema de manera efectiva.

## Cálculo del Jacobiano
El cálculo del jacobiano se realizó de dos maneras:

Método semi-manual:
1. Primero, se multiplicaron las matrices que relacionan las articulaciones con las bases del robot. Para cada matriz obtenida, se tomaron los vectores 𝑧𝑖 y 𝑜𝑖, correspondientes a cada articulación. Al tener únicamente articulaciones rotacionales, la matriz jacobiana se construyó en dos partes:
   - Las primeras tres filas se calcularon utilizando el producto cruz de 𝑧𝑖−1 con la diferencia (𝑜𝑛−𝑜𝑖−1).
   - Las siguientes tres filas se construyeron tomando cada columna como 𝑧𝑖−1.
Esto dio como resultado una matriz jacobiana geométrica completa de tamaño 6×4.

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

# Pasos del proceso y Arquitectura del Sistema

## Diagrama de Flujo 

El diagrama de flujo, describe de forma integrada el proceso de teleoperación y simulación del robot Phantom X Pincher. El sistema se inicia mediante un archivo de lanzamiento (launch file) que pone en marcha el nodo maestro y todos los componentes esenciales, tales como el nodo de hardware que gestiona el robot, el nodo que se suscribe a los estados articulares (a través del tópico /joint_states) y los nodos o servicios de cinemática inversa, los cuales son responsables de traducir las posiciones deseadas en ángulos articulares adecuados. En este punto, se verifica la conexión y la operatividad del robot; si se detecta alguna anomalía, se reintenta la conexión o se detiene la ejecución del sistema.

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/flow_diagram.png" width="400">
</p>

Posteriormente, el flujo contempla la opción de seleccionar el modo de operación mediante la integración del joystick, administrado por un nodo que publica en el tópico /joy. Si se opta por el control manual, los datos del joystick se procesan para generar comandos de velocidad o de posición, que posteriormente se convierten en ángulos articulares mediante un nuevo cálculo de cinemática inversa. Alternativamente, en el modo automático se emplean rutinas preprogramadas que definen trayectorias específicas para la ejecución de tareas, eliminando la necesidad de entrada manual. Los comandos resultantes, ya sea derivados de la entrada del joystick o de las trayectorias automáticas, se publican en tópicos correspondientes (por ejemplo, /cmd_vel o un tópico de comandos articulares) para controlar el movimiento del robot.

El flujo culmina con la integración de la simulación en MATLAB, donde un nodo puente o plugin se encarga de traducir los comandos recibidos a acciones en el entorno virtual, garantizando que la simulación refleje de manera precisa el comportamiento del robot. Este ciclo se repite de forma continua mientras el sistema esté en operación, permitiendo la actualización en tiempo real de los estados del robot y de la simulación, hasta que se emita una orden de parada o finalice la rutina programada. En conjunto, el diagrama de flujo representa un sistema de teleoperación robusto y dinámico, en el que la interconexión entre nodos y tópicos de ROS permite una comunicación fluida entre la interfaz de usuario, el cálculo de la cinemática y la ejecución en entornos tanto reales como simulados.

##  Nodos y tópicos

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/Nodos.jpeg" width="800">
</p>

El sistema se organiza en los siguientes nodos:

* 'phantom_joy': Captura la interacción del control de PS4, donde los sticks analógicos regulan la velocidad y los botones permiten cambiar el estado del sistema. Luego, envía esta información en forma de comandos de velocidad y modo de operación.

* 'phantom_mode': Define el estado operativo del robot, determinando si se encuentra en modo manual o automático. También se encarga de enviar esta información a otros nodos.

* 'phantom_diff': Calcula la velocidad necesaria para cada articulación del robot utilizando la matriz Jacobiana a partir de los comandos de velocidad enviados por el controlador.

* 'phantom_control': Inicia los controladores de velocidad del Phantom Px100 a través de un script de lanzamiento (viz_launch.py). Este nodo es clave para la ejecución del movimiento del brazo.

* 'phantom_mode (gemelo digital)': Representa la simulación del robot en un entorno virtual, permitiendo probar y visualizar el comportamiento del brazo antes de ejecutarlo físicamente.

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/rosgraph.png" width="900">
</p>

# Estación remota y visualización

## Configuración Joystick --- Botones (Control)

Se divide en dos archivos principales: PS4Controller.py, que maneja la lectura de los datos del joystick, y joy_tracker.py, que actúa como un nodo de ROS2 publicando la información procesada en tópicos específicos. Para el primero se usa una función que escuha los eventors del joystick y actualiza los valores según el botón (en un boleano) o devuelve un vector con los valores de los ejes. Por otro lado, joy_tracker.py define el nodo PhantomJoy, que se encarga de recibir la información del joystick y publicarla en ROS2. Este nodo tiene dos publicadores: uno para enviar velocidades como un mensaje Twist en el tópico joy_vel y otro para enviar el modo de operación (manual o automático) como un mensaje Bool en el tópico operation_mode.

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/ps4_photo.jpg" width="200">
</p>

La obtención de los valores de los ejes y la actualización de los datos de control se actualiza continuamente, así como se verifica el modo de operación actual ya sea con los botones X o Círculo. 

## Visualización Coppelia y R_viz

Este archivo de lanzamiento en ROS2 automatiza la apertura de CoppeliaSim con una escena predefinida. Para ello, localiza el paquete donde se encuentra la escena y ejecuta el simulador como un proceso externo. Esto permite que CoppeliaSim se inicie junto con otros nodos de ROS2, facilitando la integración y automatizando el flujo de trabajo sin necesidad de abrir el simulador manualmente.

<p align="center">
<img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/sim_coppelia.png" width="500">
</p>

## Trayectoria y rutina

<div align="center">
  <a href="https://drive.google.com/file/d/1Udc-wwv2dIOUX_I1wh8XVtV829M44O2a/view?usp=sharing">
  <img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/simulacion.png" width="400">
  </a>
  <p><em>Click en la imagen para abrir video</em></p>
</div>


# Implementación final

<div align="center">
  <a href="https://drive.google.com/file/d/11eDLsTr2OdRrjGnuTbBnuILa6CpbUE7G/view?usp=drive_link">
  <img src="https://github.com/danir2705/p-p_teleop_robotics_unal/blob/main/figures/large.png" width="300">
  </a>
  <p><em>Click en la imagen para abrir video</em></p>
</div>

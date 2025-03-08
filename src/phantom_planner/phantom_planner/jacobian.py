import rclpy
import numpy as np

from rclpy.node import Node

from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray, Bool



class JacobianOperator(Node):

    def __init__(self):
        super().__init__('jacobian_translator')

        self.publisher_ = self.create_publisher(JointState, 'coppelia/joint_commands', 10)
        self.publisher_cmds = self.create_publisher(Float64MultiArray, '/position_controller/commands', 10)
        self.subscriber = self.create_subscription(Twist, 'joy_vel', self.vel_cmd_callback, 10)

        self.subscriber = self.create_subscription(Bool, 'operation_mode', self.operation_mode_callback, 10)


        self.enable_manual = True

    def dh_transform(self, theta, d, a, alpha):
        return np.array([
            [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
            [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])


    def jacobian_dh(self, q):
        """
        Calcula la matriz jacobiana para un robot con articulaciones de tipo revolutivo.
        
        q: lista de ángulos articulares (configuración actual).
        
        Retorna la matriz jacobiana J.
        """
        # Parámetros DH: (theta, d, a, alpha)
        parameters_dh = [
            (0, 0.5, 0.4, np.pi/2),  # Articulación 1
            (0, 0, 0.3, 0),          # Articulación 2
            (0, 0.5, 0.3, np.pi/2),  # Articulación 3
            (0, 0, 0.2, 0)           # Articulación 4
        ]
        
        n = len(q)  # Número de articulaciones
        J_v = np.zeros((3, n))  # Parte lineal de la jacobiana
        J_omega = np.zeros((3, n))  # Parte angular de la jacobiana
        
        # Matriz de transformación acumulada
        T = np.eye(4)
        
        # Vector de posiciones de cada articulación
        positions = [np.zeros(3)]  # La base (primer eslabón) está en el origen
        
        # Calculamos las matrices de transformación homogénea para cada eslabón
        for i in range(n):
            theta, d, a, alpha = parameters_dh[i]
            
            # Ajustar theta con el ángulo articular correspondiente
            T_i = self.dh_transform(q[i], d, a, alpha)
            T = np.dot(T, T_i)  # Actualizamos la transformación acumulada
            
            # Almacenamos la posición de cada eslabón (traslación)
            positions.append(T[:3, 3])
        
        # Calcular la jacobiana
        for i in range(n):
            # Eje de rotación (la parte angular de la jacobiana)
            z_i = np.array([0, 0, 1])  # Eje Z de la articulación i
            
            # La posición de la articulación i y el end-effector
            p_i = positions[i]
            p_end = positions[-1]  # Posición del end-effector
            
            # Parte angular (derivada de la orientación)
            J_omega[:, i] = z_i
            
            # Parte lineal (derivada de la posición)
            J_v[:, i] = np.cross(z_i, p_end - p_i)
        
        # Concatenamos la parte lineal y angular para obtener la matriz jacobiana completa
        J = np.vstack((J_v, J_omega))
        
        return J
    
    def jacobian_pseudoinverse(self, J):
        """
        Calcula la pseudoinversa de la matriz jacobiana utilizando la descomposición en valores singulares (SVD).
        
        J: Matriz jacobiana.
        
        Retorna la pseudoinversa de la jacobiana J.
        """
        # Realizar la descomposición en valores singulares
        U, S, Vt = np.linalg.svd(J)
        
        # Pseudoinversa: J+ = V * S+ * U.T
        # Crear la matriz de valores singulares invertidos
        S_inv = np.zeros_like(J.T)
        for i in range(len(S)):
            if S[i] > 1e-6:  # Considerar valores singulares pequeños como 0 para evitar problemas numéricos
                S_inv[i, i] = 1 / S[i]
        
        # Calcular la pseudoinversa
        J_pseudo_inv = np.dot(Vt.T, np.dot(S_inv, U.T))
        
        return J_pseudo_inv

    def operation_mode_callback(self, msg: Bool): 
        self.enable_manual = msg.data

    def vel_cmd_callback(self, msg: Twist): 
        dx = msg.linear.x 
        dy = msg.linear.y 
        dz = msg.linear.z 

        dX = np.array([[dx, dy, dz, 0,0,0]]).T
        J = self.jacobian_dh([0, 0.3, 1, 0])

        dq = self.jacobian_pseudoinverse(J) @ dX 
        dq = dq.T

        self.get_logger().info(str(dq[0]))

        # Publish to command 
        dq_cmd = JointState()

        VEL_FACTOR = 2
        dq_cmd.name = ['waist', 'shoulder', 'elbow', 'wrist_angle']
        dq_cmd.position = dq[0].tolist() 
        dq_cmd.velocity = [0.0, 0.0, 0.0, 0.0]
        dq_cmd.effort = [0.0, 0.0, 0.0, 0.0]

        dq_multiarray = Float64MultiArray() 

        dq_multiarray.data = [0.1 * e for e in dq_cmd.position ]


        self.publisher_.publish(dq_cmd)

        if not self.enable_manual: 
            self.publisher_cmds.publish(dq_multiarray)
        elif sum(dq_multiarray.data) == 0.0 :
            self.get_logger().info("Auto mode. Activate manual mode to move the pincher manually.")



def main(args=None):
    rclpy.init(args=args)
    jacobian_node = JacobianOperator()
    rclpy.spin(jacobian_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    jacobian_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
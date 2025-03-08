import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from rclpy.qos import QoSProfile
import argparse
import sympy as sp


class VectorPublisherSubscriber(Node):
    def __init__(self):
        super().__init__('vector_publisher_subscriber')

        # Definir el publisher para el resultado
        self.publisher = self.create_publisher(Float64MultiArray, 'resultado_vector', QoSProfile(depth=10))

        # Crear los subscribers para recibir los vectores
        self.create_subscription(Float64MultiArray, 'vector_4x1', self.listener_callback_4x1, QoSProfile(depth=10))
        self.create_subscription(Float64MultiArray, 'vector_6x1', self.listener_callback_6x1, QoSProfile(depth=10))

        # Inicializar variables para almacenar los vectores
        self.vector_4x1 = None
        self.vector_6x1 = None

    def listener_callback_4x1(self, msg):
        self.vector_4x1 = msg.data
        self.get_logger().info(f"Recibido vector_4x1: {self.vector_4x1}")

        # Si ambos vectores están disponibles, realizar el cálculo
        if self.vector_4x1 is not None and self.vector_6x1 is not None:
            self.calcular_y_publicar(self.vector_6x1, self.vector_4x1)

    def listener_callback_6x1(self, msg):
        self.vector_6x1 = msg.data
        self.get_logger().info(f"Recibido vector_6x1: {self.vector_6x1}")

        # Si ambos vectores están disponibles, realizar el cálculo
        if self.vector_4x1 is not None and self.vector_6x1 is not None:
            self.calcular_y_publicar(self.vector_6x1, self.vector_4x1)

    def calcular_y_publicar(self, vector_6x1, vector_4x1):
        self.get_logger().info("Iniciando cálculo y publicación...")

        try:
            q1, q2, q3, q4 = vector_4x1

            # Obtener la matriz y su pseudo-inversa
            matriz = self.c_matriz(q1, q2, q3, q4)
            matriz_inv = self.c_inv(matriz)

            # Multiplicar la pseudo-inversa por el vector 6x1 recibido
            v_sp = sp.Matrix(vector_6x1)
            delta_q = matriz_inv * v_sp

            # Convertir el resultado a una lista de float64
            resultado_lista = [float(val) for val in delta_q]

            # Publicar el resultado
            msg = Float64MultiArray()
            msg.data = resultado_lista
            self.publisher.publish(msg)

            self.get_logger().info(f"Publicando el resultado: {resultado_lista}")

        except Exception as e:
            self.get_logger().error(f"Ocurrió un error al calcular y publicar: {e}")

    def c_matriz(self, q1, q2, q3, q4):
        sin = sp.sin
        cos = sp.cos

        # Primera fila
        a11 = (5.5 * sin(q2 - q1 + q3 + q4)) - (5.25 * sin(q1 + q2 + q3)) + (5.25 * cos(q1 - q2)) - (
                5.5 * sin(q1 + q2 + q3 + q4)) - (5.25 * cos(q1 + q2)) + (5.25 * sin(q2 - q1 + q3))
        a12 = (-5.25 * sin(q1 + q2 + q3)) - (5.5 * sin(q2 - q1 + q3 + q4)) - (5.25 * cos(q1 - q2)) - (
                5.5 * sin(q1 + q2 + q3 + q4)) - (5.25 * cos(q1 + q2)) - (5.25 * sin(q2 - q1 + q3))
        a13 = (-5.25 * sin(q1 + q2 + q3)) - (5.5 * sin(q2 - q1 + q3 + q4)) - (5.5 * sin(q1 + q2 + q3 + q4)) - (
                5.25 * sin(q2 - q1 + q3))
        a14 = -(5.5 * sin(q2 - q1 + q3 + q4)) - (5.5 * sin(q1 + q2 + q3 + q4))

        # Segunda fila
        a21 = (5.25 * cos(q1 + q2 + q3)) + (5.5 * cos(q2 - q1 + q3 + q4)) + (5.25 * sin(q1 - q2)) + (
                5.5 * cos(q1 + q2 + q3 + q4)) - (5.25 * sin(q1 + q2)) + (5.25 * cos(q2 - q1 + q3))
        a22 = (5.25 * cos(q1 + q2 + q3)) - (5.5 * cos(q2 - q1 + q3 + q4)) - (5.25 * sin(q1 - q2)) + (
                5.5 * cos(q1 + q2 + q3 + q4)) - (5.25 * sin(q1 + q2)) - (5.25 * cos(q2 - q1 + q3))
        a23 = (5.25 * cos(q1 + q2 + q3)) - (5.5 * cos(q2 - q1 + q3 + q4)) + (5.5 * cos(q1 + q2 + q3 + q4)) - (
                5.25 * cos(q2 - q1 + q3))
        a24 = (5.5 * cos(q2 - q1 + q3 + q4)) - (5.5 * cos(q2 - q1 + q3 + q4))

        # Tercera fila
        a31 = 0
        a32 = (11 * cos(q2 + q3 + q4)) + (10.5 * cos(q2 + q3)) - (10.5 * sin(q2))
        a33 = (11 * cos(q2 + q3 + q4)) + (10.5 * cos(q2 + q3))
        a34 = (11 * cos(q2 + q3 + q4))

        # Cuarta fila
        a41 = 0
        a42 = sin(q1)
        a43 = sin(q1)
        a44 = sin(q1)

        # Quinta fila
        a51 = 0
        a52 = -cos(q1)
        a53 = -cos(q1)
        a54 = -cos(q1)

        # Sexta fila
        a61 = 1
        a62 = 0
        a63 = 0
        a64 = 0

        # Crear la matriz
        Matriz = [
            [a11, a12, a13, a14],
            [a21, a22, a23, a24],
            [a31, a32, a33, a34],
            [a41, a42, a43, a44],
            [a51, a52, a53, a54],
            [a61, a62, a63, a64],
        ]
        return Matriz

    def c_inv(self, Matriz_total):
        Matriz_sp = sp.Matrix(Matriz_total)
        Matriz_inv = Matriz_sp.pinv().evalf(3)
        # Definir un umbral para los valores muy pequeños
        umbral = 1e-4  # El valor debajo del cual se considerará como 0

        # Aproximar valores pequeños a cero
        for i in range(Matriz_inv.shape[0]):
            for j in range(Matriz_inv.shape[1]):
                if abs(Matriz_inv[i, j]) < umbral:
                    Matriz_inv[i, j] = 0

        return Matriz_inv


def parse_args():
    # Analizar los vectores pasados por consola
    parser = argparse.ArgumentParser(description='Pase los vectores 4x1 y 6x1 desde la consola.')
    parser.add_argument('vector_6x1', type=str, help='Vector 6x1, por ejemplo: "[1, 2, 3, 4, 5, 6]"')
    parser.add_argument('vector_4x1', type=str, help='Vector 4x1, por ejemplo: "[1, 2, 3, 4]"')

    args = parser.parse_args()

    # Convertir las cadenas de texto a listas de números (y asegurarse de que sean float)
    vector_6x1 = [float(i) for i in eval(args.vector_6x1)]  # Convierte los valores a float
    vector_4x1 = [float(i) for i in eval(args.vector_4x1)]  # Convierte los valores a float

    return vector_6x1, vector_4x1


def main(args=None):
    rclpy.init(args=args)

    # Crear el nodo
    vector_publisher_subscriber = VectorPublisherSubscriber()

    # Parsear los vectores desde la consola
    vector_6x1, vector_4x1 = parse_args()

    # Ahora, ejecutar directamente el cálculo y la publicación con los vectores
    # Publicar los vectores para activar los callbacks
    vector_publisher_subscriber.listener_callback_6x1(Float64MultiArray(data=vector_6x1))
    vector_publisher_subscriber.listener_callback_4x1(Float64MultiArray(data=vector_4x1))

    # Asegurarse de que el nodo está corriendo
    rclpy.spin(vector_publisher_subscriber)

    # Destruir el nodo y cerrar la ejecución
    vector_publisher_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

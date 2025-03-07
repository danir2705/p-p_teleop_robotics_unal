import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys

# Importar la librería correcta según el sistema operativo
if sys.platform.startswith('win'):
    import msvcrt
else:
    import termios
    import tty

class KeyMover(Node):
    def __init__(self):
        super().__init__('key_mover')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('Presiona A para mover a la derecha, B para mover a la izquierda. Ctrl+C para salir.')

    def get_key(self):
        """ Captura la tecla presionada en Windows o Unix """
        if sys.platform.startswith('win'):
            return msvcrt.getch().decode('utf-8').lower()
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return key.lower()

    def run(self):
        """ Lee la tecla y publica la velocidad a turtlesim """
        while rclpy.ok():
            key = self.get_key()
            twist = Twist()

            if key == '\x03':  # Captura Ctrl+C
                    self.get_logger().info('Saliendo del nodo...')
                    break

            if key == 'a':  # Mover a la derecha
                twist.angular.z = -1.0
                self.get_logger().info(f'Tecla presionada: {key}')
            elif key == 'b':  # Mover a la izquierda
                twist.angular.z = 1.0
                self.get_logger().info(f'Tecla presionada: {key}')
            else:
                continue  # Ignorar teclas no deseadas

            self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = KeyMover()
    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info('Nodo detenido.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

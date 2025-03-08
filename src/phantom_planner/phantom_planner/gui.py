import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_msgs.msg import Float64MultiArray
import tkinter as tk
from tkinter import ttk
from threading import Thread


class GUIPlanner(Node):

    def __init__(self):
        super().__init__('gui_planner')

        # ROS 2 Subscriber for operating mode (Bool)
        self.subscription_mode = self.create_subscription(
            Bool,
            '/operation_mode',  # Topic for the operating mode (True/False)
            self.mode_callback,
            10
        )
        self.subscription_mode  # Prevent unused variable warning

        # ROS 2 Subscriber for position controller (Float32MultiArray)
        self.subscription_position = self.create_subscription(
            Float64MultiArray,
            '/position_controller/commands',  # Topic for the position vector
            self.position_callback,
            10
        )
        self.subscription_position  # Prevent unused variable warning

        # Tkinter GUI setup
        self.root = tk.Tk()
        self.root.title("ROS 2 Operating Mode and Position Display")

        # Operating mode indicator (Initially Red, assuming False mode)
        self.mode_label = tk.Label(self.root, text="Modo Manual: OFF", font=("Arial", 14))
        self.mode_label.config(bg="red", width=30, height=2)
        self.mode_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Grid layout for two columns
        self.auto_mode_label = tk.Label(self.root, text="qdot:", font=("Arial", 14))
        self.auto_mode_label.grid(row=1, column=0, pady=10, sticky="w")
        
        self.position_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.position_entry.grid(row=1, column=1, pady=10)
        self.position_entry.config(state="disabled")  # Initially disabled

        self.routine_label = tk.Label(self.root, text="Select Routine:", font=("Arial", 14))
        self.routine_label.grid(row=2, column=0, pady=10, sticky="w")
        
        # Routine selection ComboBox (disabled initially)
        self.routine_combo = ttk.Combobox(self.root, values=["Rutina 1", "Rutina 2"], font=("Arial", 14))
        self.routine_combo.grid(row=2, column=1, pady=10)
        self.routine_combo.config(state="disabled")  # Initially disabled

        # Button to trigger routine (disabled initially)
        self.run_button = tk.Button(self.root, text="Run", font=("Arial", 14), command=self.run_routine)
        self.run_button.grid(row=3, column=0, columnspan=2, pady=20)
        self.run_button.config(state="disabled")  # Initially disabled

        # Quit button to close the Tkinter window
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # ROS 2 thread
        self.ros_thread = Thread(target=self.spin_ros)
        self.ros_thread.start()

    def mode_callback(self, msg):
        # Update the operating mode label and color
        if msg.data:
            self.mode_label.config(text="Modo Manual: OFF", bg="red")
            # Disable auto mode data and enable routine section
            self.position_entry.config(state="disabled")
            self.routine_combo.config(state="normal")
            self.run_button.config(state="normal")
        else:
            self.mode_label.config(text="Modo Manual: ON", bg="green")
            # Disable routine section and enable auto mode data
            self.position_entry.config(state="normal")
            self.routine_combo.config(state="disabled")
            self.run_button.config(state="disabled")

    def position_callback(self, msg):
        # Update the position entry with the received data (x, y, z components)
        position_text = ", ".join([f"{value:.2f}" for value in msg.data])
        self.position_entry.delete(0, tk.END)  # Clear current entry text
        self.position_entry.insert(0, position_text)  # Insert new data

    def run_routine(self):
        selected_routine = self.routine_combo.get()
        print(f"Running {selected_routine}")

    def spin_ros(self):
        # Spins ROS 2 while running the Tkinter GUI
        rclpy.spin(self)

    def close(self):
        self.root.quit()


def main(args=None):
    rclpy.init(args=args)

    gui_planner = GUIPlanner()

    # Start Tkinter main loop in the main thread
    gui_planner.root.mainloop()

    # Clean up ROS 2 node before exiting
    gui_planner.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

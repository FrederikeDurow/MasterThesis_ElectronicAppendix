import rclpy
from rclpy.node import Node
import tkinter as tk
from std_msgs.msg import String
# Constants
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 15
level = 1
start_x = 50 
start_y = 20 
running = True

class BT_Subscriber(Node):

    def __init__(self):
        super().__init__('Behavior_Tree_Visualizer')
        self.subscription = self.create_subscription(
            String,
            '/behavior_tree',
            self.bt_callback,
            10)
        # Create Tkinter window
        tkroot = tk.Tk()
        tkroot.title("Behavior Tree Visualization")

        # Create canvas
        self.canvas = tk.Canvas(tkroot, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='black')
        self.canvas.pack()

    def bt_callback(self, msg):
        self.draw_behavior_tree(msg.data)
        self.canvas.update()

    def draw_text(self, text, x, y, color='white'):
        self.canvas.create_text(x, y, text=text, fill=color, font=('Helvetica', FONT_SIZE), anchor='w')

    def draw_behavior_tree(self, msg):
        try: 
            nodes = msg.strip().split('\n')
            for node in nodes: 
                name, x, y, color = node.split(',')
                name = name.strip()
                x = float(x)
                y = float(y)
                color = color.strip()
                self.draw_text(name, x, y, color)
        except Exception as e: 
            print(str(e))
        

def main(args=None):
    rclpy.init(args=args)
    bt_sub = BT_Subscriber()
    rclpy.spin(bt_sub)
    bt_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
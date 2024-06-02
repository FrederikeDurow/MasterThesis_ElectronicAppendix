import yaml
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PolygonStamped, Point32

class PolygonPublisher(Node):
    def __init__(self, yaml_file="/home/nuc242/MasterThesisGit/bt_ws/src/behavior_tree/behavior_tree/config/regions.yaml"):
        super().__init__('polygon_publisher')
        self.yaml=yaml_file
        self.regions = self.load_yaml()
        self.polygon_publishers = {}
        self.centroids_dict = {}
        self.create_polygon_publishers()

    def load_yaml(self):
        # Load the YAML file
        with open(self.yaml, 'r') as file:
            self.polygons_data = yaml.safe_load(file)

        # Check if the YAML file is empty or not properly loaded
        if self.polygons_data is not None and isinstance(self.polygons_data, dict):
            # Iterate over each polygon in the YAML file
            for polygon_name, polygon_data in self.polygons_data.items():
                # Access the vertices of the current polygon
                polygon_vertices = polygon_data.get('vertices', [])

                # Check if 'centroid' key already exists in the current polygon entry
                if 'centroid' not in polygon_data:
                    # Calculate the centroid of the current polygon
                    centroid_polygon = self.calculate_region_centroid(polygon_vertices)

                    polygon_data['centroid'] = {'x': centroid_polygon[0], 'y': centroid_polygon[1]}

            with open(self.yaml, 'w') as file:
                yaml.dump(self.polygons_data, file, default_flow_style=False)
        else:
            print("Error: YAML file is empty or not properly loaded.")

        return self.polygons_data

    def create_polygon_publishers(self):
        for polygon_name in self.polygons_data.keys():
            topic_name = f'region_{polygon_name}'
            self.polygon_publishers[polygon_name] = self.create_publisher(PolygonStamped, topic_name, 10)

    def calculate_region_centroid(self,vertices):
        n = len(vertices)
        if n < 3:
            raise ValueError("A polygon must have at least three vertices.")
        area = 0
        cx = 0
        cy = 0

        for i in range(n):
            xi, yi = vertices[i]['x'], vertices[i]['y']
            xi1, yi1 = vertices[(i + 1) % n]['x'], vertices[(i + 1) % n]['y']
            common_term = xi * yi1 - xi1 * yi
            area += common_term
            cx += (xi + xi1) * common_term
            cy += (yi + yi1) * common_term

        area *= 0.5
        cx /= (6 * area)
        cy /= (6 * area)

        return cx, cy

    def publish_polygons(self):
        for polygon_name, publisher in self.polygon_publishers.items():
            polygon_data = self.polygons_data[polygon_name]

            # Publish the current polygon
            polygon_msg = PolygonStamped()
            polygon_msg.header.frame_id = 'map'  # Replace with your frame_id
            polygon_msg.header.stamp = self.get_clock().now().to_msg()

            for vertex in polygon_data['vertices']:
                point = Point32(x=float(vertex['x']), y=float(vertex['y']), z=0.0)
                polygon_msg.polygon.points.append(point)

            center = Point32(x=float(polygon_data['centroid']['x']), y=float(polygon_data['centroid']['y']), z=0.0)
            self.centroids_dict[polygon_name]=center

            publisher.publish(polygon_msg)

    def get_centroid(self,region_name:str):
        return self.centroids_dict[region_name]

def main(args=None):
    rclpy.init(args=args)
    polygon_publisher = PolygonPublisher()
    polygon_publisher.create_timer(1.0, polygon_publisher.publish_polygons)
    rclpy.spin(polygon_publisher)
    polygon_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
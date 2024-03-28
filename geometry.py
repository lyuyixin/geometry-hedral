import numpy as np
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


############################################################
# Setup Hello World
############################################################


class Hello(Resource):

    # Corresponds to the GET request.
    # This function is called whenever there is a GET request for this resource
    # on the terminal type: curl http://127.0.0.1:5000/
    # Returns hello world when we use GET.
    # Returns the data that we send when we use POST.
    def get(self):
        return jsonify({'message': 'hello world'})

        # Corresponds to POST request

    def post(self):
        data = request.get_json()  # status code
        return jsonify({'data': data}), 201


############################################################
# Problem 1. Smallest Bounding Square
# Given an array of 3D Points,
# calculate the Smallest Bounding Box that contains all the 3D Points.
# POST request, on the terminal type:
# curl -X POST -H "Content-Type: application/json" -d
# '{"points": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}'
# http://127.0.0.1:5000/smallest_bounding_square
############################################################


class SmallestBoundingSquare(Resource):

    def post(self):  # retrieving data and calculate
        data = request.json
        # Corner case
        if not data:
            return make_response(
                jsonify({'error': 'Missing required JSON data'}), 400)
        points = data.get('points')
        if not points:
            return make_response(
                jsonify({'error': 'Missing points data'}), 400)

        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')

        # Traverse points, get the max and min of coordinates x,y,z,
        for point in points:
            x, y, z = point
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)

        # Calculate width, height, depth
        width = max_x - min_x
        height = max_y - min_y
        depth = max_z - min_z

        return jsonify({
            'min_x': min_x,
            'min_y': min_y,
            'min_z': min_z,
            'max_x': max_x,
            'max_y': max_y,
            'max_z': max_z,
            'width': width,
            'height': height,
            'depth': depth
        })


############################################################
# Problem 2. Rotate 3d Mesh
# Given a 3D Mesh as an input,
# rotate the mesh by X degrees along the specified axis.
# POST request, on the terminal type:
# curl -X POST -H "Content-Type: application/json" -d
# '{"mesh": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "angle": 30, "axis": "Y"}'
# http://127.0.0.1:5000/rotate_3d_mesh
############################################################


class Rotate3dMesh(Resource):

    def post(self):  # retrieving data and calculate

        data = request.json
        # Corner case
        if not data:
            return make_response(
                jsonify({'error': 'Missing required JSON data'}), 400)
        # Check if required fields are present in the JSON data
        if not all(key in data for key in ['mesh', 'angle', 'axis']):
            return make_response(jsonify(
                {'error': 'Missing required fields in JSON data'}), 400)

        mesh = data.get('mesh')
        angle = data.get('angle')
        axis = data.get('axis')

        # Check if mesh or angle or axis is missing
        if not mesh:
            return make_response(jsonify({'error': 'No mesh provided'}), 400)
        if not angle:
            return make_response(jsonify({'error': 'No angle provided'}), 400)
        if not axis:
            return make_response(jsonify({'error': 'No axis provided'}), 400)

        # Convert to radian, use numpy to calculate rotation matrix
        angle_rad = np.radians(angle)

        if axis == 'X':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle_rad), -np.sin(angle_rad)],
                [0, np.sin(angle_rad), np.cos(angle_rad)]
            ])
        elif axis == 'Y':
            rotation_matrix = np.array([
                [np.cos(angle_rad), 0, np.sin(angle_rad)],
                [0, 1, 0],
                [-np.sin(angle_rad), 0, np.cos(angle_rad)]
            ])
        elif axis == 'Z':
            rotation_matrix = np.array([
                [np.cos(angle_rad), -np.sin(angle_rad), 0],
                [np.sin(angle_rad), np.cos(angle_rad), 0],
                [0, 0, 1]
            ])
        else:  # If axis is not valid
            return make_response(jsonify(
                {'error': "Invalid axis. Please specify 'X', 'Y', or 'Z'"}),
                400)

        mesh_array = np.array(mesh)
        mesh_rotated = np.dot(mesh_array, rotation_matrix)
        return jsonify({'mesh': mesh_rotated.tolist()})


############################################################
# Problem 3. Move 3d Mesh
# Given a 3D mesh as an input,
# Move the mesh in 3D Space by a, b and c units
# along X, Y and Z axis respectively.
# POST request, on the terminal type:
# curl -X POST -H "Content-Type: application/json" -d
# '{"mesh": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "x": 30, "y": 20, "z": 25}'
# http://127.0.0.1:5000/move_3d_mesh
############################################################

class Move3dMesh(Resource):

    def post(self):  # retrieving data and calculate
        data = request.json
        # Corner case
        if not data:
            return make_response(
                jsonify({'error': 'Missing required JSON data'}), 400)

        mesh = data.get('mesh')
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        mesh_moved = []

        # Check if mesh or x or y or z are missing
        if not all(key in data for key in ['mesh', 'x', 'y', 'z']):
            # Return a JSON response with an error message and status code 400
            return make_response(
                jsonify({'error': 'Missing required fields in JSON data'}),
                400)

        # Traverse mesh, move the point one by one
        for point in mesh:
            cur_x, cur_y, cur_z = point
            new_x = x + cur_x
            new_y = y + cur_y
            new_z = z + cur_z
            mesh_moved.append([new_x, new_y, new_z])

        return jsonify({'mesh': mesh_moved})


############################################################
# Problem 4. Check Polygon
# Given a polygon in a 3D space represented by 3D Points,
# check whether the polygon is convex.
# POST request, on the terminal type:
# curl -X POST -H "Content-Type: application/json" -d
# '{"polygon": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0.5, 1.5, 0], [0, 1, 0]]}'
# http://127.0.0.1:5000/check_polygon
############################################################


class CheckPolygon(Resource):
    # Calculate the cross product of vectors AB and AC.
    def cross_product(self, a, b, c):
        ab = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
        ac = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]

        return [
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0]
        ]

    def post(self):  # retrieving data and calculate
        data = request.json
        # Corner case
        if not data:
            return make_response(
                jsonify({'error': 'Missing required JSON data'}), 400)
        if not data['polygon']:
            return make_response(jsonify(
                {'error': 'Missing required fields in JSON data'}), 400)

        polygon = data.get('polygon')

        # Check if polygon is valid or not
        num_points = len(polygon)
        if num_points < 3:
            return make_response(
                jsonify({'message': 'False: polygon must have at least 3 '
                                    'vertices to be considered convex'}), 400)

        # Iterate over each set of three consecutive vertices
        reference_vector = None
        for i in range(num_points):
            a, b, c = polygon[i], polygon[(i + 1) % num_points], polygon[
                (i + 2) % num_points]
            cross = self.cross_product(a, b, c)
            # Determine the direction of the cross product
            if reference_vector is None:
                reference_vector = cross
            elif (cross[0] * reference_vector[0] < 0) or (
                    cross[1] * reference_vector[1] < 0) or (
                    cross[2] * reference_vector[2] < 0):
                # If cross product changes direction, the polygon is concave
                return jsonify({'message': 'False'})

        return jsonify({'message': 'True'})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(SmallestBoundingSquare, '/smallest_bounding_square')
api.add_resource(Rotate3dMesh, '/rotate_3d_mesh')
api.add_resource(Move3dMesh, '/move_3d_mesh')
api.add_resource(CheckPolygon, '/check_polygon')

# driver function
if __name__ == '__main__':
    app.run(debug=True)

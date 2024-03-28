import unittest
import json
from geometry import app


class GeometryTest(unittest.TestCase):

    def setUp(self):
        #  returns a test client object that allows you to send HTTP requests
        #  (such as GET, POST, PUT, DELETE) to your Flask routes and endpoints
        #  without actually running a server.
        self.app = app.test_client()

    def test_smallest_bounding_square(self):
        # Test Case 1
        input_data = {"points": [[-1, 2, 3], [0, 5, 6], [7, 8, 9]]}
        response = self.app.post('/smallest_bounding_square', json=input_data)
        response_data = json.loads(response.data)
        expected_mesh = {"depth": 6,
                         "height": 6,
                         "max_x": 7,
                         "max_y": 8,
                         "max_z": 9,
                         "min_x": -1,
                         "min_y": 2,
                         "min_z": 3,
                         "width": 8
                         }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 2
        input_data_2 = {"points": [[0, 1, 2], [1, 2, 3], [2, 3, 4]]}
        response = self.app.post('/smallest_bounding_square',
                                 json=input_data_2)
        response_data = json.loads(response.data)
        expected_mesh = {"width": 2,
                         "height": 2,
                         "depth": 2,
                         "max_x": 2,
                         "max_y": 3,
                         "max_z": 4,
                         "min_x": 0,
                         "min_y": 1,
                         "min_z": 2,
                         }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 3: empty points
        input_data_3 = {"points": []}
        response = self.app.post('/smallest_bounding_square',
                                 json=input_data_3)
        response_data = json.loads(response.data)
        expected_mesh = {'error': 'Missing points data'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 4: empty JSON
        input_data_4 = {}
        response = self.app.post('/smallest_bounding_square',
                                 json=input_data_4)
        response_data = json.loads(response.data)
        expected_mesh = {'error': 'Missing required JSON data'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

    def test_rotate_3d_mesh(self):
        # Test Case 1
        input_data = {"mesh": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                      "angle": 30, "axis": "Y"}
        response = self.app.post('/rotate_3d_mesh', json=input_data)
        response_data = json.loads(response.data)
        expected_mesh = {
            "mesh": [
                [
                    -0.6339745962155612,
                    2.0,
                    3.098076211353316
                ],
                [
                    0.46410161513775516,
                    5.0,
                    7.196152422706632
                ],
                [
                    1.5621778264910717,
                    8.0,
                    11.294228634059948
                ]
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 2
        input_data_2 = {
            "mesh": [[1, 0, 0], [0, 0, 1], [0, 1, 1]], "angle": 30, "axis": "X"
        }
        response = self.app.post('/rotate_3d_mesh',
                                 json=input_data_2)
        response_data = json.loads(response.data)
        expected_mesh = {
            "mesh": [
                [
                    1.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.49999999999999994,
                    0.8660254037844387
                ],
                [
                    0.0,
                    1.3660254037844386,
                    0.36602540378443876
                ]
            ]

        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 3: invalid axis
        input_data_3 = {
            "mesh": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "angle": 30, "axis": "K"
        }
        response = self.app.post('/rotate_3d_mesh',
                                 json=input_data_3)
        response_data = json.loads(response.data)
        expected_mesh = {
            "error": "Invalid axis. Please specify 'X', 'Y', or 'Z'"
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 4: missing angle, missing axis
        input_data_4 = {
            "mesh": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        }
        response = self.app.post('/rotate_3d_mesh',
                                 json=input_data_4)
        response_data = json.loads(response.data)
        expected_mesh = {
            "error": "Missing required fields in JSON data"
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 5: missing JSON
        input_data_5 = {}
        response = self.app.post('/rotate_3d_mesh',
                                 json=input_data_5)
        response_data = json.loads(response.data)
        expected_mesh = {
            "error": "Missing required JSON data"
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

    def test_move_3d_mesh(self):
        # Test Case 1
        input_data = {
            'mesh': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            'x': 10,
            'y': 20,
            'z': 30
        }
        response = self.app.post('/move_3d_mesh', json=input_data)
        response_data = json.loads(response.data)
        expected_mesh = [[11, 22, 33], [14, 25, 36], [17, 28, 39]]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['mesh'], expected_mesh)

        # Test Case 2
        input_data_2 = {
            'mesh': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            'x': -10,
            'y': -20,
            'z': -30
        }
        response = self.app.post('/move_3d_mesh', json=input_data_2)
        response_data = json.loads(response.data)
        expected_mesh = [[-9, -18, -27], [-6, -15, -24], [-3, -12, -21]]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['mesh'], expected_mesh)

        # Test Case 3: empty mesh
        input_data_3 = {
            'x': -10,
            'y': -20,
            'z': -30
        }
        response = self.app.post('/move_3d_mesh', json=input_data_3)
        response_data = json.loads(response.data)
        expected_mesh = {'error': 'Missing required fields in JSON data'}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 4: empty z
        input_data_4 = {
            "mesh": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            'x': -10,
            'y': -20,
        }
        response = self.app.post('/move_3d_mesh', json=input_data_4)
        response_data = json.loads(response.data)
        expected_mesh = {'error': 'Missing required fields in JSON data'}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

        # Test Case 5: empty JSON
        input_data_5 = {}
        response = self.app.post('/move_3d_mesh', json=input_data_5)
        response_data = json.loads(response.data)
        expected_mesh = {'error': 'Missing required JSON data'}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)

    def test_check_polygon(self):
        # Test Case 1
        input_data = {
            "polygon": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0.5, 1.5, 0],
                        [0, 1, 0]]
        }
        response = self.app.post('/check_polygon', json=input_data)
        response_data = json.loads(response.data)
        expected_bol = "True"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], expected_bol)

        # Test Case 2
        input_data_2 = {
            "polygon": [[0, 0, 0], [2, 0, 0], [2, 1, 0], [1, 0.5, 0],
                        [2, 2, 0], [0, 2, 0]]
        }
        response = self.app.post('/check_polygon', json=input_data_2)
        response_data = json.loads(response.data)
        expected_bol = "False"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], expected_bol)

        # Test Case 3: invalid polygon
        input_data_3 = {
            "polygon": [[0, 0, 0]]
        }
        response = self.app.post('/check_polygon', json=input_data_3)
        response_data = json.loads(response.data)
        expected_bol = "False: polygon must have at least 3 vertices " \
                       "to be considered convex"

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'], expected_bol)

        # Test Case 4: empty polygon
        input_data_4 = {
            "polygon": []
        }
        response = self.app.post('/check_polygon', json=input_data_4)
        response_data = json.loads(response.data)
        expected_bol = {'error': 'Missing required fields in JSON data'}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_bol)

        # Test Case 5: empty JSON
        input_data_5 = {}
        response = self.app.post('/check_polygon', json=input_data_5)
        response_data = json.loads(response.data)
        expected_mesh = {'error': 'Missing required JSON data'}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, expected_mesh)


if __name__ == '__main__':
    unittest.main()

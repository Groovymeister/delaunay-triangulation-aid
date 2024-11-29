from flask import Flask, request, jsonify
from flask_cors import CORS 
import numpy as np
from scipy.spatial import Delaunay

import sys
import os

sys.path.append(os.path.abspath('..'))
from main import *

app = Flask(__name__)
# CORS(app)  
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

@app.route('/api/triangulate', methods=['POST'])
def triangulate():
    data = request.get_json()
    points = data.get('points', [])
    
    if not points:
        return jsonify({"error": "No points provided"}), 400
    # print(points)

    point_objects = []
    for point in points:
        x, y = point[0], point[1]
        point_objects.append(Point(float(x), float(y)))
        
    triangulation = delaunay(point_objects)
    print('not the algo')
    edge_lists = []
    for edge in triangulation:
        edge_lists.append([edge.p1.x, edge.p1.y, edge.p2.x, edge.p2.y])
    print("not the appending")
    return jsonify(list(edge_lists))

if __name__ == '__main__':
    app.run(debug=True)

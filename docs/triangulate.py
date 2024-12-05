from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from scipy.spatial import Delaunay
import os
import sys
from delaunay import delaunay, Point, Edge, return_steps
# sys.path.append(os.path.abspath('..'))
# from main import *
app = Flask(__name__)
CORS(app)

@app.route('/api/triangulate', methods=['POST'])
def triangulate():
    data = request.get_json()
    points_data = data.get('points', [])
    print(points_data)
    
    if not points_data:
        return jsonify({"error": "No points provided"}), 400

    points = [Point(p[0], p[1]) for p in points_data]

    triangulation = delaunay(points)

    triangles = [{"p1": {"x": edge.p1.x, "y": edge.p1.y}, 
                  "p2": {"x": edge.p2.x, "y": edge.p2.y}} for edge in triangulation]
    
    return jsonify(triangles=triangles)

@app.route('/api/step', methods=['POST'])
def step():
    data = request.get_json()
    points_data = data.get('points', [])
    print(points_data)
    
    if not points_data:
        return jsonify({"error": "No points provided"}), 400

    points = [Point(p[0], p[1]) for p in points_data]

    _, steps = return_steps(points)

    formatted_steps = []
    for step in steps:
        step_type = step[0]
        edges_data = step[1]

        if isinstance(edges_data, set):
            edges = [{"p1": {"x": edge.p1.x, "y": edge.p1.y}, 
                      "p2": {"x": edge.p2.x, "y": edge.p2.y}} for edge in edges_data]
        else:
            edges = [{"p1": {"x": edges_data.p1.x, "y": edges_data.p1.y}, 
                      "p2": {"x": edges_data.p2.x, "y": edges_data.p2.y}}]

        formatted_steps.append({
            "type": step_type,
            "edges": edges
        })

    print("Formatted Steps: ", formatted_steps)
    
    return jsonify(steps=formatted_steps)

    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

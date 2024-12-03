from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from scipy.spatial import Delaunay
import os
from delaunay import delaunay, Point, Edge

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

    triangulation, _ = delaunay(points)

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

    _, steps = delaunay(points)

    formatted_steps = []
    for step in steps:

        step_type = step[0]
        
        edges = [{"p1": {"x": edge.p1.x, "y": edge.p1.y}, 
                  "p2": {"x": edge.p2.x, "y": edge.p2.y}} for edge in step[1]]
    
        formatted_steps.append({
            "type": step_type,
            "edges": edges
        })

    print("Formatted Steps: ", formatted_steps)
    
    return jsonify(steps=formatted_steps)
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

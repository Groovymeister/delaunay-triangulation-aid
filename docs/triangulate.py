from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from scipy.spatial import Delaunay
import os
from utils import Point, Edge
from delaunay import delaunay

app = Flask(__name__)
CORS(app)

@app.route('/api/triangulate', methods=['POST'])
def triangulate():
    data = request.get_json()
    points_data = data.get('points', [])
    
    if not points_data:
        return jsonify({"error": "No points provided"}), 400

    points = [Point(p['x'], p['y']) for p in points_data]

    triangulation = delaunay(points)

    triangles = [{"p1": {"x": edge.p1.x, "y": edge.p1.y}, 
                  "p2": {"x": edge.p2.x, "y": edge.p2.y}} for edge in triangulation]

    return jsonify(triangles=triangles)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

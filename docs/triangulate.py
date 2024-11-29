from flask import Flask, request, jsonify
from flask_cors import CORS 
import numpy as np
from scipy.spatial import Delaunay
import os

app = Flask(__name__)
CORS(app, origins=["https://groovymeister.github.io/delaunay-triangulation-aid/"])

@app.route('/api/triangulate', methods=['POST'])
def triangulate():
    data = request.get_json()
    points = data.get('points', [])
    
    if not points:
        return jsonify({"error": "No points provided"}), 400

    points_array = np.array(points)
    triangulation = Delaunay(points_array)

    return jsonify(triangles=triangulation.simplices.tolist())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

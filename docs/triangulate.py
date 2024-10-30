from flask import Flask, request, jsonify
from flask_cors import CORS 
import numpy as np
from scipy.spatial import Delaunay

app = Flask(__name__)
CORS(app)  

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
    app.run(debug=True)

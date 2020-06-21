from flask import Flask, request, jsonify
import numpy as np
import time
from flask_cors import CORS
from main import sintetize
app = Flask(__name__)
CORS(app)

@app.route("/spectrum", methods=['GET'])
def spectrum():
  time, signal, fourierTransformA, frequencies = sintetize(amplitudeList = [1, 0.5, 0.2], frequencyList = [60, 120, 240])
  fourierTransformA *= 1

  time, signal, fourierTransformB, frequencies = sintetize(amplitudeList = [1, 0.5, 0.5], frequencyList = [60, 120, 181])
  fourierTransformB *= 1

  time, signal, fourierTransformC, frequencies = sintetize(amplitudeList = [1, 0.8, 0.2], frequencyList = [60, 120, 240])  
  fourierTransformC *= 1

  res = fourierTransformA + fourierTransformB + fourierTransformC

  res += np.random.uniform(0,0.02,len(res))
  return jsonify([list(frequencies), list(abs(res))])

@app.route("/train", methods=['POST'])
def train():
  regioes = request.get_json()
  return jsonify(regioes)


if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5000, debug=False)
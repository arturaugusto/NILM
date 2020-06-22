from flask import Flask, request, jsonify
import numpy as np
import time
from flask_cors import CORS
from main import sintetize, buildData, spectrumData, train
app = Flask(__name__)
CORS(app)

global model
global labelMap

try:
  model = keras.models.load_model('path/to/location')
except Exception as e:
  print('No model found')
  model = None

labelMap = None

@app.route("/spectrum", methods=['GET'])
def spectrum():
  global model
  global labelMap

  # Carga A
  time, signal, fourierTransformA, frequencies = sintetize(
    amplitudeList = [1, 0.5, 0.2],
    frequencyList = [60, 120, 240])
  fourierTransformA *= 1

  # Carga B
  time, signal, fourierTransformB, frequencies = sintetize(
    amplitudeList = [1, 0.5, 0.5],
    frequencyList = [60, 120, 181])
  fourierTransformB *= 0

  # Carga C
  time, signal, fourierTransformC, frequencies = sintetize(
    amplitudeList = [1, 0.8, 0.2],
    frequencyList = [60, 120, 240])  
  fourierTransformC *= 0

  spectrum = fourierTransformA + fourierTransformB + fourierTransformC
  spectrum += np.random.uniform(0,0.02,len(spectrum))
  spectrum = spectrum/max(abs(spectrum))


  # make predictions
  loadPrediction = []
  if model:
    prediction = model.predict(np.array([spectrum]))
    for i, score in enumerate(prediction[0]):
      if len(labelMap[i]) == 1:
        loadPrediction.append({'score': round(float(score), 6), 'load': labelMap[i]})

  loadPrediction = sorted(loadPrediction, key=lambda k: k['score'], reverse=True)
  print(loadPrediction)

  return jsonify({
    'freq':list(frequencies),
    'mag': list(abs(spectrum)),
    'imag': list(spectrum.imag),
    'real': list(spectrum.real),
    'prediction': loadPrediction
  })

@app.route("/trainState", methods=['POST'])
def trainState():
  global model
  global labelMap

  req = request.get_json()
  
  loads = [(x['loads'],
    np.array(x['state']['real']) + np.array(x['state']['imag'])*1j,) for x in req]

  data, labelMap, combinationCount = buildData(loads, noise = 0.0005, nVariation = 100)
  print(labelMap)

  trainingSpectrum, trainingLabels, testingSpectrum, testingLabels = spectrumData(data, trainingPct = 0.8)

  model = train(trainingSpectrum, trainingLabels, combinationCount)

  model.save('model.h5')
  
  testLoss, testAcc = model.evaluate(testingSpectrum, testingLabels, verbose=2)

  print('\nTest accuracy:', testAcc)


  return jsonify({})


if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5000, debug=True)
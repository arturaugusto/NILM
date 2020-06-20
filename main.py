import tensorflow as tf
from tensorflow import keras
#print(tf.__version__)
from scipy.signal import hann
import numpy as np
import matplotlib.pyplot as plotter
import random
import itertools


def sintetize(amplitudeList = [], frequencyList = []):
  samplingFrequency = 100
  samplingInterval = 1 / samplingFrequency
  beginTime = random.uniform(0, 1)
  endTime = beginTime + 10 
  time = np.arange(beginTime, endTime, samplingInterval)

  # sintetize signal
  signal = np.zeros(len(time))
  for a, f in zip(amplitudeList, frequencyList):
    signal += np.sin(2 * np.pi * f * time) * a
  
  # apply hanning window
  signal *=  hann(len(signal))
  
  # fft
  fourierTransform = np.fft.fft(signal)/len(signal)
  fourierTransform = fourierTransform[range(int(len(signal)/2))]
  tpCount = len(signal)
  values = np.arange(int(tpCount/2))
  timePeriod = tpCount/samplingFrequency
  frequencies = values/timePeriod

  #plot(time, signal, fourierTransform, frequencies)
  return time, signal, fourierTransform, frequencies

def plot(time, signal, fourierTransform, frequencies):
  figure, axis = plotter.subplots(2, 1)
  axis[0].plot(time, signal)
  axis[1].plot(frequencies, abs(fourierTransform))
  plotter.show()

def combineSpectrum(x, noise):
  labelStr = ''
  spectrumCombination = np.zeros(len(x[0][1]), dtype=np.complex_)
  for loadName, fourierTransform in x:
    labelStr += loadName
    spectrumCombination += fourierTransform
  spectrumCombination = spectrumCombination/(max(spectrumCombination))
  # add some noise
  spectrumCombination *= np.random.normal(1,noise,len(spectrumCombination))
  return labelStr, spectrumCombination

def buildData(loads, seed=445, noise=0.05, nVariation=10):
  # all possible combinations, by pairs, trios, quartets...
  combinations = list()
  combinationCount = 0
  # we must use integers to label the combinations for keras,
  # the `labelMap` maps the integer to the string identifier
  labelMap = dict()
  for r in range(1, len(loads)):
    for x in itertools.combinations(loads, r+1):
      labelInt = combinationCount
      combinationCount += 1
      
      # the `combineSpectrum` function combine the spectrum 
      # and add some noise, so we append multiple samples of the array
      for _i in range(nVariation):
        labelStr, spectrumCombination = combineSpectrum(x, noise)
        combinations.append((labelInt, spectrumCombination),)

      labelMap[labelInt] = labelStr      
  
  random.seed(seed)
  random.shuffle(combinations)
  
  return combinations, labelMap, combinationCount

def buildLoads(N=10, seed=735):
  random.seed(seed)
  loads = list()
  labelMap = dict()
  # create random loads with random features
  for i in range(N):
    # name the load
    loadName = chr(65+i)

    nFeatures = int(np.random.uniform(1,10))
    amplitudeList = np.random.uniform(1,10, nFeatures)
    frequencyList = np.random.uniform(1,10, nFeatures)

    time, signal, fourierTransform, frequencies = sintetize(amplitudeList = amplitudeList, frequencyList = frequencyList)
    loads.append((loadName, fourierTransform),)

  return loads

def spectrumData(data, trainingPct = 0.8):
  # split training and testing data
  dataLen = len(data)
  trainingPct = trainingPct
  testingPct = 1-trainingPct
  
  ti = int(trainingPct*dataLen)

  trainingData = data[0:ti]
  trainingLabels = np.array([x[0] for x in trainingData])
  trainingSpectrum = np.array([x[1] for x in trainingData])

  testingData = data[ti::]
  testingLabels = np.array([x[0] for x in testingData])
  testingSpectrum = np.array([x[1] for x in testingData])

  return trainingSpectrum, trainingLabels, testingSpectrum, testingLabels

def train(trainingSpectrum, trainingLabels, combinationCount):
  shape = trainingSpectrum[0].shape
  model = keras.Sequential([
    keras.layers.Flatten(input_shape=shape),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(combinationCount, activation='softmax')
  ])

  model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
  
  model.fit(trainingSpectrum, trainingLabels, epochs=10)

  return model

def main():
  # create N loads with random harmonics and random phase shifts
  loads = buildLoads(N = 10)
  
  # create combinations of resulting loads spectrum * nVariation,
  # multiplied by a noise
  data, labelMap, combinationCount = buildData(loads, noise = 0.05, nVariation = 100)

  # split training and testing data
  # the dataset is shuffled
  trainingSpectrum, trainingLabels, testingSpectrum, testingLabels = spectrumData(data, trainingPct = 0.2)

  # fit the model
  model = train(trainingSpectrum, trainingLabels, combinationCount)
  
  # evaluate the model
  testLoss, testAcc = model.evaluate(testingSpectrum, testingLabels, verbose=2)

  print('\nTest accuracy:', testAcc)


if __name__ == '__main__':
  main()
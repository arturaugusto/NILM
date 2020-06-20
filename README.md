# NILM

Nonintrusive load monitoring using TensorFlow.

The `main` function output:

```python
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
Train on 20260 samples
Epoch 1/10
20260/20260 [==============================] - 2s 82us/sample - loss: 3.8875 - accuracy: 0.1956
Epoch 2/10
20260/20260 [==============================] - 1s 71us/sample - loss: 1.4359 - accuracy: 0.4907
Epoch 3/10
20260/20260 [==============================] - 1s 69us/sample - loss: 0.9159 - accuracy: 0.6405
Epoch 4/10
20260/20260 [==============================] - 1s 69us/sample - loss: 0.6348 - accuracy: 0.7596
Epoch 5/10
20260/20260 [==============================] - 2s 76us/sample - loss: 0.4299 - accuracy: 0.8572
Epoch 6/10
20260/20260 [==============================] - 1s 66us/sample - loss: 0.2924 - accuracy: 0.9138
Epoch 7/10
20260/20260 [==============================] - 1s 66us/sample - loss: 0.2084 - accuracy: 0.9432
Epoch 8/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.1515 - accuracy: 0.9637
Epoch 9/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.1134 - accuracy: 0.9743
Epoch 10/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.0902 - accuracy: 0.9813
81040/81040 - 3s - loss: 0.0794 - accuracy: 0.9835

# evaluate the model
testLoss, testAcc = model.evaluate(testingSpectrum, testingLabels, verbose=2)
Test accuracy: 0.98348963
```
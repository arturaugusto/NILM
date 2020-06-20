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
20260/20260 [==============================] - 2s 81us/sample - loss: 3.7806 - accuracy: 0.2265
Epoch 2/10
20260/20260 [==============================] - 1s 68us/sample - loss: 1.2869 - accuracy: 0.5773
Epoch 3/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.7720 - accuracy: 0.7204
Epoch 4/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.5314 - accuracy: 0.8016
Epoch 5/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.3751 - accuracy: 0.8736
Epoch 6/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.2561 - accuracy: 0.9283
Epoch 7/10
20260/20260 [==============================] - 1s 67us/sample - loss: 0.1720 - accuracy: 0.9644
Epoch 8/10
20260/20260 [==============================] - 1s 68us/sample - loss: 0.1191 - accuracy: 0.9801
Epoch 9/10
20260/20260 [==============================] - 1s 69us/sample - loss: 0.0825 - accuracy: 0.9885
Epoch 10/10
20260/20260 [==============================] - 1s 68us/sample - loss: 0.0608 - accuracy: 0.9918
81040/81040 - 3s - loss: 0.0485 - accuracy: 0.9952

# evaluate the model
testLoss, testAcc = model.evaluate(testingSpectrum, testingLabels, verbose=2)
Test accuracy: 0.9952246
```
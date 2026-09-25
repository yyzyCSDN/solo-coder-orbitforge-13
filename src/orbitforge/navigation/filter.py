from __future__ import annotations
import math


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scalar_inverse(value):
    if abs(value) < 1e-15:
        raise ValueError('singular innovation variance')
    return 1.0 / value


class ScalarMeasurementEKF:
    def __init__(self, state, covariance):
        self.state = list(state)
        self.covariance = [list(row) for row in covariance]

    def predict(self, transition, process_noise):
        self.state = [sum(transition[i][j] * self.state[j] for j in range(len(self.state))) for i in range(len(self.state))]
        propagated = matmul(matmul(transition, self.covariance), transpose(transition))
        self.covariance = add(propagated, process_noise)

    def update(self, measurement, predicted, jacobian, variance):
        hp = [sum(jacobian[j] * self.covariance[j][k] for j in range(len(jacobian))) for k in range(len(jacobian))]
        innovation_variance = sum(hp[k] * jacobian[k] for k in range(len(jacobian))) + variance
        inv = scalar_inverse(innovation_variance)
        gain = [sum(self.covariance[i][j] * jacobian[j] for j in range(len(jacobian))) * inv for i in range(len(jacobian))]
        innovation = measurement - predicted
        self.state = [x + k * innovation for x, k in zip(self.state, gain)]
        n = len(self.state)
        update_matrix = [[(1.0 if i == j else 0.0) - gain[i] * jacobian[j] for j in range(n)] for i in range(n)]
        self.covariance = matmul(update_matrix, self.covariance)
        return innovation, innovation_variance

    def sigma(self):
        return [math.sqrt(max(0.0, self.covariance[i][i])) for i in range(len(self.state))]

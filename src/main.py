import numpy as np
import control as ct
import matplotlib.pyplot as plt

#parameters definition

M = 1 #mass of cart
m = 0.1 #mass of pendulum
l = 0.5 #length of pendulum
g = 9.81 #acceleration due to gravity

#state space representation
A = np.array([[0, 1, 0, 0],
              [0, 0, 7*g*m/(7*M+4*m), 0],
              [0, 0, 0, 1],
              [0, 0, -6*g*(m+M)/(l*(7*M+4*m)), 0]])
B = np.array([[0],  
              [7/(7*M+4*m)],
              [0],
              [-6/(l*(7*M+4*m))]])

C = np.array([0, 0, 1, 0])  # Output matrix (1x4)
D = np.array([0])          # Direct transmission matrix (1x1)

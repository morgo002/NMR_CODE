import pandas as pd
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

df = pd.read_csv('sine.csv')
data = np.array(df['1Hz'].values)

y = fft(data)

plt.figure(2)
plt.plot(np.abs(y))
plt.show()

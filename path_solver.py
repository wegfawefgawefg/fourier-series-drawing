'''

given a complex signal of n points, over the interval [0, 1]
compute the fourier series of the signal with m terms

'''

import json
import math
import numpy as np
import matplotlib.pyplot as plt

def convert_to_complex(path):
    '''
    ex:path = [[0, 0],[20, 13],[2, 5],[0, 0]]
    '''
    p = np.array(path)
    return p[:,0] + 1j * p[:,1]

def get_fourier_series(signal, m):
    series_coefs = np.zeros(2*m-1,dtype=complex)
    freqs = np.zeros(2*m -1)
    for i in range(m):
        t = np.arange(len(signal))/len(signal)   
        basis_elem = np.exp(-2j * math.pi * i * t)
        series_coefs[i] = np.sum(signal * basis_elem) / len(signal)
        if i != 0:
            series_coefs[m+i-1] = np.sum(signal * np.conj(basis_elem)) / len(signal)
            freqs[[i, m+i-1]] = i,-i

    return series_coefs,freqs

def test_fourier_series():
    n = 1000
    m = 1000
    signal = np.arange(n,dtype=complex)

    series_coefs,_ = get_fourier_series(signal, m)

    res = np.zeros_like(signal)
    for i in range(m):
        t = np.arange(len(signal))/len(signal)
        basis_elem =  np.exp(2j * math.pi * i * t)
        res += series_coefs[i] * basis_elem
    np.testing.assert_almost_equal(res, signal)


def main():
    with open('tpath.json') as f:
        path = json.load(f)
    print(f"number of points: {len(path)}")
    m = 200
    signal = convert_to_complex(path)
    f_coefs,freqs = get_fourier_series(signal, m)

    out_dump = {
        'angles'      :     np.angle(f_coefs[1:]).tolist(),
        'magnitudes'  :     np.abs(f_coefs[1:]).tolist(),
        'rotation_speeds':  freqs[1:].tolist(),
        'center'      :     [np.real(f_coefs[0]), np.imag(f_coefs[0])],
    }
    with open('fourier_series.json', 'w') as f:
        json.dump(out_dump, f)







if __name__ == "__main__":
    main()    


import numpy as np

class Calcs():
    def __init__(self, frequency_list, number_of_files):
        self.setup_frequency_modes(frequency_list,number_of_files)
        self.check_triplet_frequency()

    def setup_frequency_modes(self, frequency_list, number_of_files):
        self.frequencys_alphabetic_order = sorted(frequency_list, key=str)
        frequencys_alphabetic_order_size = len(self.frequencys_alphabetic_order)
        self.frequency_modes = np.zeros(frequencys_alphabetic_order_size * number_of_files)
        for i in range(number_of_files):
            for j in range(frequencys_alphabetic_order_size):
                index_from_frequency_mode = i * frequencys_alphabetic_order_size + j
                self.frequency_modes[index_from_frequency_mode] = self.frequencys_alphabetic_order[j]

    def check_triplet_frequency(self):
        self.sum_frequencys = []
        number_frequencys = len(self.frequency_modes)

        frequency_inverse = [1 / x for x in self.frequency_modes ]

        for i in range(number_frequencys - 2):
            for j in range(i + 1, number_frequencys - 1):
                for k in range(j + 1, number_frequencys):
                    if np.isclose((frequency_inverse[i] + frequency_inverse[j]),frequency_inverse[k], rtol=0.009, atol=0.0):
                        self.sum_frequencys.append((i,j,k))
                    elif np.isclose((frequency_inverse[i] + frequency_inverse[k]),frequency_inverse[j], rtol=0.009, atol=0.0):
                        self.sum_frequencys.append((i,k,j))
                    elif np.isclose((frequency_inverse[j] + frequency_inverse[k]),frequency_inverse[i], rtol=0.009, atol=0.0):
                        self.sum_frequencys.append((j,k,i))

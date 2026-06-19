import numpy as np

# Calculates and processes data to determine phase mismatch values.

class Calcs():
    def __init__(self, bases, betas, frequency_list, min_poling, sweep_points, number_of_files):        
        self.frequency_list = frequency_list
        self.number_of_files = number_of_files
        self.sweep_points = sweep_points

        self.bases = bases
        self.betas = betas

        self.tolerance = (2*np.pi)/min_poling

        self.setup_frequencies_modes()
        self.calculate_sum_triplet_frequency()
        self.filtered_bases = self.filter_data(bases)
        self.filtered_betas = self.filter_data(betas)

        self.calculate_phase_mismatch()

    def setup_frequencies_modes(self):
        # Computes the frequencies_modes vector by sorting the user-provided frequencies in ascending order
        # and repeating them according to the number of files.

        self.frequencies_ascending_order = sorted(self.frequency_list, key=int)
        frequencies_ascending_order_size = len(self.frequencies_ascending_order)
        
        self.frequencies_modes = np.zeros(frequencies_ascending_order_size * self.number_of_files)
        
        for i in range(self.number_of_files):
            for j in range(frequencies_ascending_order_size):
                index_from_frequencies_mode = i * frequencies_ascending_order_size + j
                self.frequencies_modes[index_from_frequencies_mode] = self.frequencies_ascending_order[j]

    def calculate_sum_triplet_frequency(self):
        # Calculates the sum_frequencies vector by identifying which inverse frequencies (1/frequencies)
        # form a valid triplet sum.

        self.sum_frequencies = []
        number_frequencies = len(self.frequencies_modes)

        frequencies_inverse = [1 / x for x in self.frequencies_modes ]

        for i in range(number_frequencies - 2):
            for j in range(i + 1, number_frequencies - 1):
                for k in range(j + 1, number_frequencies):
                    if np.isclose((frequencies_inverse[i] + frequencies_inverse[j]),frequencies_inverse[k], rtol=0.009, atol=0.0):
                        self.sum_frequencies.append((i,j,k))
                    elif np.isclose((frequencies_inverse[i] + frequencies_inverse[k]),frequencies_inverse[j], rtol=0.009, atol=0.0):
                        self.sum_frequencies.append((i,k,j))
                    elif np.isclose((frequencies_inverse[j] + frequencies_inverse[k]),frequencies_inverse[i], rtol=0.009, atol=0.0):
                        self.sum_frequencies.append((j,k,i))

    def filter_data(self, data):  
        # Filters the vector data by dividing it into chunks based on the frequency count, then
        # appending them sequentially for each file.
        # Args:
        #   data: vector of data
        # Return:
        #   filtered_data: vector of data filtered.
        list_data_in_chunk = []

        for file in range(self.number_of_files):
            chunk_size = len(self.frequency_list)
            
            # Method to separate a list into chunks of size chunks_size.
            data_chunks = [data[file][i: i + chunk_size ] for i in range(0,len(data[file]), chunk_size)]
            list_data_in_chunk.append(data_chunks)

        filtered_data = []

        for sweep in range(self.sweep_points-1):
            union_chunk_data = []
            for file in range(self.number_of_files):
                union_chunk_data.extend(list_data_in_chunk[file][sweep])
            filtered_data.append(union_chunk_data)
        
        return filtered_data
        

    def calculate_phase_mismatch(self):
        # Calculates the mismatch values and poling conditions by extracting indices from sum_frequencies,
        # removing degeneracy, and summing the corresponding values in filteredbeta for each base.
        # Finally, it checks if these sums match within a specified tolerance.

        # Saves the resulst in a dict

        self.results = {
            "parameter_value" : [],
            "triplet_sum" : [],
            "values" : [],
            "mismatch" : [],
            "poling" : []
        }

        for base in range(len(self.filtered_bases)):
            for freq_one,freq_two,target_freq in self.sum_frequencies:

                if freq_one == freq_two or freq_one == target_freq or freq_two == target_freq:
                    continue
                
                sum = self.filtered_betas[base][freq_one] + self.filtered_betas[base][freq_two]
                target_value = self.filtered_betas[base][target_freq]
                
                if np.isclose(sum,target_value,atol=self.tolerance):
                    mismatch = sum - target_value
                    poling = (2 * np.pi)/mismatch
                    #print(f"For parameter {np.round(self.filtered_bases[base][0])}: curve {freq_one} + curve {freq_two} ≈ curve {target_freq}")
                    #print(f"Values: {self.filtered_betas[base][freq_one]} + {self.filtered_betas[base][freq_two]} ≈ {self.filtered_betas[base][target_freq]}")
                    #print(f"Mismatch: {mismatch}")
                    #print(f"Poling: {poling}")
                    #print("\n")
                    self.results["parameter_value"].append(np.round(self.filtered_bases[base][0]))
                    self.results["triplet_sum"].append((freq_one,freq_two,target_freq)) 
                    self.results["values"].append((self.filtered_betas[base][freq_one], self.filtered_betas[base][freq_two], self.filtered_betas[base][target_freq]))
                    self.results["mismatch"].append(mismatch)
                    self.results["poling"].append(poling)


            
                
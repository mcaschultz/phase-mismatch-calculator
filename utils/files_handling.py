import numpy as np

def read_data_txt(files_paths):
    bases = []
    betas = []

    for idx, file_path in enumerate(files_paths):
        col1, col2 = np.genfromtxt(file_path, comments="%", usecols=(0,1), unpack=True, skip_header=1)
        bases.append(col1 * 1000000000) 
        betas.append(col2)
    return bases, betas

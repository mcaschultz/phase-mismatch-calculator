import numpy as np

def read_data_txt(files_paths):
    # Read the comsol output files in .txt
    # Args:
    #   files_path: list of all the files paths
    # Return:
    #   bases: list of the bases of all the files
    #   betas: list of the betas of all the files.

    bases = []
    betas = []

    for file_path in files_paths:
        col1, col2 = np.genfromtxt(file_path, comments="%", usecols=(0,1), unpack=True, skip_header=1)
        bases.append(col1 * 1000000000) 
        betas.append(col2)
    return bases, betas

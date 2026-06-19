import utils

files_paths = [r"data/etch_h600nm_3_b1500nm.txt", r"data\etch_h600nm_4_b1500nm.txt"]

freq = [780,787,970,1550,1570,1600,2592]
min_poling = 3.7e-6
sweep_points = 42

bases, betas = utils.files_handling.read_data_txt(files_paths)

calc = utils.Calcs(bases,betas,freq,min_poling,sweep_points, len(files_paths))

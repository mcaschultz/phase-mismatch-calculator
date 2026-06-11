def read_data_txt(path : str):
    with open(path, 'r') as data:
        geometric_param = []
        propagation_const = []
        for line in data:
            if line.startswith("%") != True:
                column = line.split()
                geometric_param.append(float(column[0]))
                propagation_const.append(float(column[1]))
    return geometric_param, propagation_const

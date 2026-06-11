import utils

path = r"data\etch_h900nm_b1500nm_3neff.txt"

x, beta = utils.read_data_txt(path)
# Frequencia por calculo, se aplica a todos os arquivos, sem tamanho maximo, em nanometros, valores inteiros
freq = [780,787,970,1550,1570,1600,2592]

calc = utils.Calcs(freq,3)
print(calc.frequency_modes)
print("\n")
print(calc.sum_frequencys)
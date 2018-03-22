import re

# for using with programa.pulp
def decode(line):
    line = re.sub(' ', '', line)
    if len(re.findall('#', line)) > 0:
        line = line[:line.index('#')]

    return line[:2], line[2:5], line[5:]

def bin2Int(bin_number):
    return int(bin_number, 2)

def int2StrBin(i):
    b_str = bin(i)
    return (("0" * (3 - (len(b_str) - 2))) + b_str[2:])

def process(instruction, val_1, val_2):
    instr_number = bin2Int(instruction)
    instr_type = instructions[instr_number]
    r = instr_type(val_1, val_2)

    if 0 < instr_number < 3:
        registradores[0] = r

def load(register, memory_pos):
    registradores[register] = dados[memory_pos]

def save(memory_pos, register):
    dados[memory_pos] = registradores[register]

def save_dados():
    with open('data.fiction', 'w+') as data:
        for i in dados:
            data.write(int2StrBin(i) + '\n')

def load_dados():
    try:
        data = open('data.fiction')

        for line in data:
            val = int(line, 2)
            dados.append(val)

        data.close()
    except:
        print('Erro abrindo o programa/dados')
        exit()

def print_state():
    print('Registradores:', registradores)
    print('Dados:', dados)

def execute(instruction, register_1, register_2):
    val_1, val_2 = bin2Int(register_1), bin2Int(register_2)
    process(instruction, val_1, val_2)

registradores = [0 for i in range(8)]
dados = []

instructions = [load,
                lambda n1, n2: registradores[n1] + registradores[n2],
                lambda n1, n2: registradores[n1] - registradores[n2],
                save]

def main():
    load_dados()
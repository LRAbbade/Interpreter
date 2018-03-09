import re

def decode(line):
    line = re.sub(' ', '', line)
    if len(re.findall('#', line)) > 0:
        line = line[:line.index('#')]

    return line[:2], line[2:5], line[5:]

def get_register(bin_number):
    return int(bin_number, 2)

def process(instruction, val_1, val_2):
    instr_number = int(instruction, 2)
    instr_type = instructions[instr_number]

    if 0 < instr_number < 3:
        val_1, val_2 = registradores[val_1], registradores[val_2]
        registradores[0] = instr_type(val_1, val_2)        # pos 0 eh a AC
    else:
        instr_type(val_1, val_2)

def load(register, memory_pos):
    registradores[register] = dados[memory_pos]

def save(memory_pos, register):
    dados[memory_pos] = registradores[register]

def save_dados():
    with open('data.fiction', 'w+') as data:
        for i in dados:
            b_str = bin(i)
            data.write(("0" * (3 - (len(b_str) - 2))) + b_str[2:] + '\n')

def print_state():
    print('Registradores:', registradores)
    print('Dados:', dados)

registradores = [0 for i in range(8)]
registradores[1] = 1

instructions = [load,
                lambda n1, n2: n1 + n2,
                lambda n1, n2: n1 - n2,
                save]

dados = []

try:
    program = open('programa.pulp')
    data = open('data.fiction')

    for line in data:
        val = int(line, 2)
        dados.append(val)

    data.close()
except:
    print('Erro abrindo o programa/dados')
    exit()

print_state()

for pc in program:
    instruction, register_1, register_2 = decode(pc)
    val_1, val_2 = get_register(register_1), get_register(register_2)
    process(instruction, val_1, val_2)
    print_state()

save_dados()
program.close()

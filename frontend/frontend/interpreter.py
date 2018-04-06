import re

# tamanho da memoria
memory_size = 8

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
    b_str = ("0" * (memory_size - (len(b_str) - 2))) + b_str[2:]
    return (b_str[-memory_size:])

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

def update_dados(new_dados):
    global dados
    dados = [bin2Int(i) for i in new_dados]

def get_dados():
    return dados

def get_registradores():
    return registradores

def load_dados():
    try:
        data = open('data.fiction')
        for i in data:
            dados.append(bin2Int(i))

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
                lambda n1, n2: ((registradores[n1] + registradores[n2]) & (2 ** memory_size - 1)),
                lambda n1, n2: ((registradores[n1] - registradores[n2]) % (2 ** memory_size)),
                save]

def main():
    load_dados()

def executar_programa():
    load_dados()

    print('Iniciando execução')
    print('Estado atual:')
    print_state()

    with open('programa.pulp') as pc:
        for line in pc:
            execute(*decode(line))

    save_dados()
    print('Terminado')
    print('Estado final:')
    print_state()

# descomentar para rodar pelo programa, deixar comentado para rodar pelo site
# executar_programa() 

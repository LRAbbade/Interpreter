import re

# tamanho da memoria
memory_size = 8
cache_size = 4

# for using with programa.pulp
def decode(line):
    line = re.sub(' ', '', line)
    if len(re.findall('#', line)) > 0:
        line = line[:line.index('#')]

    return line[:2], line[2:5], line[5:]

def bin2Int(bin_number):
    return int(bin_number, 2)

def int2StrBin(i, fill=memory_size):
    b_str = bin(i)
    b_str = ("0" * (fill - (len(b_str) - 2))) + b_str[2:]
    return (b_str[-memory_size:])

def process(instruction, val_1, val_2):
    instr_number = bin2Int(instruction)
    instr_type = instructions[instr_number]
    r = instr_type(val_1, val_2)

    if 0 < instr_number < 3:
        registradores[0] = r        # salva resultado na ALU
        invalidate_cache_for(0)

def invalidate_cache_for(pos):
    cache_pos = pos % cache_size
    if get_cache_pos_tag(cache_pos) == pos:
        cache[cache_pos] = '0' + cache[cache_pos][1:]

def load(register, memory_pos):
    registradores[register] = dados[memory_pos]
    invalidate_cache_for(register)

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

def get_cache():
    return cache

def get_cache_decimal():
    return [[i[0], bin2Int(i[1:4]), bin2Int(i[4:])] for i in cache]

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
    print(' $ Estado Atual:')
    print(' $ Registradores:', registradores)
    print(' $ Dados:', dados)
    print(' $ Cache:', cache)

def execute(instruction, register_1, register_2):
    val_1, val_2 = bin2Int(register_1), bin2Int(register_2)
    process(instruction, val_1, val_2)

def get_val_from_cache_pos(cache_pos):
    return bin2Int(cache[cache_pos][4:])

def fetch_to_cache(memory_pos):
    aux = '1'         # valid bit
    aux += int2StrBin(memory_pos, 3)         # TAG
    aux += int2StrBin(registradores[memory_pos])        # memory value
    cache[memory_pos % cache_size] = aux

def get_cache_pos_tag(cache_pos):
    return bin2Int(cache[cache_pos][1:4])

def check_cache_pos_valid(cache_pos):
    return int(cache[cache_pos][0])

def get_from_cache(memory_pos):
    cache_pos = memory_pos % cache_size
    if not check_cache_pos_valid(cache_pos) or get_cache_pos_tag(cache_pos) != memory_pos:
        print('[MISS] Cache miss for memory pos:', memory_pos)
        fetch_to_cache(memory_pos)
    else:
        print('[HIT] Cache hit for memory_pos:', memory_pos)

    return get_val_from_cache_pos(cache_pos)

def soma(n1, n2):
    val_1 = get_from_cache(n1)
    val_2 = get_from_cache(n2)
    return ((val_1 + val_2) & (2 ** memory_size - 1))

def sub(n1, n2):
    val_1 = get_from_cache(n1)
    val_2 = get_from_cache(n2)
    return ((val_1 - val_2) % (2 ** memory_size))

registradores = [0 for i in range(8)]
cache = ["0" * 12] * cache_size             # 12 = 1 (valido) + 3 (tag) + 8 (memory)
dados = []
instructions = [load, soma, sub, save]

def main():
    load_dados()

def executar_programa():
    load_dados()

    print('Iniciando execução')
    print('Estado atual:')

    with open('programa.pulp') as pc:
        for line in pc:
            print_state()
            execute(*decode(line))

    save_dados()
    print('Terminado')
    print('Estado final:')
    print_state()

# descomentar para rodar pelo programa, deixar comentado para rodar pelo site
# executar_programa()

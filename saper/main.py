import random
from random import choice


def get_number(position, alls, prints):
    x = position[0]
    y = position[1]
    pos_to_check = [
        (x-1, y),
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1),
        (x+1, y),
        (x+1, y-1),
        (x, y-1),
        (x-1, y-1)
    ]
    num = 0
    for xy, act in alls.items():
        if (xy[0], xy[1]) in pos_to_check and alls[(xy[0], xy[1])] == "b":
            num += 1
    return num


def print_nums(position, alls, prints):
    x = position[0]
    y = position[1]
    pos_to_check = [
        (x - 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
        (x + 1, y),
        (x + 1, y - 1),
        (x, y - 1),
        (x - 1, y - 1)
    ]
    for xy in pos_to_check:
        if (xy[0], xy[1]) in alls.keys() and alls[(xy[0], xy[1])] != "b":
            prints[(xy[0], xy[1])] = f"{get_number((xy[0], xy[1]), alls, prints)}"
    write_prints(prints)

def print_field(N, prints, positions):
    row = "|"
    first_row = "  |"
    for i in range(1, N+1):
        first_row += str(i) + "|"
    field = first_row + "\n"
    for i in range(N):
        row += str(i + 1) + "|"
        for j in range(N):
            num = get_number((j, i), positions, prints)
            if positions[(j, i)] == "o":
                row += f"{num}|"
                prints[(j, i)] = num
                write_prints(prints)
                print_nums((j, i), positions, prints)
            else:
                row += f"{prints[(j, i)]}|"
        row += "\n"
        field += row
        row = "|"
    print(field)


def get_n():
    N = None
    N_bombs = None
    try:
        with open("n.txt", "r") as file:
            for line in file:
                N = int(line.split()[0])
                N_bombs = int(line.split()[1])
    except FileNotFoundError:
        with open("n.txt", "w") as file:
            pass
    return N, N_bombs

def write_n(N, N_bombs):
    with open("n.txt", "w") as file:
        file.write(f"{N} {N_bombs}\n")


def del_n():
    with open("n.txt", "w") as file:
        pass


def get_bombs():
    code = "231"
    positions = {}
    try:
        with open("bombs.txt", "r") as file:
            for line in file:
                pos = line.split()
                x = int(pos[0])
                y = int(pos[1])
                if pos[2] == code:
                    action = "b"
                else:
                    action = "*"
                positions[(x, y)] = action
    except FileNotFoundError:
        with open("bombs.txt", "w") as file:
            pass
    return positions


def write_bombs(positions):
    arr = ["123", "132", "213", "312", "321"]
    code = "231"
    with open("bombs.txt", "w") as file:
        for k, v in positions.items():
            if v == "b":
                file.write(f"{k[0]} {k[1]} {code}\n")
            else:
                file.write(f"{k[0]} {k[1]} {choice(arr)}\n")


def del_bombs_xy():
    with open("bombs.txt", "w") as file:
        pass

def clear_bombs_xy():
    with open("bombs.txt", "w") as file:
        pass


def random_bomb_xy(N, N_bombs):
    positions = {}
    counter = 0
    for i in range(N):
        for j in range(N):
            positions[(j, i)] = "*"
    while True:
        x = int(random.randint(0, N - 1))
        y = int(random.randint(0, N - 1))
        if positions[(x, y)] == "b":
            continue
        else:
            positions[(x, y)] = "b"
            counter += 1
        if counter == N_bombs:
            break
    return positions

def get_bomb_positions(poss):
    res = []
    for k, v in poss.items():
        if v == "b":
            res.append(k)
    return res

def start_new_game(N, N_bombs):
    write_n(N, N_bombs)
    positions = random_bomb_xy(N, N_bombs)
    bomb_pos = get_bomb_positions(positions)
    prints = get_prints(N)
    write_bombs(positions)
    write_prints(prints)

    while True:
        counter, flagged = get_counter()
        #print(f"counter = {counter}, N_b = {N_bombs}, bombs = {bomb_pos}")
        if counter == N_bombs and set(flagged) == set(bomb_pos):
            print("WIN!")
            del_savings()
            return
        print_field(N, prints, positions)
        x, y, action = make_choice()
        if action == "Open" and positions[(x, y)] == "b":
            print("WASTED...")
            del_savings()
            return
        elif action == "Open":
            positions[(x, y)] = "o"
        if action == "Flag":
            if (x, y) in bomb_pos:
                flagged.append((x, y))
            prints[(x, y)] = "f"
            if (x, y) in bomb_pos:
                counter += 1
            write_counter(counter, flagged)
        write_prints(prints)



def continue_game():
    N, N_bombs = get_n()
    positions = get_bombs()
    bomb_pos = get_bomb_positions(positions)
    prints = get_prints(N)

    while True:
        counter, flagged = get_counter()
        if counter == N_bombs and set(flagged) == set(bomb_pos):
            print("WIN!")
            del_savings()
            return
        print_field(N, prints, positions)
        x, y, action = make_choice()
        if action == "Open" and positions[(x, y)] == "b":
            print("WASTED...")
            del_savings()
            return
        elif action == "Open":
            positions[(x, y)] = "o"
        if action == "Flag":
            if (x, y) in bomb_pos:
                flagged.append((x, y))
            prints[(x, y)] = "f"
            if (x, y) in bomb_pos:
                counter += 1
            write_counter(counter, flagged)

        write_prints(prints)


def make_choice():
    choice = input("X Y Action(Open or Flag): ").split()
    x = int(choice[0]) - 1
    y = int(choice[1]) - 1
    action = choice[2]
    return x, y, action

def get_prints(N):
    prints = {}
    try:
        with open("prints.txt", "r") as file:
            for line in file:
                choice = line.split()
                x = int(choice[0])
                y = int(choice[1])
                printing = choice[2]
                prints[(x, y)] = printing
    except FileNotFoundError:
        with open("prints.txt", "w") as file:
            pass

    if len(prints) == 0:
        for i in range(N):
            for j in range(N):
                prints[(j, i)] = "*"

    return prints


def write_prints(printings):
    with open("prints.txt", "w") as file:
        for k, v in printings.items():
            file.write(f"{k[0]} {k[1]} {v}\n")


def del_prints():
    with open("prints.txt", "w") as file:
        pass


def get_counter():
    countr = 0
    counters = []
    try:
        with open("counters.txt", "r") as file:
            flag = True
            for line in file:
                if flag:
                    countr = int(line)
                    flag = False
                    continue
                counter = line.split()
                x = int(counter[0])
                y = int(counter[1])
                counters.append((x, y))
    except FileNotFoundError:
        with open("counters.txt", "w") as file:
            pass
    return countr, counters


def write_counter(countr, counters):
    with open("counters.txt", "w") as file:
        file.write(f"{countr}\n")
        for k in counters:
            file.write(f"{k[0]} {k[1]}\n")


def del_counter():
    with open("counters.txt", "w") as file:
        pass


def del_savings():
    del_n()
    del_prints()
    del_bombs_xy()
    del_counter()


if __name__ == "__main__":
    N, N_bombs = get_n()
    if N is None:
        N = int(input("Введите размер поля N*N:\nN = "))
        N_bombs = int(input("Введите количество бомб N_b\nN_b = "))
        start_new_game(N, N_bombs)
    else:
        continue_game()

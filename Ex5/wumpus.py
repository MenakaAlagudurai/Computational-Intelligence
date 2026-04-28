import random

# ==============================
# SETUP ENVIRONMENT
# ==============================

def create_world():
    n = int(input("Enter number of rooms (>=4): "))
    if n < 4:
        print("Grid must be at least 4x4. Setting to 4.")
        n = 4

    world = {}
    sensors = {}
    cell_number = 1

    for i in range(1, n+1):
        for j in range(1, n+1):
            world[(i,j)] = {
                "number": cell_number,
                "wampus": False,
                "pit": False,
                "gold": False
            }
            sensors[(i,j)] = {
                "stench": False,
                "breeze": False,
                "glitter": False
            }
            cell_number += 1

    start = (1,1)

    # Place Wampus
    while True:
        wampus = (random.randint(1,n), random.randint(1,n))
        if wampus != start:
            world[wampus]["wampus"] = True
            break

    # Place Gold
    while True:
        gold = (random.randint(1,n), random.randint(1,n))
        if gold != start and not world[gold]["wampus"]:
            world[gold]["gold"] = True
            sensors[gold]["glitter"] = True
            break

    # 20% pits
    total_cells = n*n
    pit_count = int(0.2 * total_cells)
    placed = 0

    while placed < pit_count:
        pit = (random.randint(1,n), random.randint(1,n))
        if pit != start and not world[pit]["wampus"] and not world[pit]["gold"] and not world[pit]["pit"]:
            world[pit]["pit"] = True
            placed += 1

    # Configure Sensors
    for (i,j) in world:
        if world[(i,j)]["wampus"]:
            for adj in get_adjacent(i,j,n):
                sensors[adj]["stench"] = True

        if world[(i,j)]["pit"]:
            for adj in get_adjacent(i,j,n):
                sensors[adj]["breeze"] = True

    return n, world, sensors, start


def get_adjacent(i,j,n):
    adj = []
    if i > 1: adj.append((i-1,j))
    if i < n: adj.append((i+1,j))
    if j > 1: adj.append((i,j-1))
    if j < n: adj.append((i,j+1))
    return adj


# ==============================
# MOVEMENT FUNCTIONS
# ==============================

def turn_left(direction):
    dirs = ["UP","LEFT","DOWN","RIGHT"]
    return dirs[(dirs.index(direction)+1)%4]

def turn_right(direction):
    dirs = ["UP","RIGHT","DOWN","LEFT"]
    return dirs[(dirs.index(direction)+1)%4]

def move_forward(position, direction, n):
    x,y = position

    if direction == "UP":
        x -= 1
    elif direction == "DOWN":
        x += 1
    elif direction == "LEFT":
        y -= 1
    elif direction == "RIGHT":
        y += 1

    if x < 1 or x > n or y < 1 or y > n:
        print("BUMP! You hit a wall.")
        return position

    return (x,y)


# ==============================
# SHOOT FUNCTION (ONE ARROW)
# ==============================

def shoot_arrow(position, direction, world, n):
    x,y = position

    while True:
        if direction == "UP":
            x -= 1
        elif direction == "DOWN":
            x += 1
        elif direction == "LEFT":
            y -= 1
        elif direction == "RIGHT":
            y += 1

        if x < 1 or x > n or y < 1 or y > n:
            break

        if world[(x,y)]["wampus"]:
            world[(x,y)]["wampus"] = False
            print("SCREAM! Wampus died.")
            return True

    print("Arrow missed.")
    return False


# ==============================
# DISPLAY FUNCTION (SHOW AGENT)
# ==============================

def display_world(world, n, agent_pos):
    print("\nWorld Map:")
    for i in range(1,n+1):
        for j in range(1,n+1):
            if (i,j) == agent_pos:
                print("A", end=" ")
            elif world[(i,j)]["wampus"]:
                print("W", end=" ")
            elif world[(i,j)]["pit"]:
                print("P", end=" ")
            elif world[(i,j)]["gold"]:
                print("G", end=" ")
            else:
                print(".", end=" ")
        print()
    print()


# ==============================
# CLUE FUNCTION (Semi Automatic)
# ==============================

def next_cell_clue(position, direction, world, n):
    x,y = position

    if direction == "UP": x -= 1
    elif direction == "DOWN": x += 1
    elif direction == "LEFT": y -= 1
    elif direction == "RIGHT": y += 1

    if (x,y) in world:
        if world[(x,y)]["pit"]:
            print(" Warning: Next cell may have a PIT!")
        if world[(x,y)]["wampus"]:
            print(" Warning: Next cell may have WAMPUS!")


# ==============================
# GAME LOOP
# ==============================

def play_game():
    n, world, sensors, position = create_world()
    direction = "RIGHT"
    score = 100          # Initial score = 100
    game_over = False
    arrow_available = True

    while not game_over:

        display_world(world, n, position)

        print("Current Position:", position)
        print("Facing:", direction)
        print("Score:", score)

        # If score <= 0  Game Over
        if score <= 0:
            print(" Score reached 0. Game Over!")
            break

        if sensors[position]["stench"]:
            print("Stench detected!")
        if sensors[position]["breeze"]:
            print("Breeze detected!")
        if sensors[position]["glitter"]:
            print("Glitter detected!")

        next_cell_clue(position, direction, world, n)

        action = input("Action (forward, left, right, grab, shoot, exit): ").lower()

        if action == "forward":
            score -= 1          # -1 for every forward move
            position = move_forward(position, direction, n)

        elif action == "left":
            direction = turn_left(direction)

        elif action == "right":
            direction = turn_right(direction)

        elif action == "grab":
            if sensors[position]["glitter"]:
                print("Gold grabbed! You win!")
                game_over = True
            else:
                print("No gold here.")

        elif action == "shoot":
            if arrow_available:
                score -= 10
                shoot_arrow(position, direction, world, n)
                arrow_available = False
            else:
                print(" ERROR: No arrows left!")

        elif action == "exit":
            break

        # Death Conditions
        if world[position]["wampus"]:
            print("You were eaten by Wampus!")
            score -= 1000
            game_over = True
        if world[position]["pit"]:
            print("You fell into a Pit!")
            score -= 1000
            game_over = True

    print("\nGAME OVER")
    print("Final Score:", score)
# ==============================
# RUN GAME
# ==============================

play_game()
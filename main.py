import math
import heapq


# DUNGEON

# 0 = jalan
# 1 = obstacle

dungeon = [
    [0, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 0]
]

enemy = (0, 0)
player = (4, 6)

detection_range = 10


# CALCULATE DISTANCE

def calculate_distance(enemy, player):
    return math.sqrt(
        (player[0] - enemy[0]) ** 2 +
        (player[1] - enemy[1]) ** 2
    )


# FSM

def get_state(enemy, player):
    distance = calculate_distance(enemy, player)

    if distance <= detection_range:
        return "CHASE"

    return "IDLE"


# A* PATHFINDING

def get_neighbors(position):
    row, col = position

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if (
            0 <= new_row < len(dungeon)
            and 0 <= new_col < len(dungeon[0])
            and dungeon[new_row][new_col] == 0
        ):
            neighbors.append(
                (new_row, new_col)
            )

    return neighbors


def heuristic(current, goal):
    return (
        abs(current[0] - goal[0])
        + abs(current[1] - goal[1])
    )


def a_star(start, goal):

    open_set = [(0, start)]

    came_from = {}

    cost = {
        start: 0
    }

    while open_set:

        _, current = heapq.heappop(open_set)

        if current == goal:

            path = []

            while current != start:
                path.append(current)
                current = came_from[current]

            path.append(start)

            return path[::-1]

        for neighbor in get_neighbors(current):

            new_cost = cost[current] + 1

            if (
                neighbor not in cost
                or new_cost < cost[neighbor]
            ):

                cost[neighbor] = new_cost

                priority = (
                    new_cost
                    + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (priority, neighbor)
                )

                came_from[neighbor] = current

    return None


# MOVEMENT

def calculate_direction(current, target):
    return (
        target[0] - current[0],
        target[1] - current[1]
    )


def calculate_velocity(direction):
    return direction


def update_position(position, velocity):
    return (
        position[0] + velocity[0],
        position[1] + velocity[1]
    )


# MAIN

distance = calculate_distance(enemy, player)

print("Enemy position :", enemy)
print("Player position:", player)
print("Distance       :", round(distance, 2))


# FSM
state = get_state(enemy, player)

print("Enemy state     :", state)


if state == "CHASE":

    # A* mencari jalur menuju Player
    path = a_star(enemy, player)

    if path is None:

        print("Jalur menuju Player tidak ditemukan.")

    else:

        print("Path:", path)

        # Enemy mengikuti path
        for next_position in path[1:]:

            direction = calculate_direction(
                enemy,
                next_position
            )

            velocity = calculate_velocity(
                direction
            )

            enemy = update_position(
                enemy,
                velocity
            )

            print(
                "Enemy bergerak ke:",
                enemy
            )

        print("Enemy mencapai Player.")

else:

    print("Enemy tetap dalam STATE IDLE.")
import sys
import math
import time

# GLOBAL
previous_enemy_distance = None
boost_ready = True
previous_x = None
previous_y = None
previous_enemy_x = None
previous_enemy_y = None
second_round = False

# MEMORY OF PASSED CHECKPOINTS
checkpoints = []

def distance(x, y, next_checkpoint_x, next_checkpoint_y):
    return int(math.sqrt( math.pow(x-next_checkpoint_x, 2) + math.pow(y-next_checkpoint_y, 2) ))

def speed(x, y, previous_x, previous_y):
    return distance(x, y, previous_x, previous_y)

def to_radian(angle):
    return angle * (3.14/180)

def to_degree(angle):
    return int(angle * 180/3.14)

def brain3 (cumulative_enemy_speed, cumulative_speed, x, y, next_checkpoint_x, next_checkpoint_y, distance_to_checkpoint, distance_to_enemy, next_checkpoint_angle,opponent_x, opponent_y, distance_enemy_to_checkpoint):
    global boost_ready, previous_x, previous_y, second_round

    checkpoint_position = (next_checkpoint_x, next_checkpoint_y)

    if len(checkpoints)>1:
        if checkpoints[0] == checkpoint_position:
            second_round = True

    speed = 100
    r = cumulative_speed
    angle_correction = to_radian(next_checkpoint_angle)
    
    angle_me_and_checkpoint = math.atan2(x-next_checkpoint_x, y-next_checkpoint_y)  + angle_correction - 1.57079633

    next_checkpoint_x = int(r * math.cos(angle_me_and_checkpoint) + next_checkpoint_x)
    next_checkpoint_y = int(r * -math.sin(angle_me_and_checkpoint) + next_checkpoint_y)

    if checkpoint_position not in checkpoints:
        checkpoints.append(checkpoint_position)
    elif second_round:
        
        if distance_to_checkpoint < 900:
            next_checkpoint_index = checkpoints.index(checkpoint_position) + 1
            if (next_checkpoint_index > len(checkpoints)-1):
                next_checkpoint_index = 0
            # print(next_checkpoint_x, next_checkpoint_y, speed, "TEST" + str(next_checkpoint_index))

            next_checkpoint_x = checkpoints[next_checkpoint_index][0]
            next_checkpoint_y = checkpoints[next_checkpoint_index][1]

    if distance_to_checkpoint > 6000 and abs(next_checkpoint_angle) <3 and boost_ready:
        speed = "BOOST"
        boost_ready = False
    elif abs(next_checkpoint_angle) > 90:
        speed = 0
    elif distance_to_enemy < 1000 and distance_to_checkpoint < 3000 and distance_enemy_to_checkpoint - 300 < distance_to_checkpoint:
        speed = "SHIELD"

    log = "S: " + str(speed) + " A: " + str(next_checkpoint_angle) + " D: " + str(distance_to_checkpoint) + " r: " + str(r) + " ES: " + str(cumulative_enemy_speed)
    print(next_checkpoint_x, next_checkpoint_y, speed, log)

while True:
    ### INPUT
    input_list_one = input().split()
    input_list_two = input().split()
    
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input_list_one]
    opponent_x, opponent_y = [int(i) for i in input_list_two]

    ### DISTANCE
    distance_to_checkpoint = distance(x, y, next_checkpoint_x, next_checkpoint_y)
    distance_to_enemy = distance(x, y, opponent_x, opponent_y)
    distance_enemy_to_checkpoint = distance(opponent_x, opponent_y, next_checkpoint_x, next_checkpoint_y)

    ### ADD TO MEMORY <ON FIRST RUN>
    if (previous_enemy_distance == None):
        previous_enemy_distance = distance_to_enemy
    if (previous_x==None):
        previous_x = x
        previous_y = y
    if (previous_enemy_x==None):
        previous_enemy_x = opponent_x
        previous_enemy_y = opponent_y

    ### SPEED
    cumulative_speed = speed(x, y, previous_x, previous_y)
    cumulative_enemy_speed = speed(opponent_x, opponent_y, previous_enemy_x, previous_enemy_y)

    ### DECISION ENGINE
    brain3(cumulative_enemy_speed, cumulative_speed, x, y , next_checkpoint_x, next_checkpoint_y, distance_to_checkpoint, distance_to_enemy, next_checkpoint_angle, opponent_x, opponent_y, distance_enemy_to_checkpoint)
    
    ### ADD TO MEMORY
    previous_x = x
    previous_y = y
    previous_enemy_x = opponent_x
    previous_enemy_y = opponent_y
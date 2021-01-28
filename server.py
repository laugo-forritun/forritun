###########################################
#### HELPER FUNCTIONS                   ###
###########################################
def send(ID: number, n: number):
    """ Send `n` to client `ID` """
    radio.send_value(str(ID), n)

# Custom implementation of hashmap since python
# hashmap is borked in MicroBit
#
# map_init(n) - Initialize map of capacity n
# map_put(m, k, v) - In map m, put v at k
# map_get(m,k) - In map m, get value at k
#
# NOTE:
# The values returned on invalid keys is undefined
def map_hash(k: number, size: number):
    """
    Return hash of `k`, for a `size`-big container
    """
    return (k*BIG_PRIME) % (3*size)
def map_put(m: List[number], k: number, v: number):
    """ Put `v` at `k` in map `m` """
    hashed_key = map_hash(k,len(m))
    m[hashed_key] = v
def map_get(m: List[number], k: number):
    """ Get value at `k` in `m` """
    hashed_key = map_hash(k,len(m))
    return m[hashed_key]
def map_init(size: number):
    """ Initialize a map of size `size` """
    size += 1 # Off by 1 in size, otherwise
    _chunks = [[0]]
    while len(_chunks[len(_chunks)-1])*10 < size:
        _x = [0]; _x.pop()
        for _ in range(10):
            _x = _x+_chunks[len(_chunks)-1]
        _chunks.push(_x)
    _chunks.reverse()
    _a = [0]; _a.pop()
    for chunk in _chunks:
        while len(_a)+len(chunk) < size:
            _a = _a + chunk
    print("Initialized a map with size " + len(_a))
    return _a



def clear_contestant(contestant):
    """ Remove `contestant` as a client """
    for i in range(len(bits)):
        if bits[i] == contestant:
            bits.remove_at(i)
            break
    map_put(challenge_id, contestant, 0)
    map_put(progress, contestant, 0)
def send_win(contestant):
    """ Notify `contestant` that they won """
    radio.send_string("" + contestant + " WIN")
    clear_contestant(contestant)
    basic.show_icon(IconNames.HAPPY)
    basic.clear_screen()
def send_loss(contestant):
    """ Notify `contestant` that they lost """
    radio.send_string("" + contestant + " LOSS")
    clear_contestant(contestant)
    basic.show_icon(IconNames.SAD)
    basic.clear_screen()






def on_received_value(name, value):
    """ Message handling """
    ID = int(name)

    # Register contestant in `bits`,
    # and send challenge
    if ID not in bits:
        bits.push(ID)
        map_put(challenge_id, ID, value)
        map_put(progress, ID, 0)
        for x in challenges[value]:
            send(ID, x)
            pause(100)
        return

    # Increment progress, or terminate in loss
    challenge = map_get(challenge_id, ID)
    prog = map_get(progress, ID)
    answer = answers[challenge][prog]
    if abs(answer - value) < EPSILON:
        # Increment progress
        map_put(progress, ID, prog+1)
        led.plot(prog%5, prog/5)
    else:
        send_loss(ID)
        return

    # Check for completion
    prog = map_get(progress, ID)
    challenge = map_get(challenge_id, ID)
    answer_len = len(answers[challenge])
    if prog >= answer_len:
        send_win(ID)

    # Show packet transmission rate
    led.toggle(3,4)

radio.on_received_value(on_received_value)


# Show the server is running
def on_forever():
    """ Prove server is running """
    led.toggle(4,4)
    basic.pause(250)
forever(on_forever)



###########################################
### SETUP                               ###
###########################################
radio.set_group(1)

BIG_PRIME = 946290599
EPSILON = 0.01
DEFAULT_MAP_SIZE = 100

challenge_id = map_init(DEFAULT_MAP_SIZE)
progress = map_init(DEFAULT_MAP_SIZE)
bits: List[number] = []

###########################################
### EDIT THE CHALLENGE AND ANSWERS LIST ###
### TO FIT YOUR CHALLENGES              ###
###########################################
challenges: List[List[number]] = [
    [-1], # Challenge 0
    [-1], # Challenge 1
    [-1], # challenge 2
    [-1], # challenge 3
    [-1], # challenge 4
]
answers: List[List[number]] = [
    [-1], # answer 0
    [-1], # answer 1
    [-1], # answer 2
    [-1], # answer 3
    [-1], # answer 4
]

##########################################
### Helper functions for clients       ###
##########################################
""" Handle messages """
def on_received_value(ID_recv, n_recv):
    if int(ID_recv) == ID:
        queue.append(n_recv)
radio.on_received_value(on_received_value)
""" Write (send) `n` to server """
def write(n: number):
    radio.send_value(str(ID), n)
""" Blocking read from server """
def read():
    while len(queue) == 0:
        basic.pause(100)
    return queue.shift()
""" Win/lose handling """
def on_received_string(_s):
    _i = 0
    for c in _s:
        if c == ' ': break
        _i += 1
    if int(_s.substr(0,_i)) == ID:
        _s = _s.substr(_i+1, len(_s))
        if _s == "WIN":
            on_win()
        elif _s == "LOSS":
            on_loss()
        else: basic.show_icon(IconNames.CONFUSED)
radio.on_received_string(on_received_string)


ID = 0
queue: List[number] = []
queue = []
ID = randint(0, 1000000)
radio.set_group(1)



##########################################
### Functions for clients to implement ###
##########################################
""" Code handling a win scenario """
def on_win():
    # You code here
    basic.show_icon(IconNames.HAPPY)
""" Code handling a loss scenario """
def on_loss():
    # You code here
    basic.show_icon(IconNames.SAD)

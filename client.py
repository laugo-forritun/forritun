##########################################
### Helper functions for clients       ###
##########################################
def on_received_value(ID_recv, n_recv):
    """ Handle messages """
    if int(ID_recv) == ID:
        queue.append(n_recv)
radio.on_received_value(on_received_value)
def write(n: number):
    """ Write (send) `n` to server """
    radio.send_value(str(ID), n)
def read():
    """ Blocking read from server """
    while len(queue) == 0:
        basic.pause(100)
    return queue.shift()
def on_received_string(_s):
    """ Win/lose handling """
    _i = 0
    for c in _s:
        if c == ' ': break
        _i += 1
    if int(_s[:_i]) != ID: return
    _s = _s[_i+1:]
    if _s == "WIN":
        on_win()
    elif _s == "LOSS":
        on_loss()
    else: basic.show_icon(IconNames.CONFUSED)
radio.on_received_string(on_received_string)

# Required objects
radio.set_group(1)
queue: List[number] = []
ID = randint(0, 1000000)



##########################################
### Functions for clients to implement ###
##########################################
def on_win():
    """ Code handling a win scenario """
    # You code here
    basic.show_icon(IconNames.HAPPY)
def on_loss():
    """ Code handling a loss scenario """
    # You code here
    basic.show_icon(IconNames.SAD)

def on_forever():
    """ Main code, reading/writing and logic """
    # You code here
forever(on_forever)

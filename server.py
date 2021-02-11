###########################################
#### HELPER FUNCTIONS                   ###
###########################################
def send(ID: number, n: number):
    """ Send `n` to client `ID` """
    radio.send_value(str(ID), n)




def clear_contestant(contestant):
    """ Remove `contestant` as a client """
    global challenge, bit, progress
    challenge = -1
    bit = -1
    progress = -1
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
    global progress, challenge, bit
    ID = int(name)

    # Register contestant in `bits`,
    # and send challenge
    if bit == -1:
        led.toggle(1,0)
        bit = ID
    if ID != bit:
        # Only one bit allowed
        led.toggle(2,0)
        return

    # Select challenge
    if challenge == -1:
        led.toggle(3,0)
        challenge = value
        # Send all challenge numbers
        for x in challenges[challenge]:
            led.toggle(0,4)
            send(ID, x)
        return

    # Increment progress, or terminate in loss
    answer = answers[challenge][progress]
    if abs((answer ^ SECRET_KEY) - value) < EPSILON:
        # Increment progress
        led.plot_bar_graph(progress, len(challenges[challenge]))
        progress += 1
    else:
        send_loss(ID)
        return

    # Check for completion
    answer_len = len(answers[challenge])
    if progress >= answer_len:
        send_win(ID)

    # Show packet transmission rate
    led.toggle(3,4)




###########################################
### SETUP                               ###
###########################################
radio.set_group(1)

SECRET_KEY = 123456789
BIG_PRIME = 946290599
EPSILON = 0.01

challenge = -1
progress = -1
bit = -1

###########################################
### EDIT THE CHALLENGE AND ANSWERS LIST ###
### TO FIT YOUR CHALLENGES              ###
###########################################
challenges: List[List[number]] = [
    [ # Challenge 0
     50, # N
     2345, 6789, 124, 5876, 123, 4857, 6341, 587, 1304, 7613, 5497, 8013, 2457, 8960, 1874, 5601, 3422, 3456, 7890, 1245, 8760, 1234, 8576, 3410, 5871, 3047, 6135, 4978, 132, 4578, 9601, 8745, 6013, 4223, 4567, 8901, 2458, 7601, 2348, 5763, 4105, 8713, 476, 1354, 9780, 1324, 5789, 6018, 7456, 134,
    ],
    [ # Challenge 1
     50, # N
     2345, 6789, 124, 5876, 123, 4857, 6341, 587, 1304, 7613, 5497, 8013, 2457, 8960, 1874, 5601, 3422, 3456, 7890, 1245, 8760, 1234, 8576, 3410, 5871, 3047, 6135, 4978, 132, 4578, 9601, 8745, 6013, 4223, 4567, 8901, 2458, 7601, 2348, 5763, 4105, 8713, 476, 1354, 9780, 1324, 5789, 6018, 7456, 134,
    ],
    [ # Challenge 2
     20, # N
     2345, 6789, 124, 5876, 123, 4857, 6341, 587, 1304, 7613, 5497, 8013, 2457, 8960, 1874, 5601, 3422, 3456, 7890, 1245,
    ],
    [ # Challenge 3
     20, # N
     3554, 1502,
     7339, 6483,
     4855, 8800,
     5428, 2230,
     8838, 2153,
     732, 5237,
     8558, 7659,
     6406, 2557,
     3562, 9405,
     8573, 6180,
     2900, 1787,
     1699, 8387,
     5020, 2872,
     2873, 2603,
     872, 6036,
     5989, 8992,
     5933, 6830,
     2114, 6089,
     2509, 6637,
     1165, 5607,
    ],
    [ # Challenge 4
     20, # N
     3554, 1502,
     7339, 6483,
     4855, 8800,
     5428, 2230,
     8838, 2153,
     732, 5237,
     8558, 7659,
     6406, 2557,
     3562, 9405,
     8573, 6180,
     2900, 1787,
     1699, 8387,
     5020, 2872,
     2873, 2603,
     872, 6036,
     5989, 8992,
     5933, 6830,
     2114, 6089,
     2509, 6637,
     1165, 5607,
    ],
]
answers: List[List[number]] = [
    [ # answer 0
     452390407,
    ],
    [ # answer 1
     452380744,
    ],
    [ # answer 2
     452389558,
    ],
    [ # answer 3
     452380113,
     452383896,
     452389459,
     452386055,
     452389557,
     452385862,
     452389213,
     452383029,
     452390030,
     452389198,
     452379495,
     452389104,
     452385711,
     452379402,
     452386727,
     452389651,
     452383389,
     452386810,
     452383198,
     452386260,
    ],
    [ # answer 4
     447200207,
     404960834,
     410854035,
     441350859,
     466915525,
     449623743,
     421457353,
     437205213,
     453633521,
     434021799,
     448387951,
     439330330,
     439170579,
     444912800,
     447125523,
     432239507,
     412916389,
     439525857,
     436789242,
     445998088,
    ],
]


# Show the server is running
def on_forever():
    """ Prove server is running """
    if bit != -1:
        led.toggle(0,0)
    for _ in range(4):
        led.toggle(4,4)
        pause(50)
    basic.pause(400)

forever(on_forever)
radio.on_received_value(on_received_value)

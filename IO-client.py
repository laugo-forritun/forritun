def on_received_value(ID_recv, n_recv):
    if int(ID_recv) == ID:
        queue.append(n_recv)
def send(n: number):
    radio.send_value(str(ID), n)
def read():
    while len(queue) == 0:
        basic.pause(100)
    return queue.shift()


def on_forever():
    pass


radio.set_group(1)
queue: List[number] = []
ID = randint(0, 1000000)

basic.forever(on_forever)
radio.on_received_value(on_received_value)

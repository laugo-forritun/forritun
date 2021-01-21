def on_received_value(ID_recv, n_recv):
    queue.append([int(ID_recv), n_recv])
def send(n: number):
    radio.send_value("" + str(ID), n)
def read():
    global ID_queued, n_queued
    while True:
        i = 0
        while i <= len(queue) - 1:
            ID_queued = queue[i][0]
            n_queued = queue[i][1]
            if ID_queued == ID:
                queue.remove_at(i)
                return n_queued
            i += 1
        basic.pause(1000)


def on_forever():
    pass


n_queued = 0
ID_queued = 0
queue: List[List[number]] = []
ID = 0
radio.set_group(1)
ID = randint(0, 1000000)

basic.forever(on_forever)
radio.on_received_value(on_received_value)

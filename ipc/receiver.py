from multiprocessing import Queue

def receiver(queue):
    message = queue.get()
    print("Received message:", message)

if __name__ == '__main__':
    q = Queue(name='my_queue')
    receiver(q)

from multiprocessing import Queue

def sender(queue):
    message = "Hello, receiver!"
    queue.put(message)

if __name__ == '__main__':
    q = Queue(name='my_queue')
    sender(q)

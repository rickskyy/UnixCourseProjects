from multiprocessing import Process, Event, Queue, Lock
import time
import os


class ProcessManager:

    def start_scenario(self):
        main_to_1_event = Event()
        main_to_2_event = Event()
        lock = Lock()

        print("Creating channels K0 and K1")
        queue_k0 = Queue()
        queue_k1 = Queue()

        print("Starting process 1 ...")
        process1 = Process(target=self.process_1_task, args=(main_to_1_event, main_to_2_event, queue_k0, queue_k1, lock))
        process1.start()

        time.sleep(1)
        with lock:
            print("Main process ({}) sending signal to process 1 ({})".format(os.getpid(), process1.pid))
        main_to_1_event.set()

        process2_pid = queue_k0.get(block=True)
        with lock:
            print("Main process ({}) received Process 2 ({}) pid from Process 1".format(os.getpid(), process2_pid))
            print("Main process ({}) sending signal to Process 2".format(os.getpid()))

        main_to_2_event.set()

        message1 = queue_k0.get(block=True)
        with lock:
            print("Main process ({}) received message1: '{}' from channel K0".format(os.getpid(), message1))
        message2 = queue_k0.get(block=True)
        with lock:
            print("Main process ({}) received message2: '{}' from channel K0".format(os.getpid(), message2))

        with lock:
            print("Main process ({}) finished execution".format(os.getpid()))

    def process_1_task(self, main_to_1, main_to_2, queue0, queue1, lock):
        with lock:
            print("Process 1 with id {} has started".format(os.getpid()))

        p2_to_p1 = Event()

        with lock:
            print("Process 1 ({}) is starting Process 2".format(os.getpid()))
        process2 = Process(target=self.process_2_task, args=(main_to_2, p2_to_p1, queue0, queue1, lock))
        process2.start()

        main_to_1.wait()
        with lock:
            print("Process 1 ({}) received signal from Main process".format(os.getpid()))
            print("Process 1 ({}) is sending pid of the process 2 ({}) to main process".format(os.getpid(), process2.pid))

        queue0.put(process2.pid)

        p2_to_p1.wait()
        with lock:
            print("Process 1 ({}) received signal from Process 2".format(os.getpid()))

        message = queue1.get(block=True)
        with lock:
            print("Process 1 ({}) received message from channel K1".format(os.getpid()))
            print("Process 1 ({}) is putting message to channel K0".format(os.getpid()))

        queue0.put(message)

        with lock:
            print("Process 1 ({}) finished execution".format(os.getpid()))

    @classmethod
    def process_2_task(cls, main_to_2, p2_to_p1, queue0, queue1, lock):
        with lock:
            print("Process 2 ({}) has started".format(os.getpid()))

        main_to_2.wait()
        with lock:
            print("Process 2 ({}) received signal from Main process".format(os.getpid()))
            print("Process 2 ({}) is putting message to channel K0".format(os.getpid()))
        queue0.put("Hello from P2 put to K0")

        with lock:
            print("Process 2 ({}) is putting message to channel K1".format(os.getpid()))
        queue1.put("Hello from P2 put to K1")

        with lock:
            print("Process 2 ({}) is sending signal to Process 1".format(os.getpid()))
        p2_to_p1.set()

        with lock:
            print("Process 2 ({}) finished execution".format(os.getpid()))


if __name__ == "__main__":
    ProcessManager().start_scenario()

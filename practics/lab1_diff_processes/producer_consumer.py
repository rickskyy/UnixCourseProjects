from multiprocessing import Process, Lock
from multiprocessing.managers import SyncManager
import os
import time
import random
import itertools

START_INDEX = 0
PRODUCER_WAIT_TIME_WHEN_BUFFER_FULL = 0.2
MAX_RAND_INT = 100


# infinite generator of random int values
def random_int_generator():
    while True:
        yield random.randint(0, MAX_RAND_INT)


# infinite generator of consequent int values
def count_generator():
    return itertools.count(0, 1)


class Buffer:
    """
    Concurrent safe shared buffer
    """
    def __init__(self, buffer, consumers_number, lock):
        """
        :param buffer: reference to the proxy of shared list
        :param consumers_number: number of consumers
        :param lock: multiprocessing.Lock
        """
        self.buffer = buffer
        self.cnumber = consumers_number
        self._lock = lock

    def read_value(self, index, process_id):
        """
        Read value from the buffer by index if it has not been yet read.
        :param index: index of a list element
        :param process_id: id of the process who is attempting to read the value
        :return: value or None
        """
        with self._lock:
            # check if the process has already read the value
            if process_id not in self.buffer[index]['ids']:
                # create proxy to manipulate inner objects of a shared list object
                dict_proxy = self.buffer[index]
                dict_proxy['ids'].append(process_id)
                self.buffer[index] = dict_proxy
                print("Got --- Id: {id}, Value: {value}, Index: {index}, Buffer: {buffer}".format(
                    id=process_id,
                    value=self.buffer[index]['value'],
                    index=index,
                    buffer=self.buffer), end='\n\n')
                return self.buffer[index]['value']

    def put_value(self, index, value):
        """
        Put value to the buffer element with the specified index 
        if current value has been already read by all consumers.
        :param index: index of a list element 
        :param value: value to put
        :return: True if successfully put, otherwise False 
        """
        with self._lock:
            # create proxy to manipulate inner objects of a shared list object
            dict_proxy = self.buffer[index]
            if len(dict_proxy['ids']) > 0 and (dict_proxy['ids'][0] is None or len(dict_proxy['ids']) == self.cnumber):
                dict_proxy['ids'].clear()
                dict_proxy['value'] = value
                self.buffer[index] = dict_proxy
                print("Put --- Index: {index}, Value: {value}, Buffer {buffer}".format(
                    index=index,
                    value=value,
                    buffer=self.buffer), end='\n\n')
                return True
            return False

    def __str__(self):
        return str(self.buffer)


class ProcessManager:
    """
    ProcessManager class for initializing and starting consumers' and producer's processes
    """
    def __init__(self, consumers_number, buffer_size, csleep_time_list, psleep_time, values):
        """
        :param consumers_number: number of consumers in [2,10] range
        :param buffer_size: size of the buffer
        :param csleep_time_list: list containing sleeping times for consumer processes
        :param psleep_time: sleeping time of a producer
        :param values: iterable obj for providing values to the producer process
        """
        self.buffer_size = buffer_size

        if 2 <= consumers_number <= 10:
            self.consumers_number = consumers_number
        else:
            raise ValueError("Number of consumers should be in [2,10] range")

        if len(csleep_time_list) == consumers_number:
            self.csleep_time_list = csleep_time_list
        else:
            raise ValueError("List containing consumers sleeping time does not equal to provided number of consumers.\n"
                             "Length of the list: {consumers_list}, Consumers_number: {cnumber}".format(
                                consumers_list=len(csleep_time_list),
                                cnumber=len(self.consumers_number)))

        self.psleep_time = psleep_time

        self._producer = None
        self._consumers = []
        self._values = values

    @classmethod
    def _produce(cls, buffer, lock, sleep_time, values):
        """
        Produces random values and putting it to the buffer
        :param buffer: Buffer object
        :param lock: multiprocessing.Lock
        :param sleep_time: sleeping time of the process before producing next value
        :param values: iterable returning random numbers, generator by default
        """
        with lock:
            print('Starting producer => {}'.format(os.getpid()))

        buffer_size = len(buffer.buffer)
        current_buffer_index = START_INDEX

        for value in values:
            time.sleep(sleep_time)
            while True:
                with lock:
                    print("Putting value {value} to index {index} of {buffer}".format(
                        value=value,
                        index=current_buffer_index,
                        buffer=buffer))
                if buffer.put_value(current_buffer_index, value):
                    current_buffer_index = (current_buffer_index + 1) % buffer_size
                    break
                time.sleep(PRODUCER_WAIT_TIME_WHEN_BUFFER_FULL)

    @classmethod
    def _consume(cls, buffer, lock, sleep_time):
        """
        Consumes values from the buffer
        :param buffer: Buffer object
        :param lock: multiprocessing.Lock
        :param sleep_time: sleeping time of the process before consuming next value
        """
        with lock:
            print('Starting consumer => {}'.format(os.getpid()))

        buffer_size = len(buffer.buffer)
        current_buffer_index = START_INDEX

        while True:
            time.sleep(sleep_time)
            with lock:
                print("Process {id} getting value from index {index} of {buffer}: ".format(
                    id=os.getpid(),
                    index=current_buffer_index,
                    buffer=buffer))
            v = buffer.read_value(current_buffer_index, os.getpid())
            if v is not None:
                current_buffer_index = (current_buffer_index + 1) % buffer_size

    def _create_shared_container(self, manager):
        """
        Creates shared list with the structure:
        Example: [{'value': 23, 'ids': [5232, 5235, 5236]}, {'value': 24, 'ids': [5232]}]
                 Element of the buffer is represented as dict containing the value and 'ids' list.
                 'ids' list stores ids of the processes who has already read the value.
                 Producer rewrites only the element when the ids list contains initial None value
                 or length of the ids list equals to the number of the processes, meaning that every 
                 consumer process read the value.
        :param manager: SyncManager object
        :return: reference to the proxy of the shared list
        """
        return manager.list([manager.dict({'value': None, 'ids': manager.list([None])})] * self.buffer_size)

    def start(self):
        """
        Initialize and start producer's and consumers' processes
        """
        with SyncManager() as manager:
            lock = Lock()
            buffer = Buffer(self._create_shared_container(manager), self.consumers_number, lock)
            self._producer = Process(target=self._produce, args=(buffer, lock, self.psleep_time, self._values))
            self._consumers = map(lambda sleep: Process(target=self._consume, args=(buffer, lock, sleep)),
                                  self.csleep_time_list)

            for c in self._consumers:
                c.daemon = True
                c.start()

            self._producer.start()
            self._producer.join()


if __name__ == "__main__":
    ProcessManager(
        consumers_number=2,
        buffer_size=5,
        csleep_time_list=[2, 1],
        psleep_time=0.5,
        # possible to use count_generator(), producing consequent numbers
        values=random_int_generator()
    ).start()

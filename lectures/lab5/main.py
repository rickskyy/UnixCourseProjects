# Task: Calculate arcsin(x) while paralleling computational subtasks
#
#            inf            (2n)!
# arcsin x = sum ----------------------------- * x ^ 2n+1 (-1, 1)
#            n=0     4^n * (n!)^2 * (2n + 1)
#

import os
from multiprocessing import Process, Queue, Lock, Value
from multiprocessing.managers import SyncManager

INT_MAX = 100000
STEP_TO_CHECK = 4


def calculate_factorial(q1, q2, n, lock, finish_flag):
    q1.put(1)
    q2.put(1)
    curr = 1
    for i in range(1, 2*n+1):
        if i % STEP_TO_CHECK == 0:
            with lock:
                if finish_flag.value:
                    break
        curr *= i
        if i % 2 == 0:  # calculating (2n)!
            q1.put(curr)
            with lock:
                print("{id} putting {curr} to q_2n".format(id=os.getpid(), curr=curr))

        if i <= n:  # calculating n!
            q2.put(curr)
            with lock:
                print("{id} putting {curr} to q_n".format(id=os.getpid(), curr=curr))


def calculate_pow(q1, base, n, lock, finish_flag):
    q1.put(1)
    curr = 1
    for i in range(n+1):
        if i % STEP_TO_CHECK == 0:
            with lock:
                if finish_flag.value:
                    break
        curr *= base
        q1.put(curr)
        with lock:
            print("{id} putting {curr} to q_pow".format(id=os.getpid(), curr=curr))


def arcsin_calc(q_pow, q_2n, q_n, x, eps, n, lock, finish_flag):
    curr, next = 0, INT_MAX
    i = 0

    while abs(next - curr) > eps:
        next = curr
        val_2n = q_2n.get()  # (2n)!
        val_n = pow(q_n.get(), 2)  # (n!)^2
        val_pow = q_pow.get()  # 4^n
        val_linear = 2*i + 1
        curr += val_2n * pow(x, val_linear) / (val_pow * val_n * val_linear)
        with lock:
            print("Id: {id}, Val_2n: {val_2n}, Val_n: {val_n}, Val_pow: {val_pow}, Curr: {curr}, i:{i}".format(
                val_2n=val_2n, val_n=val_n, val_pow=val_pow, curr=curr, i=i, id=os.getpid()))
        if i > n:
            with lock:
                raise ValueError("Cannot find arcsin with given eps")
        i += 1

    with lock:
        finish_flag.value = True
    with lock:
        print("Id: {id}, Result: {curr}, i:{i}".format(id=os.getpid(), curr=curr, i=i))


class ProcessManager:
    def __init__(self):
        self._x = None
        self._eps = None
        self._max_iters = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if -1 < x < 1:
            self._x = x
        else:
            raise ValueError("x must be in range (-1, 1)")

    @property
    def eps(self):
        return self._eps

    @eps.setter
    def eps(self, eps):
        if eps >= 0:
            self._eps = eps
        else:
            raise ValueError("eps might have positive value")

    @property
    def max_iters(self):
        return self._max_iters

    @max_iters.setter
    def max_iters(self, val):
        if val > 0:
            self._max_iters = val
        else:
            raise ValueError("max number of iterations might have positive value")

    def start(self):
        with SyncManager():
            lock = Lock()
            q_pow, q_2n, q_n = Queue(), Queue(), Queue()
            finish_flag = Value('b', False)

            main_process = Process(target=arcsin_calc,
                                   args=(q_pow, q_2n, q_n, self.x, self.eps, self.max_iters, lock, finish_flag))
            factorial_process = Process(target=calculate_factorial,
                                        args=(q_2n, q_n, self.max_iters, lock, finish_flag))
            pow_process = Process(target=calculate_pow, args=(q_pow, 4, self.max_iters, lock, finish_flag))

            factorial_process.daemon = True
            factorial_process.start()

            pow_process.daemon = True
            pow_process.start()

            main_process.start()
            main_process.join()


if __name__ == "__main__":
    pm = ProcessManager()
    pm.x = 0.5
    pm.max_iters = 100
    pm.eps = 0.0001
    pm.start()

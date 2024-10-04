from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool


def multithreadizer(t_num: int = cpu_count()):
    def decorator(func):
        def wrapper(args: list, th_num: int = t_num):
            if not th_num:
                th_num = len(args)
            with ThreadPool(th_num) as thread_pool:
                ans = thread_pool.starmap(func, args)
            return ans

        return wrapper

    return decorator

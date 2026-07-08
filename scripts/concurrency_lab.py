import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generation.generator import generate_customers, generate_accounts, generate_normal_transactions


def cpu_bound_work(accounts, n):
    """Generating transactions is CPU-bound: pure Python object creation, no I/O."""
    return list(generate_normal_transactions(accounts, n))


def run_sequential(accounts, n, num_batches):
    start = time.perf_counter()
    for _ in range(num_batches):
        cpu_bound_work(accounts, n)
    return time.perf_counter() - start


def run_threaded(accounts, n, num_batches):
    from concurrent.futures import ThreadPoolExecutor

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_batches) as executor:
        futures = [executor.submit(cpu_bound_work, accounts, n) for _ in range(num_batches)]
        for f in futures:
            f.result()
    return time.perf_counter() - start


def run_multiprocess(accounts, n, num_batches):
    from concurrent.futures import ProcessPoolExecutor

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=num_batches) as executor:
        futures = [executor.submit(cpu_bound_work, accounts, n) for _ in range(num_batches)]
        for f in futures:
            f.result()
    return time.perf_counter() - start


if __name__ == "__main__":
    customers = list(generate_customers(200, seed=1))
    accounts = list(generate_accounts(customers))

    n_per_batch = 200_000
    num_batches = 4

    seq_time = run_sequential(accounts, n_per_batch, num_batches)
    print(f"Sequential:    {seq_time:.2f}s")

    thread_time = run_threaded(accounts, n_per_batch, num_batches)
    print(f"Threaded:      {thread_time:.2f}s")

    process_time = run_multiprocess(accounts, n_per_batch, num_batches)
    print(f"Multiprocess:  {process_time:.2f}s")
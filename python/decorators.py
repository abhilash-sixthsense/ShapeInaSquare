import time

# Dictionary to store function execution times and count
execution_times = {}


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        if func.__name__ in execution_times:
            execution_times[func.__name__] = (
                execution_times[func.__name__][0] + total_time,
                execution_times[func.__name__][1] + 1,
                total_time,
            )
        else:
            execution_times[func.__name__] = (total_time, 1, total_time)

        return result

    return wrapper


def print_measure_time():
    # Print the execution times
    sorted_data = sorted(execution_times.items(), key=lambda item: item[1][0])
    for function_name, execution_time in sorted_data[-4:]:
        print(
            f"{function_name:<35} took {execution_time[0]:.2f} seconds to run , total {execution_time[1]} times,"
            + f" average {execution_time[0]/execution_time[1]:.4f} seconds, last run {execution_time[2]:.4f} seconds"
        )

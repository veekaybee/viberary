import time

from knn_search import KNNSearch

from conf.config_manager import ConfigManager
from conf.redis_conn import RedisConnection

print(ConfigManager().set_logger_config())
retriever = KNNSearch(RedisConnection().conn(), ConfigManager())


def run_search():
    return retriever.vectorize_query("dog")


def measure_average_execution_time(num_calls):
    total_execution_time = 0

    for i in range(num_calls):
        start_time = time.time()
        run_search()
        end_time = time.time()
        total_execution_time += end_time - start_time

    average_execution_time = total_execution_time / num_calls
    return average_execution_time


if __name__ == "__main__":
    average_time = measure_average_execution_time(1000)
    print(f"Average execution time: {average_time:.6f} seconds")

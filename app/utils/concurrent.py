import concurrent.futures
import logging

logger = logging.getLogger("app")


def execute_functions_concurrently(functions_list, kwargs_list, workers_count=5, raise_exception=False):
    '''
        Gets list of functions along with list of kwargs for executing in concurrent manner along with
        max_workers_count for maximum threads to execute the functions.
        Note: Need to pass the variable which will be manipulated inside the kwargs for easier functioning of threads
        Example: def is_odd(num, output_list):
                    if num % 2 != 1:
                        output_list.append(True)
                    else:
                        output_list.append(False)
                output_list_test = []
                execute_functions_in_parallel([is_odd for _ in range(0,10)], [(dict(num=inp, output_list=output_list_test)) for inp in range(0,10)])
        Number of functions and number of input kwargs must be equal. But number of kwargs can be anything.
        The function will log error if raise exception is not passed or is False. Otherwise, the function will
        throw an error and stop the thread.
    '''
    workers_count = min(workers_count, 5)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_count) as executor:
        future_to_function = {
            executor.submit(functions_list[index], **kwargs_list[index]): index for index in range(len(functions_list))
        }
        for future in concurrent.futures.as_completed(future_to_function):
            index = future_to_function[future]
            try:
                yield {index: future.result()}
            except Exception as exc:
                logger.info(f'{index} generated an exception: {exc}')
                if raise_exception:
                    raise exc

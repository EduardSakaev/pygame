import time


class DelayedCall:
    def __init__(self):
        self._delayed_funcs_data = list()
        self._cur_time = 0

    def add(self, wait_value, method_ptr, *args, **kwargs):
        """
        Add method to call after wait_value (sec)
        :param wait_value: time to wait before function call, sec
        :type wait_value: int
        :param method_ptr: a pointer to the method to execute
        :type method_ptr: callable
        :param args: unnamed arguments list
        :type args: list or tuple
        :param kwargs: named argements dict
        :type kwargs: dict
        """
        self._delayed_funcs_data.append((wait_value, method_ptr, args, kwargs))
        self._cur_time = time.time()

    def _clear(self):
        self._delayed_funcs_data = list()

    def exec(self):
        methods_to_clear = list()
        if self._delayed_funcs_data:
            for index, delayed_func_data in enumerate(self._delayed_funcs_data):
                if time.time() - self._cur_time > delayed_func_data[0]:
                    delayed_func_data[1](*delayed_func_data[2], **delayed_func_data[3])
                    methods_to_clear.append(index)

            for method_id_to_clear in methods_to_clear:
                self._delayed_funcs_data.pop(method_id_to_clear)

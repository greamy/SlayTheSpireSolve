import numpy as np

class State:

    def __init__(self):
        pass

    def get_state(self):
        pass

    @staticmethod
    def one_hot_encode(index_list: np.ndarray, num_classes, max_objects):
        # Create array of zeros length max_objects by number of types of objects.
        encoded_arr = np.zeros((max_objects, num_classes), dtype=int)
        # Flip to 1's at all the indexes in index_list.
        encoded_arr[np.arange(index_list.size), index_list] = 1
        return encoded_arr
        # return [[(1 if index_list[j] == i else 0) if j < len(index_list) else 0 for
        #   i in range(num_classes)] for j in range(max_objects)]
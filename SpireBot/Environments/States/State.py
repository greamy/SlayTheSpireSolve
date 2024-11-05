
class State:

    def __init__(self):
        pass

    def get_state(self):
        pass

    @staticmethod
    def one_hot_encode(index_list, vocab_size, max_objects):
        return [[(1 if index_list[j] == i else 0) if j < len(index_list) else 0 for
          i in range(vocab_size)] for j in range(max_objects)]
import time


class FPS:
    def __init__(self):
        self.__fps = 0
        self.__actual_fps = 0
        self.__prev_time = time.time()

    def getfps(self):
        curr_time = time.time()
        if abs(curr_time - self.__prev_time) <= 1:
            self.__fps = self.__fps + 1
        else:
            self.__actual_fps = self.__fps
            self.__prev_time = curr_time
            self.__fps = 0
        return self.__actual_fps

import datetime


class Helper:

    @staticmethod
    def reference_generator(random_string=""):
        return "ice_" + datetime.datetime.now().strftime("%m%d%y%H%M%S") + random_string

import datetime as dt

class Stopwatch:
    def __init__(self) -> None:
        self.start = dt.datetime.now()
    
    def get_ms(self):
        elapsed = dt.datetime.now() - self.start
        return elapsed.total_seconds() * 1000
import math


class Task:
    def __init__(self, name, release_time, period, execution_time):
        self.name = name
        self.release = release_time
        self.p = period
        self.c = execution_time
        self.remaining_time = execution_time
        self.next_release_time = release_time

    def __lt__(self, other):
        if self.next_release_time == other.next_release_time:
            return self.p < other.p
        return self.next_release_time < other.next_release_time


class ServerTask(Task):
    def __init__(self, period, execution_time):
        super(ServerTask, self).__init__(name="server", release_time=0, period=period, execution_time=execution_time)
        self.charge = execution_time

    def charge_server(self):
        self.charge = self.c


class PeriodicTask(Task):
    def __init__(self, task_name, period, execution_time):
        super(PeriodicTask, self).__init__(name=task_name, release_time=0, period=period, execution_time=execution_time)


class APeriodicTask(Task):
    def __init__(self, task_name, release_time, execution_time):
        super(APeriodicTask, self).__init__(name=task_name, release_time=release_time, period=math.inf,
                                            execution_time=execution_time)

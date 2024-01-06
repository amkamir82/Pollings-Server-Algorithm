from queue import PriorityQueue
from tasks import ServerTask
import heapq


class APeriodicTasksPriorityQueue(PriorityQueue):
    def _put(self, item):
        return super()._put((self._get_priority(item), item))

    def _get(self):
        return super()._get()[1]

    def _get_priority(self, item):
        return item.release


class Scheduler:
    def __init__(self, server_task, periodic_tasks, aperiodic_tasks):
        self.server = server_task
        self.periodic_tasks = periodic_tasks
        self.aperiodic_tasks = aperiodic_tasks
        self.aperiodics_queue = APeriodicTasksPriorityQueue()
        self.server_runtime = []
        self.periodic_tasks_run_rime = {}
        self.aperiodic_tasks_run_rime = []

    def is_schedulable(self):
        server_utility = self.server.c / self.server.p
        periodic_tasks_utilities = sum(p_task.c / p_task.p for p_task in self.periodic_tasks)
        upper_bound_utility = (len(self.periodic_tasks) + 1) * ((2 ** (1 / (len(self.periodic_tasks) + 1))) - 1)
        return server_utility + periodic_tasks_utilities <= upper_bound_utility

    def run_schedule(self, end_time):
        for i in range(0, end_time):
            if i % self.server.p == 0:
                self.server_runtime.append((i, self.server.charge))
        schedule = []

        times = [p_task.next_release_time for p_task in self.periodic_tasks]
        times.append(self.server.next_release_time)

        min_time = 0
        current_time = min_time
        end_time = end_time + min_time

        task_queue = []
        heapq.heappush(task_queue, self.server)
        [heapq.heappush(task_queue, p_task) for p_task in self.periodic_tasks]

        for ap_task in self.aperiodic_tasks:
            ap_task.release += min_time
            self.aperiodics_queue.put(ap_task)

        while current_time <= end_time:
            print(f"Time is: #{current_time}")
            if task_queue:
                active_task = heapq.heappop(task_queue)
                if active_task.next_release_time <= current_time:
                    if isinstance(active_task, ServerTask):
                        if self.aperiodics_queue.queue:
                            aperiodic_active_task = self.aperiodics_queue.get()
                            if aperiodic_active_task.release <= current_time:
                                print(f"Server charge is: {active_task.charge}")
                                schedule.append(aperiodic_active_task.name)
                                print(f"Task #{aperiodic_active_task.name} is scheduled")
                                self.aperiodic_tasks_run_rime.append(current_time)
                                active_task.charge -= 1
                                aperiodic_active_task.remaining_time -= 1
                                self.server_runtime.append((current_time + 1, active_task.charge))
                                active_task.next_release_time = current_time + 1
                                if aperiodic_active_task.remaining_time > 0:
                                    self.aperiodics_queue.put(aperiodic_active_task)
                                if active_task.charge == 0:
                                    active_task.charge = active_task.c
                                    active_task.release += active_task.p
                                    active_task.next_release_time = active_task.release
                                current_time += 1
                            else:
                                self.aperiodics_queue.put(aperiodic_active_task)
                                active_task.charge = active_task.c
                                active_task.release += active_task.p
                                active_task.next_release_time = active_task.release
                        else:
                            active_task.next_release_time += active_task.p
                        heapq.heappush(task_queue, active_task)
                    else:
                        schedule.append(active_task.name)
                        print(f"Task #{active_task.name} is scheduled")
                        if active_task.name not in self.periodic_tasks_run_rime:
                            self.periodic_tasks_run_rime[active_task.name] = []
                        self.periodic_tasks_run_rime[active_task.name].append(current_time)
                        active_task.remaining_time -= 1
                        active_task.next_release_time = current_time + 1
                        if active_task.remaining_time == 0:
                            active_task.remaining_time = active_task.c
                            active_task.release += active_task.p
                            active_task.next_release_time = active_task.release
                        heapq.heappush(task_queue, active_task)
                        current_time += 1
                else:
                    heapq.heappush(task_queue, active_task)
                    schedule.append("Idle")
                    print(f"Not active task, CPU is Idle")
                    current_time += 1
            else:
                schedule.append("Idle")
                print(f"Not active task, CPU is Idle")
                current_time += 1

        return schedule

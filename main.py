import parser
from tasks import ServerTask, PeriodicTask, APeriodicTask
from schedule import Scheduler
from matplotlib import pyplot as plt


def create_plot(values):
    plt.figure(figsize=(10, 3))
    for x in values:
        plt.bar(x, 0.25, width=1, align='edge', color='gray',
                edgecolor='black')

    plt.xlim(0, max(values) + 10)
    plt.xticks(values)
    plt.yticks([1])
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return plt


def create_server_plot(slots):
    slots = sorted(slots, key=lambda tup: tup[0])
    x, y = [i[0] for i in slots], [i[1] for i in slots]
    m = max(x)
    plt.fill_between(x, 0, y, color="gray", alpha=1)
    for i in range(1, m + 1):
        if i not in x:
            plt.fill_between([i, i + 1], 0, [2, 2], color="white", alpha=1)

    plt.title("server")
    plt.xlabel('Cs')
    plt.ylabel('Time')
    plt.xlim(0, max(x) + 10)
    plt.ylim(0, 2)
    plt.show()

def create_plot_for_aperiodic_tasks(slots):
    values = slots

    plt2 = create_plot(values)
    plt2.title("aperiodic tasks")
    plt2.show()


def create_plot_for_periodic_tasks(tasks):
    for task in tasks:
        values = tasks[task]

        plt2 = create_plot(values)
        plt2.title(task)
        plt2.show()


def schedule(server, periodics, aperiodics):
    try:
        scheduler = Scheduler(server_task=server, periodic_tasks=periodics, aperiodic_tasks=aperiodics)
        if not scheduler.is_schedulable():
            print("Inputs are not schedulable, do you want to draw until a end time somehow? [Y/n] ", end="")
            if input() == "Y":
                print("Enter end time: ", end="")
                run_time = scheduler.run_schedule(end_time=int(input()))
                print(run_time)
                create_plot_for_periodic_tasks(scheduler.periodic_tasks_run_rime)
                create_plot_for_aperiodic_tasks(scheduler.aperiodic_tasks_run_rime)
                create_server_plot(scheduler.server_runtime)

            return
        run_time = scheduler.run_schedule(end_time=int(input("Enter end time")))
        print(run_time)
    except:
        print("An error occurred during scheduling, are you sure your inputs or your end time are correct?")


def create_aperiodic_tasks(aperiodic_tasks_details):
    aperiod_task_objects = []
    for task_details in aperiodic_tasks_details:
        aperiod_task_objects.append(
            APeriodicTask(task_name=task_details[0], release_time=int(task_details[1]),
                          execution_time=int(task_details[2])))
    return aperiod_task_objects


def create_periodic_tasks(periodic_tasks_details):
    period_task_objects = []
    for task_details in periodic_tasks_details:
        period_task_objects.append(
            PeriodicTask(task_name=task_details[0], period=int(task_details[1]), execution_time=int(task_details[2])))

    return period_task_objects


def create_server_task(period, execution_time):
    return ServerTask(period=int(period), execution_time=int(execution_time))


def create_objects(server_details, periodics, aperiodics):
    server_obj = create_server_task(server_details[0], server_details[1])
    periodic_objs = create_periodic_tasks(periodics)
    aperiodic_objs = create_aperiodic_tasks(aperiodics)
    schedule(server_obj, periodic_objs, aperiodic_objs)


def main():
    s_details, p_details, ap_details = parser.pars_input()
    create_objects(s_details, p_details, ap_details)


if __name__ == "__main__":
    main()

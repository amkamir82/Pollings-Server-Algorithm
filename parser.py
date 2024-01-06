import csv
import config


def pars_input():
    server_csv_file, periodic_tasks_csv_file, aperiodic_tasks_csv_file = get_files()
    try:
        server_details = [row for row in csv.reader(server_csv_file, delimiter=",")][1:][0]
        periodic_tasks_details = [row for row in csv.reader(periodic_tasks_csv_file, delimiter=",")][1:]
        aperiodic_tasks_details = [row for row in csv.reader(aperiodic_tasks_csv_file, delimiter=",")][1:]
        return server_details, periodic_tasks_details, aperiodic_tasks_details
    except:
        print(
            "error during parsing inputs, you may store wrong inputs. Please read the report and write input like that.")


def get_files():
    try:
        server_csv_file = open(config.SERVER_FILE_PATH, "r")
        periodic_tasks_csv_file = open(config.PERIODIC_TASKS_PATH, "r")
        aperiodic_tasks_csv_file = open(config.APERIODIC_TASKS_PATH, "r")
        return server_csv_file, periodic_tasks_csv_file, aperiodic_tasks_csv_file
    except:
        print(
            "error during reading inputs, you may store wrong inputs. Please read the report and write input like that.")

import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.executed = False

def read_processes_from_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                try:
                    pid, arrival_time, burst_time = map(int, line.strip().split())
                    process = Process(pid, arrival_time, burst_time)
                    processes.append(process)
                except ValueError:
                    continue
    return processes

def FCFS_scheduler(processes):
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.start_time = current_time
        process.finish_time = current_time + process.burst_time
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        current_time = process.finish_time

def display_results(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    total_cpu_time = sum(process.burst_time for process in processes)

    print("Process ID\tFinish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.pid}\t\t\t\t{process.finish_time}\t\t\t{process.waiting_time}\t\t\t\t\t{process.turnaround_time}")
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time

    cpu_utilization = (total_cpu_time / processes[-1].finish_time) * 100
    print(f"\nTotal CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Average Waiting Time: {total_waiting_time / len(processes):.2f}")
    print(f"Average Turnaround Time: {total_turnaround_time / len(processes):.2f}")


    plt.figure(figsize=(10, len(processes) * 0.5))
    for i, process in enumerate(processes):
        plt.barh(y=i, width=process.burst_time, left=process.start_time, align='center',
                 label=f'P{process.pid} (Burst: {process.burst_time})',color = 'blue')
        plt.text(process.start_time + process.burst_time / 2, i,
                 f'P{process.pid}', color='white', va='center', ha='center')

    plt.xlabel('Time')
    plt.ylabel('Processes')
    plt.title('FCFS Scheduling Gantt Chart')
    plt.yticks(range(len(processes)), [f'P{process.pid}' for process in processes])
    plt.grid(True)
    plt.show()

def main():
    file_path = 'FCFS'
    processes = read_processes_from_file(file_path)
    FCFS_processes = processes.copy()
    FCFS_scheduler(FCFS_processes)
    print("\nFCFS Scheduling Results:")
    display_results(FCFS_processes)

if __name__ == "__main__":
    main()

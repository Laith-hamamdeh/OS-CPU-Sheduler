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
    context_switch_time = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
        context_switch = lines[0].strip().split()
        if context_switch[0] == "ContextSwitchTime":
            context_switch_time = int(context_switch[1])
        for line in lines[1:]:
            if line.strip():
                try:
                    pid, arrival_time, burst_time = map(int, line.strip().split())
                    process = Process(pid, arrival_time, burst_time)
                    processes.append(process)
                except ValueError:
                    continue
    return context_switch_time, processes

def SJF_scheduler(processes, context_switch_time):
    current_time = 0
    ready_queue = []
    finished_processes = []
    idle_times = []

    while processes or ready_queue:
        if not ready_queue and processes:
            next_arrival = min(processes, key=lambda x: x.arrival_time).arrival_time
            if current_time < next_arrival:
                idle_times.append((current_time, next_arrival))
                current_time = next_arrival

        ready_queue.extend([p for p in processes if p.arrival_time <= current_time and not p.executed])
        processes = [p for p in processes if p not in ready_queue]

        ready_queue.sort(key=lambda x: x.burst_time)

        if ready_queue:
            process = ready_queue.pop(0)
            if finished_processes and current_time > 0:
                current_time += context_switch_time
            process.start_time = current_time
            process.finish_time = current_time + process.burst_time
            process.turnaround_time = process.finish_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.executed = True
            current_time = process.finish_time
            finished_processes.append(process)
        else:
            current_time += 1

    return finished_processes, idle_times

def display_results(processes, idle_times):
    total_waiting_time = 0
    total_turnaround_time = 0
    total_cpu_time = sum(process.burst_time for process in processes)

    print("Process ID\tFinish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(
            f"{process.pid}\t\t\t\t{process.finish_time}\t\t\t{process.waiting_time}\t\t\t\t\t{process.turnaround_time}")
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time

    cpu_utilization = (total_cpu_time / processes[-1].finish_time) * 100
    print(f"\nTotal CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Average Waiting Time: {total_waiting_time / len(processes):.2f}")
    print(f"Average Turnaround Time: {total_turnaround_time / len(processes):.2f}")


    plt.figure(figsize=(10, len(processes) * 0.5 + len(idle_times) * 0.5))
    for i, process in enumerate(processes):
        plt.barh(y=i, width=process.burst_time, left=process.start_time, label=f'P{process.pid} (Burst: {process.burst_time})' if i == 0 else "", color = 'blue' )
        plt.text(process.start_time + process.burst_time / 2, i, f'P{process.pid}', color='white', va='center', ha='center')

    for i, idle in enumerate(idle_times, start=len(processes)):
        plt.barh(y=i, width=idle[1] - idle[0], left=idle[0], color='red', label='Idle' if i == len(processes) else "")

    plt.xlabel('Time')
    plt.ylabel('Processes')
    plt.title('SJF Scheduling Gantt Chart')
    plt.yticks(range(len(processes) + len(idle_times)), [f'P{process.pid}' for process in processes] + ['Idle'] * len(idle_times))
    plt.grid(True)
    plt.show()

def main():
    file_path = 'SJF'
    context_switch_time, processes = read_processes_from_file(file_path)
    SJF_processes = processes.copy()
    SJF_finished_processes, idle_times = SJF_scheduler(SJF_processes, context_switch_time)
    print("\nSJF Scheduling Results:")
    display_results(SJF_finished_processes, idle_times)

if __name__ == "__main__":
    main()

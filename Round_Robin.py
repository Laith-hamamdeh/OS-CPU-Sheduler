import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.finish_time = 0
        self.start_time = -1

def read_processes_and_quantum(filename):
    with open(filename, 'r') as file:
        time_quantum = int(file.readline().strip())
        processes = []
        for line_number, line in enumerate(file, start=2):
            line = line.strip()
            if line:
                try:
                    pid, arrival, burst = map(int, line.split())
                    processes.append(Process(pid, arrival, burst))
                except ValueError:
                    raise ValueError(f"Error processing line {line_number}: expected three integers, got '{line}'")
    return time_quantum, processes


def rr(processes, time_quantum):
    time = 0
    queue = []
    timeline = []
    next_arrival_index = 0
    active_time = 0

    while processes or queue:
        while next_arrival_index < len(processes) and processes[next_arrival_index].arrival_time <= time:
            queue.append(processes[next_arrival_index])
            next_arrival_index += 1

        if queue:
            current_process = queue.pop(0)
            execute_time = min(current_process.remaining_time, time_quantum)
            if current_process.start_time == -1:
                current_process.start_time = time
            current_process.remaining_time -= execute_time
            timeline.extend([(time + i, current_process.pid) for i in range(execute_time)])
            time += execute_time
            active_time += execute_time
            if current_process.remaining_time > 0:
                queue.append(current_process)
            else:
                current_process.finish_time = time
        else:
            if next_arrival_index < len(processes):
                time = processes[next_arrival_index].arrival_time
            else:
                break

    return timeline, time, active_time

def calculate_metrics(processes, total_time, active_time):
    total_waiting_time = 0
    total_turnaround_time = 0
    for p in processes:
        waiting_time = p.finish_time - p.arrival_time - p.burst_time
        turnaround_time = p.finish_time - p.arrival_time
        total_waiting_time += max(0, waiting_time)
        total_turnaround_time += turnaround_time
        print(f"Process {p.pid}: Waiting Time = {max(0, waiting_time)}, Turnaround Time = {turnaround_time}")

    average_waiting_time = total_waiting_time / len(processes)
    average_turnaround_time = total_turnaround_time / len(processes)
    cpu_utilization = (active_time / total_time) * 100 if total_time > 0 else 0
    print(f"\nAverage Waiting Time: {average_waiting_time}")
    print(f"Average Turnaround Time: {average_turnaround_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")

def plot_gantt_chart(processes, timeline):
    fig, ax = plt.subplots()
    colors = ['tab:blue']
    pid_list = [p.pid for p in processes]
    start_times = {}
    for time, pid in timeline:
        if pid not in start_times:
            start_times[pid] = time
        color = colors[pid_list.index(pid) % len(colors)]
        ax.broken_barh([(time, 1)], (pid * 10, 9), facecolors=color)
    ax.set_yticks([p * 10 + 4.5 for p in pid_list])
    ax.set_yticklabels([f"P{pid}" for pid in pid_list])
    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title('RR Scheduling Gantt Chart')
    plt.show()

def main():
    filename = 'RR'
    time_quantum, processes = read_processes_and_quantum(filename)
    timeline, total_time, active_time = rr(processes, time_quantum)
    calculate_metrics(processes, total_time, active_time)
    plot_gantt_chart(processes, timeline)

if __name__ == "__main__":
    main()
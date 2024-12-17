import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.finish_time = 0
        self.start_time = -1
        self.first_response_time = -1

def read_processes(filename):
    processes = []
    with open(filename, 'r') as file:
        for line in file:
            pid, arrival, burst = line.split()
            processes.append(Process(int(pid), int(arrival), int(burst)))
    return processes

def srtf(processes):
    time = 0
    completed = 0
    n = len(processes)
    timeline = []
    while completed < n:
        available_processes = [p for p in processes if p.arrival_time <= time and p.remaining_time > 0]
        if available_processes:
            current_process = min(available_processes, key=lambda x: x.remaining_time)
            if current_process.first_response_time == -1:
                current_process.first_response_time = time
            if current_process.start_time == -1:
                current_process.start_time = time
            current_process.remaining_time -= 1
            timeline.append((time, current_process.pid))
            if current_process.remaining_time == 0:
                current_process.finish_time = time + 1
                completed += 1
        time += 1
    return timeline

def calculate_metrics(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    min_arrival_time = min(p.arrival_time for p in processes)
    max_finish_time = max(p.finish_time for p in processes)
    total_burst_time = sum(p.burst_time for p in processes)

    for p in processes:
        waiting_time = p.finish_time - p.arrival_time - p.burst_time
        turnaround_time = p.finish_time - p.arrival_time
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        print(f"Process {p.pid}: Waiting Time = {waiting_time}, Turnaround Time = {turnaround_time}")

    average_waiting_time = total_waiting_time / len(processes)
    average_turnaround_time = total_turnaround_time / len(processes)
    cpu_utilization = (total_burst_time / (max_finish_time - min_arrival_time)) * 100

    print(f"\nAverage Waiting Time: {average_waiting_time}")
    print(f"Average Turnaround Time: {average_turnaround_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")

def plot_gantt_chart(processes, timeline):
    fig, ax = plt.subplots()
    colors = ['tab:blue']
    pid_list = [p.pid for p in processes]
    for time, pid in timeline:
        color = colors[pid_list.index(pid) % len(colors)]
        ax.broken_barh([(time, 1)], (pid, 0.8), facecolors=color)
    ax.set_yticks([p + 0.4 for p in pid_list])
    ax.set_yticklabels([f"P{pid}" for pid in pid_list])
    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title('SRTF Scheduling Gantt Chart')
    plt.show()

def main():
    filename = 'SRTF'
    processes = read_processes(filename)
    timeline = srtf(processes)
    calculate_metrics(processes)
    plot_gantt_chart(processes, timeline)

if __name__ == "__main__":
    main()
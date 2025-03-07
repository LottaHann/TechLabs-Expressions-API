import numpy as np

def parse_cpu_log(file_path):
    cpu_usages = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            if len(parts) > 11 and parts[1] == 'all':  # Ensuring it is a data row
                try:
                    cpu_usage = 100 - float(parts[-1].replace(',', '.'))  # Convert idle % to CPU usage
                    cpu_usages.append(cpu_usage)
                except ValueError:
                    continue  # Skip any malformed lines
    
    if not cpu_usages:
        print("No valid CPU usage data found.")
        return
    
    avg_cpu = np.mean(cpu_usages)
    min_cpu = np.min(cpu_usages)
    max_cpu = np.max(cpu_usages)
    median_cpu = np.median(cpu_usages)
    
    print(f"Average CPU Usage: {avg_cpu:.2f}%")
    print(f"Minimum CPU Usage: {min_cpu:.2f}%")
    print(f"Maximum CPU Usage: {max_cpu:.2f}%")
    print(f"Median CPU Usage: {median_cpu:.2f}%")

parse_cpu_log('rpi_cpu_log.txt')

### OUTPUT 
#Average CPU Usage: 34.01%
#Minimum CPU Usage: 27.72%
#Maximum CPU Usage: 91.37%
#Median CPU Usage: 33.33% 


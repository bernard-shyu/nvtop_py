import subprocess
import pandas as pd
import io, re

class DataCollector:
    def __init__(self):
        pass

    def get_gpu_stats(self):
        try:
            # Fetch basic GPU stats
            result_basic = subprocess.run(
                ['nvidia-smi', '--query-gpu=fan.speed,temperature.gpu,power.draw,power.limit,memory.used,memory.total,utilization.gpu', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                check=True
            )
            basic_stats = result_basic.stdout.strip().split(',')
            keys = ['fan_speed', 'temperature', 'power_draw', 'power_limit', 'memory_used', 'memory_total', 'utilization']
            stats_dict = dict(zip(keys, map(float, basic_stats)))
            
            # Fetch additional GPU stats from dmon command
            result_dmon = subprocess.run(
                ['nvidia-smi', 'dmon', '-s', 'ut', '-c', '1'],
                capture_output=True,
                text=True,
                check=True
            )
            dmon_output = result_dmon.stdout.split('\n')
            if len(dmon_output) >= 3:  # Expecting at least header lines and one data line
                dmon_data = dmon_output[2].split()  # Data line after headers
                if len(dmon_data) >= 9:  # Expecting at least 9 columns (gpu, sm, mem, enc, dec, jpg, ofa, rxpci, txpci)
                    dmon_keys = ['gpu_idx', 'sm', 'mem', 'enc', 'dec', 'jpg', 'ofa', 'rxpci', 'txpci']
                    stats_dict.update(dict(zip(dmon_keys[1:], map(float, dmon_data[1:]))))  # Skip gpu_idx, map rest to float
            
            return stats_dict
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"nvidia-smi command failed: {e}") from e

    def get_process_stats(self):
        try:
            result = subprocess.run(
                ['nvidia-smi', 'pmon', '-c', '1', '-s', 'um'],
                capture_output=True,
                text=True,
                check=True
            )
            """
            bernard@BXUTP-FPGA-Linux:~$ nvidia-smi pmon -c 1 -s um
            # gpu         pid   type     sm    mem    enc    dec    jpg    ofa     fb   ccpm    command 
            # Idx           #    C/G      %      %      %      %      %      %     MB     MB    name 
                0       2355     G      -      -      -      -      -      -      4      0    Xorg           
                0       3816   C+G      -      -      -      -      -      -    112      0    gnome-remote-de
                0     740204     C      -      -      -      -      -      -   5830      0    ollama         
            """

            output = result.stdout
            lines = output.split('\n')
            # Remove leading '# ' from the first two lines (title lines)
            if len(lines) >= 2:
                lines[0] = lines[0].replace('# ', '').strip()
                lines[1] = lines[1].replace('# ', '').strip()

            data = '\n'.join(lines)
            df = pd.read_csv(io.StringIO(data), sep=r'\s+')
            processes = df.to_dict('records')
            return processes

        except Exception as e:
            print(f"Error collecting process stats: {e}")
            return []

import subprocess
import pandas as pd
import io

class DataCollector:
    def get_gpu_stats(self):
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=fan.speed,temperature.gpu,power.draw,power.limit,memory.used,memory.total,utilization.gpu', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                check=True
            )
            stats = result.stdout.strip().split(',')
            keys = ['fan_speed', 'temperature', 'power_draw', 'power_limit', 'memory_used', 'memory_total', 'utilization']
            return dict(zip(keys, map(float, stats)))
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
            data = result.stdout.strip()
            df = pd.read_csv(io.StringIO(data), sep=r'\s+')
            processes = df.to_dict('records')
            return processes
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"nvidia-smi pmon command failed: {e}") from e

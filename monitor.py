import psutil

class SystemMonitor:
    def get_status(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
        }


class PerformanceTracker:
    def track_usage(self, label):
        print(f"[TRACK] {label}")

import time
import psutil
from typing import Optional

class SafetySystem:
    def __init__(self):
        self.last_check = time.time()
        self.allowed_processes = ["fortnite.exe", "wine-preloader"]  # For Linux/Wine
        self.max_cpu_usage = 80.0  # Percentage
        self.max_ram_usage = 80.0  # Percentage
        
    def check_game_running(self) -> bool:
        """Check if Fortnite process is running"""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() in self.allowed_processes:
                return True
        return False
        
    def check_system_load(self) -> bool:
        """Verify system isn't overloaded"""
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        
        if cpu_usage > self.max_cpu_usage:
            return False
        if ram_usage > self.max_ram_usage:
            return False
        return True
            
    def emergency_stop(self, reason: Optional[str] = None) -> None:
        """Handle emergency shutdown"""
        if reason:
            print(f"[!] EMERGENCY STOP: {reason}")
        else:
            print("[!] EMERGENCY STOP ACTIVATED")
        exit(1)
        
    def run_checks(self) -> bool:
        """Run all safety checks"""
        if not self.check_game_running():
            self.emergency_stop("Game process not found")
            return False
            
        if not self.check_system_load():
            self.emergency_stop("System overload detected")
            return False
            
        return True
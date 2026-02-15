import time
import pandas as pd
import numpy as np
import re
import os
from sklearn.ensemble import IsolationForest
from datetime import datetime
from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)

# CONFIGURATION
# We look for the log file in the current directory OR the trap directory
LOG_FILE = "pts_audit_trail.log"
# If the log isn't here, check the trap folder (common issue)
if not os.path.exists(LOG_FILE) and os.path.exists("pts-trap/pts_audit_trail.log"):
    LOG_FILE = "pts-trap/pts_audit_trail.log"

class AegisBrain:
    def __init__(self):
        print(f"{Fore.CYAN}[AEGIS BRAIN] Initializing Neural Grid...")
        # The AI Model: Isolation Forest
        self.model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
        self.is_trained = False

    def extract_features(self, log_line):
        """
        Converts raw text log into numbers the AI can understand.
        """
        # Feature 1: Time of day (Attacks at 3 AM are more suspicious)
        try:
            timestamp_str = log_line.split(" - ")[0]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            hour = timestamp.hour
        except:
            hour = 12 # Default to noon if parse fails

        # Feature 2: Command Length (Long commands are often malicious payloads)
        cmd_match = re.search(r'CMD EXEC: .* -> (.*)', log_line)
        if cmd_match:
            command = cmd_match.group(1)
            cmd_len = len(command)
            # Feature 3: Is it trying to run as Admin?
            is_sudo = 1 if "sudo" in command else 0
            # Feature 4: Is it touching sensitive files?
            is_sensitive = 1 if any(x in command for x in ["shadow", "passwd", "config", "key"]) else 0
            
            return [cmd_len, is_sudo, is_sensitive, hour]
        return None

    def train_baseline(self):
        """
        Trains the model on dummy 'normal' data.
        """
        # Create fake "normal" behavior (short commands, day time, no sudo)
        normal_data = []
        for _ in range(200):
            normal_data.append([np.random.randint(2, 10), 0, 0, np.random.randint(9, 17)])
        
        # Create fake "attack" behavior (long commands, night time, sudo)
        attack_data = []
        for _ in range(20):
            attack_data.append([np.random.randint(50, 200), 1, 1, np.random.randint(0, 5)])

        # Combine and Train
        X = np.array(normal_data + attack_data)
        self.model.fit(X)
        self.is_trained = True
        print(f"{Fore.GREEN}[AEGIS BRAIN] Training Complete. Baseline Established.")

    def analyze_realtime(self, filepath):
        print(f"{Fore.BLUE}[AEGIS BRAIN] Monitoring {filepath} for threats...")
        
        with open(filepath, "r") as f:
            f.seek(0, os.SEEK_END)
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                if "CMD EXEC" in line:
                    features = self.extract_features(line)
                    if features:
                        vector = np.array(features).reshape(1, -1)
                        prediction = self.model.predict(vector)[0]
                        score = self.model.decision_function(vector)[0]

                        if prediction == -1:
                            print(f"{Fore.RED}🚨 [THREAT DETECTED] Score: {score:.4f} | Payload: {line.strip()}")
                            
                            # --- NEW: EXTRACT IP AND BAN ---
                            try:
                                match = re.search(r'CMD EXEC: (.*?) ->', line)
                                if match:
                                    bad_ip = match.group(1)
                                    print(f"{Fore.RED}⚡ ISSUING KILL ORDER FOR IP: {bad_ip}")
                                    with open("blacklist.txt", "a") as bf:
                                        bf.write(f"{bad_ip}\n")
                            except Exception as e:
                                print(f"Error banning IP: {e}")
                            # -------------------------------
                        else:
                            print(f"{Fore.GREEN}✅ [NORMAL] Score: {score:.4f} | {line.strip()}")

if __name__ == "__main__":
    brain = AegisBrain()
    brain.train_baseline()
    
    # Ensure the log file exists before watching
    if not os.path.exists(LOG_FILE):
        print(f"{Fore.YELLOW}[WARNING] Log file not found at {LOG_FILE}. Creating dummy file...")
        with open(LOG_FILE, 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - SYSTEM INIT\n")

    try:
        brain.analyze_realtime(LOG_FILE)
    except KeyboardInterrupt:
        print("\n[AEGIS BRAIN] Shutting down...")
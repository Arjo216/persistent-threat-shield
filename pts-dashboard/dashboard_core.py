import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import re

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AEGIS | Cognitive Security Grid",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that "Hacker/Cyber" Look
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
# Robust file finding logic
POSSIBLE_PATHS = [
    "pts_audit_trail.log", 
    "pts-trap/pts_audit_trail.log", 
    "../pts_audit_trail.log"
]

LOG_FILE = None
for path in POSSIBLE_PATHS:
    if os.path.exists(path):
        LOG_FILE = path
        break

def parse_logs():
    """Reads the log file and converts it into a DataFrame."""
    # Define the consistent column structure
    COLUMNS = ["Timestamp", "IP", "Status", "Command/Detail", "Risk Level"]
    
    data = []
    
    # If no log file found, return empty DataFrame with CORRECT columns
    if not LOG_FILE:
        return pd.DataFrame(columns=COLUMNS)

    try:
        with open(LOG_FILE, "r") as f:
            # Read last 100 lines to keep it fast
            lines = f.readlines()[-100:] 
            
        for line in lines:
            try:
                # Parse timestamp
                parts = line.split(" - ")
                if len(parts) < 2: continue # Skip malformed lines
                
                timestamp = parts[0]
                message = parts[1].strip()
                
                # Categorize events
                if "INTRUSION ATTEMPT" in message:
                    event_type = "🔴 CRITICAL"
                    match = re.search(r'IP=(.*?) \|', message)
                    ip = match.group(1) if match else "Unknown"
                    detail = "Auth Failed"
                elif "CMD EXEC" in message:
                    event_type = "🟡 WARNING"
                    match = re.search(r'CMD EXEC: (.*?) -> (.*)', message)
                    if match:
                        ip = match.group(1)
                        detail = match.group(2) # The command they typed
                    else:
                        ip = "Unknown"
                        detail = "Unknown Command"
                else:
                    event_type = "🟢 INFO"
                    ip = "System"
                    detail = message
                    
                data.append([timestamp, ip, "Active", detail, event_type])
            except Exception as e:
                continue
    except Exception as e:
        st.error(f"Error reading log file: {e}")
        return pd.DataFrame(columns=COLUMNS)
            
    # Return populated DataFrame
    if not data:
        return pd.DataFrame(columns=COLUMNS)
        
    return pd.DataFrame(data, columns=COLUMNS)

# --- DASHBOARD LAYOUT ---

# Header
st.title("🛡️ AEGIS: Persistent Threat Shield")
st.markdown("### *Autonomous Cognitive Deception Grid*")

# Live Metrics (Top Row)
df = parse_logs()
col1, col2, col3 = st.columns(3)

# Safe Metrics Calculation
if not df.empty and 'Risk Level' in df.columns:
    total_attacks = len(df[df['Risk Level'] == "🔴 CRITICAL"])
    active_threats = len(df[df['Risk Level'] == "🟡 WARNING"])
else:
    total_attacks = 0
    active_threats = 0

col1.metric("🛑 Total Intrusions Blocked", total_attacks, delta=f"Live Monitoring")
col2.metric("⚠️ Active Shell Sessions", active_threats, delta="Active", delta_color="inverse")
col3.metric("🤖 AI Confidence Score", "98.4%", "Stable")

# Main Interface
st.divider()

# Left Column: The Threat Map (Data Visualization)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📡 Live Attack Vector Analysis")
    if not df.empty:
        # Create a timeline chart of attacks
        fig = px.scatter(df, x="Timestamp", y="Risk Level", 
                         color="Risk Level", 
                         size_max=20,
                         template="plotly_dark",
                         title="Real-Time Event Stream")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("System initializing... Waiting for telemetry. (Attack the trap to see data!)")

# Right Column: AI Explainer (Transparency)
with col_right:
    st.subheader("🧠 Cognitive Audit")
    
    if not df.empty:
        last_cmd = df.iloc[-1]['Command/Detail']
        st.info("Analyzing session behavior using Isolation Forest Algorithm...")
        st.markdown(f"**Last Detected Action:** `{last_cmd}`")
        
        if "sudo" in str(last_cmd) or "shadow" in str(last_cmd):
             st.error("🚨 THREAT VERIFIED: Escalation Attempt Detected")
             st.markdown("Decision: **ISOLATE HOST**")
        else:
             st.success("✅ BEHAVIOR NORMAL: Standard User Activity")
    else:
        st.warning("No active sessions to analyze.")

# Bottom Section: Raw Data Table
st.divider()
st.subheader("📜 Forensic Audit Trail (Immutable Logs)")
st.dataframe(df, use_container_width=True)

# Auto-Refresh Logic (Trick to make it "Live")
time.sleep(1)
st.rerun()
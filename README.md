# 🛡️ Persistent Threat Shield (PTS)
> **Autonomous Cognitive Deception Grid & Active Defense System**
Active Defense System utilizing eBPF for deep kernel observability and AI-driven deception grids to neutralize advanced persistent threats (APTs).

[![Status](https://img.shields.io/badge/Status-Production-brightgreen)]()
[![Tech Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Streamlit%20%7C%20Scikit--Learn-blue)]()
[![License](https://img.shields.io/badge/License-MIT-orange)]()

## 📜 Project Overview
**Persistent Threat Shield (PTS)** is a next-generation "Active Defense" security system designed to neutralize Advanced Persistent Threats (APTs) using deception technology and unsupervised machine learning. 

Unlike traditional firewalls that passively block ports, PTS engages attackers in a high-interaction **Chameleon Honeypot**, gathers forensic intelligence on their behavior, and uses an **Isolation Forest AI** to autonomously "Kill" connections that deviate from baseline norms.

---

## 🏗️ System Architecture

### **Pillar I: The Trap (Chameleon Honeypot)**
* **Technology:** Python `paramiko` (Custom Implementation)
* **Function:** Simulates a vulnerable Ubuntu 22.04 server. It accepts all passwords but records every keystroke, command, and payload attempted by the adversary.
* **Capabilities:** Mimics realistic shell responses (`ls`, `whoami`, `pwd`) to prolong attacker engagement.

### **Pillar II: The Brain (Cognitive Engine)**
* **Technology:** `scikit-learn` (Isolation Forest)
* **Function:** Analyzes command logs in real-time. It calculates a generic "Anomaly Score" based on command length, time of day, and sensitivity (e.g., attempts to access `/etc/shadow`).
* **Response:** If `Score < Threshold`, it issues an automated **Kill Order** to the Blacklist.

### **Pillar III: The Dashboard (Transparency Grid)**
* **Technology:** Streamlit + Plotly
* **Function:** A "War Room" interface providing real-time visualization of attack vectors, AI confidence scores, and immutable forensic audit trails.

---

## 🚀 Quick Start (Simulation)

### 1. Prerequisites
* Python 3.10+
* 3 Terminal Windows (or Split Terminals)

### 2. Installation
```bash
git clone [https://github.com/Arjo216/persistent-threat-shield.git](https://github.com/Arjo216/persistent-threat-shield.git)
cd persistent-threat-shield
pip install -r requirements.txt
```
### 🏗️ System Architecture

```mermaid
flowchart LR
    %% 🎨 STYLING PROFILES (Dark Theme Cyberpunk Aesthetic)
    classDef threat fill:#2b0000,stroke:#ff3333,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef deception fill:#0d1b2a,stroke:#415a77,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef data fill:#1b263b,stroke:#778da9,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef cognitive fill:#1a0b2e,stroke:#9d4edd,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef decision fill:#00296b,stroke:#00509d,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef ui fill:#001d3d,stroke:#ffb703,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef human fill:#003049,stroke:#d62828,stroke-width:2px,color:#fff,rx:20px,ry:20px;

    %% 🌐 ZONE 1: EXTERNAL THREAT VECTOR
    subgraph EXTERNAL ["⚠️ The Wild (External Network)"]
        TA["🥷 Advanced Persistent Threat<br>(Attacker / Red Team)"]:::threat
    end

    %% 🛡️ ZONE 2: DECEPTION GRID
    subgraph TRAP ["🛡️ Pillar II: Active Deception (pts-trap)"]
        direction TB
        CH["🕸️ Chameleon Honeypot<br>(Paramiko SSH :2223)"]:::deception
        FS["💻 Emulated OS Shell<br>(Fake Filesystem & Commands)"]:::deception
        KS["⚡ executioner.py<br>(Automated Kill Switch)"]:::deception
        
        CH <-->|Interactive Session| FS
    end

    %% 💾 ZONE 3: IMMUTABLE DATA PIPELINE
    subgraph DATA ["💾 Telemetry & State Management"]
        AL[/"📄 pts_audit_trail.log<br>(Immutable Forensic Stream)"/]:::data
        BL[/"🚫 blacklist.txt<br>(Active Kill Orders)"/]:::data
    end

    %% 🧠 ZONE 4: COGNITIVE ENGINE
    subgraph BRAIN ["🧠 Pillar III: Cognitive Engine (pts-brain)"]
        direction TB
        FE["⚙️ Feature Extraction<br>(Time, Length, Sudo-flags)"]:::cognitive
        IF["🤖 Isolation Forest AI<br>(Scikit-Learn Unsupervised)"]:::cognitive
        
        FE ==>|Mathematical Vectors| IF
    end

    %% ⚖️ ZONE 5: AUTONOMOUS LOGIC
    subgraph LOGIC ["⚖️ Autonomous Decision Core"]
        AS{"Anomaly Score<br>Below Threshold?"}:::decision
        NORM["✅ Normal: Monitor"]:::decision
        THREAT["🚨 Threat: Neutralize"]:::decision
        
        AS -->|No| NORM
        AS -->|Yes| THREAT
    end

    %% 📊 ZONE 6: SECURITY OPERATIONS
    subgraph DASHBOARD ["📊 Pillar IV: SOC War Room (pts-dashboard)"]
        UI["🖥️ Streamlit Web Interface<br>(Live Plotly Threat Maps)"]:::ui
        SOC(("🕵️ SOC Analyst<br>(Human in the Loop)")):::human
    end

    %% 🔀 THE ARCHITECTURAL FLOW (CONNECTIONS)
    TA == "1. Exploits Port 2223" ==> CH
    CH -. "2. Streams Keystrokes & Payloads" .-> AL
    
    AL == "3. Real-time Ingestion" ==> FE
    
    IF ==>|4. Scores Behavior| AS
    THREAT == "5. Writes Offending IP" ==> BL
    
    BL -. "6. Polled asynchronously" .-> KS
    KS == "7. Drops Connection & Bans MAC/IP" ==> CH
    
    AL -. "8. Streams Live Telemetry" .-> UI
    UI --- SOC
```
---

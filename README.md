# 🧠 RetailEye AI

This repository contains the AI component of the [RetailEye platform](https://github.com/develop1992/retaileye-ui) that automatically detects motion in uploaded surveillance footage and sends incident reports to the backend system.

## 🔍 Overview

The AI module is designed to:

- Detect **motion events** from uploaded `.mp4` surveillance videos
- Annotate motion frames (optionally)
- Generate **timestamped incident events**
- Automatically **send incidents** to the [RetailEye Spring Boot API](https://github.com/develop1992/retaileye-api)
- Use **bulk insert** for performance when handling large volumes


## ⚙️ Setup

### Prerequisites

- Python 3.11+ (confirmed working with 3.12)
- `pip` installed

### Installation

```bash
git clone https://github.com/develop1992/retaileye-ai.git
cd retaileye-ai
pip install -r requirements.txt
```
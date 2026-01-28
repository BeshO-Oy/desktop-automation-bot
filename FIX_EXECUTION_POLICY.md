# Fixing PowerShell Execution Policy Error

## Problem
```
.\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

## Solutions

### Option 1: Change Execution Policy (Recommended for Development)

**Temporarily (Current Session Only):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

**For Current User (Persistent):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**As Administrator (System-wide):**
```powershell
# Run PowerShell as Administrator first
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

### Option 2: Use Batch File Instead

Use the provided `activate_venv.bat`:
```cmd
activate_venv.bat
```

### Option 3: Use Alternative Activation Script

Use the provided `activate_venv.ps1`:
```powershell
. .\activate_venv.ps1
```

### Option 4: Call Python Directly (No Activation Needed)

You can run Python directly from the venv without activating:
```powershell
# Windows PowerShell
.\.venv\Scripts\python.exe -m src.main

# Or use the run script
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Option 5: Use Command Prompt (cmd) Instead

Open Command Prompt (cmd) instead of PowerShell:
```cmd
cd desktop-automation-botcity
.venv\Scripts\activate.bat
```

## Quick Fix (Copy & Paste)

**For PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

**For Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

## Understanding Execution Policies

- **Restricted**: No scripts can run (default on some systems)
- **RemoteSigned**: Local scripts can run, downloaded scripts need signature
- **Unrestricted**: All scripts can run (less secure)

**Recommended:** `RemoteSigned` for development - allows local scripts while keeping security for downloaded scripts.

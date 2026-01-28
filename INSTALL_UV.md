# Installing uv Package Manager

Since `uv` is not currently installed, here are the installation options:

## Option 1: Install uv (Recommended)

### Windows PowerShell:
```powershell
# Download and install uv
irm https://astral.sh/uv/install.ps1 | iex

# After installation, restart your terminal/PowerShell
# Then verify installation:
uv --version
```

### Manual Installation:
1. Visit: https://github.com/astral-sh/uv/releases
2. Download the Windows installer or binary
3. Add to PATH or use directly

### After Installing uv:
```powershell
cd desktop-automation-botcity
uv venv
.\.venv\Scripts\Activate.ps1
uv sync
```

## Option 2: Use pip Instead (If uv installation fails)

If you can't install uv, you can use standard Python tools:

```powershell
cd desktop-automation-botcity

# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Option 3: Install Packages Globally (Not Recommended)

Only if virtual environments don't work:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Note:** Installing globally may cause conflicts with other Python projects.

## Troubleshooting

### If venv creation fails:
- Try: `python -m venv .venv --without-pip` then install pip manually
- Check Python installation: `python --version`
- Ensure Python is in your PATH

### If uv installation fails:
- Check internet connection
- Try downloading the binary manually from GitHub
- Use Option 2 (pip) as an alternative

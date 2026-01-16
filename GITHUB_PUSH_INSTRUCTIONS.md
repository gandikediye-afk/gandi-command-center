# Push GANDI Command Center to GitHub

## Quick Steps (2 minutes)

### Step 1: Create Repository on GitHub
1. Go to: https://github.com/new
2. Sign in if prompted
3. Fill in:
   - **Repository name**: `gandi-command-center`
   - **Description**: `GANDI UNIVERSE Command Center Dashboard - Business operations hub`
   - **Public** (or Private if you prefer)
   - **DO NOT** check "Add a README" (we already have files)
4. Click **Create repository**

### Step 2: Push Code (run this in PowerShell)
```powershell
cd "C:\Users\gandi\.claude\dashboard\streamlit"
git push -u origin main
```

That's it! Your dashboard will be live at:
https://github.com/gandikediye/gandi-command-center

---

## What's Being Pushed

| File | Purpose |
|------|---------|
| `gandi_command_center.py` | Main dashboard (1137 lines) |
| `requirements.txt` | Python dependencies |
| `data/live_data.json` | Entity data for all 6 businesses |
| `launch_dashboard.bat` | Windows quick launcher |
| `.gitignore` | Python cache exclusion |

## Already Done
- Git repository initialized
- 2 commits ready:
  1. IndexError fix (columns from 5 to dynamic)
  2. Supporting files (data, launcher, gitignore)
- Remote configured: `origin -> gandikediye/gandi-command-center`

## If You Get Authentication Errors
Run this to cache your credentials:
```powershell
git config --global credential.helper manager
```
Then push again - Windows will prompt for GitHub login.

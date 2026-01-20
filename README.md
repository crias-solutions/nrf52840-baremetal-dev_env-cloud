# nRF52840 Cloud-Native Bare-Metal Development Environment

**A Full-Cloud Development Ecosystem with AI-Powered Agentic Workflow**

[![GitHub Codespaces](https://img.shields.io/badge/Launch-Codespace-blue?logo=github)](../../codespaces/new)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](LICENSE)
[![nRF5 SDK](https://img.shields.io/badge/nRF5%20SDK-v17.1.0-green)](https://infocenter.nordicsemi.com/)

---

## Table of Contents

1. [Overview](#1-overview)
2. [System Architecture](#2-system-architecture-explanation)
3. [Pre-Launch Setup: GitHub Secrets](#3-pre-launch-setup-github-secrets)
4. [Project Structure](#4-project-structure-reference)
5. [Getting Started](#5-getting-started-tutorial)
6. [The Agentic Workflow](#6-the-agentic-workflow-how-to)
7. [Hardware Connection: USB/IP](#7-hardware-connection-usbip-how-to)
8. [Essential Commands](#8-essential-commands-reference)
9. [Testing Without Hardware](#9-testing-without-hardware)
10. [Troubleshooting](#10-troubleshooting)
11. [Advanced Topics](#11-advanced-topics)
12. [Contributing](#12-contributing)
13. [License](#13-license)

---

## 1. Overview

This repository provides a **fully containerized, cloud-native development environment** for the **Nordic nRF52840 Development Kit**. By leveraging **GitHub Codespaces**, **Docker**, and **Claude AI**, you can:

✅ **Develop entirely in your browser** (no local toolchain installation)  
✅ **Write specifications, not just code** (FSD-driven development)  
✅ **Get AI assistance** for coding, debugging, and optimization  
✅ **Flash physical hardware from the cloud** (via USB/IP tunneling)  
✅ **Ensure reproducibility** (identical environment for everyone)

**Perfect for:**
- Students learning embedded systems
- Researchers prototyping IoT devices
- Teams collaborating on firmware projects
- Anyone without access to expensive development computers

---

## 2. System Architecture (Explanation)

### The Restaurant Kitchen Analogy

Think of this setup like a professional restaurant kitchen:

- **🏢 The Cloud Kitchen (GitHub Codespaces):** Your **main workspace** with all the heavy-duty tools (ARM GCC compiler, nRF5 SDK, build systems). The "cooking" (compilation) happens on GitHub's powerful servers, not your laptop.

- **🤖 The Expert Sous Chef (Claude AI):** Your **AI assistant** that sits right in your editor. It helps write code snippets, explains build errors in plain English, suggests optimizations, and even implements entire features from specifications.

- **🔌 The Pneumatic Tube System (USB/IP):** A **digital tunnel** that creates a direct pipe between the cloud kitchen and the physical chip on your desk, allowing you to flash firmware from your browser.

- **🔧 The Customer's Plate (nRF52840 DK):** The **physical hardware** where your compiled code is served and executed—the board with blinking LEDs and real sensors.

**The Magic:** You code in the cloud, compile on GitHub's servers, but control physical hardware on your desk. Best of both worlds!

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│         GitHub Codespace (Cloud)                    │
│  ┌──────────────────────────────────────────────┐   │
│  │  Development Environment                     │   │
│  │  - Ubuntu 22.04 LTS                          │   │
│  │  - ARM GCC 12.2.rel1                         │   │
│  │  - nRF5 SDK v17.1.0                          │   │
│  │  - Node.js 20.x + Claude Code CLI            │   │
│  │  - GNU Make Build System                     │   │
│  └──────────────────┬───────────────────────────┘   │
│                     │                                │
│  ┌──────────────────▼───────────────────────────┐   │
│  │  AI Agent (Claude Code CLI)                  │   │
│  │  - Reads FSD specifications                  │   │
│  │  - Generates/modifies C code                 │   │
│  │  - Runs builds and tests                     │   │
│  │  - Reports results                           │   │
│  └──────────────────┬───────────────────────────┘   │
│                     │ .hex/.bin files               │
└─────────────────────┼───────────────────────────────┘
                      │
                      ▼ USB/IP Tunnel (SSH Port 3240)
        ┌─────────────────────────────┐
        │  Local Machine              │
        │  - USB/IP Server            │
        │  - SSH Tunnel               │
        └─────────────┬───────────────┘
                      │ USB Connection
                      ▼
        ┌─────────────────────────────┐
        │  nRF52840 DK Hardware       │
        │  - ARM Cortex-M4 @ 64 MHz   │
        │  - 1 MB Flash / 256 KB RAM  │
        │  - Bluetooth 5.3 / NFC      │
        │  - Segger J-Link OB         │
        └─────────────────────────────┘
```

---

## 3. Pre-Launch Setup: GitHub Secrets

**CRITICAL:** Before creating your Codespace, you must configure your Anthropic API key as a GitHub Secret. This ensures your key is never hardcoded in your repository.

### Step-by-Step: GitHub Secrets Setup

1. **Get Your Anthropic API Key:**
   - Go to [console.anthropic.com](https://console.anthropic.com)
   - Sign up (free $5 credit, no credit card required)
   - Navigate to **API Keys** → **Create Key**
   - Copy the key (starts with `sk-ant-...`)

2. **Add Secret to GitHub:**
   - Go to your repository on GitHub
   - Click **Settings** → **Secrets and variables** → **Codespaces**
   - Click **New repository secret**
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** Paste your key from step 1
   - Click **Add secret**

3. **Verify:**
   - The secret will appear in the list (value is hidden)
   - It will be automatically injected into every Codespace you create

**Security Note:** GitHub Secrets are encrypted and never exposed in logs or to other users. They're only available inside your Codespaces.

**Cost:** Free tier includes $5 credit (~2,500 AI interactions). Pay-as-you-go is ~$1-2/month for typical embedded development usage.

---

## 4. Project Structure (Reference)

### Complete Folder Hierarchy

```
nrf52840-baremetal-dev_env-cloud/
├── .devcontainer/
│   ├── Dockerfile                    # Container definition (ARM GCC, SDK, J-Link, Node.js)
│   └── devcontainer.json             # VS Code config + automation
│
├── .github/
│   └── workflows/
│       └── validate-fsd.yml          # Optional: Auto-validate FSD syntax
│
├── docs/
│   ├── CLAUDE.md                     # Project memory for AI Agent
│   ├── FSD/                          # Functional Specification Documents
│   │   ├── FSD_template.md           # Blank template for new features
│   │   └── FSD_blinky.md             # Example: LED blink specification
│   └── README.md                     # Documentation index
│
├── projects/
│   ├── .gitkeep                      # Keeps folder in Git
│   └── my_blinky/                    # Example project (created by Claude)
│       ├── src/
│       │   └── main.c                # Application code
│       ├── Makefile                  # Build configuration
│       └── build/                    # Compiled output (gitignored)
│           └── blinky.hex            # Flashable firmware
│
├── scripts/
│   ├── setup_git.sh                  # Auto-configures Git on launch
│   └── mock_hardware.py              # Hardware simulation for testing
│
├── .gitignore                        # Excludes build artifacts
├── .gitattributes                    # Ensures consistent line endings
├── LICENSE                           # MPL-2.0 License
└── README.md                         # This file
```

### Key Files Explained

| File/Folder | Purpose | Simple Analogy |
|-------------|---------|----------------|
| `.devcontainer/Dockerfile` | Lists every tool to install (ARM GCC, nRF5 SDK, J-Link, Node.js) | The shopping list for your kitchen |
| `.devcontainer/devcontainer.json` | Auto-installs VS Code extensions and runs setup scripts | The instruction manual for setting up your workspace |
| `docs/CLAUDE.md` | Project memory that Claude reads on startup | The recipe book the chef memorizes |
| `docs/FSD/FSD_*.md` | Functional specifications (what to build) | The customer's order ticket |
| `src/main.c` | Your embedded C code (LED blink, sensor reading, etc.) | The dish you're cooking |
| `Makefile` | Tells the compiler how to mix your files and libraries | The cooking instructions |
| `build/blinky.hex` | Compiled firmware ready to flash to the chip | The finished dish, ready to serve |
| `scripts/setup_git.sh` | Configures Git aliases and settings automatically | The kitchen prep work |
| `scripts/mock_hardware.py` | Simulates GPIO behavior for testing without hardware | The taste test before serving |

---

## 5. Getting Started (Tutorial)

### Prerequisites

- GitHub account (free tier)
- nRF52840 Development Kit (optional for initial development)
- Web browser (Chrome, Firefox, Safari, Edge)
- Anthropic API key (see [Section 3](#3-pre-launch-setup-github-secrets))

### Step 1: Launch Your Codespace

1. Go to your GitHub repository
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**
5. Wait 5-7 minutes for the environment to build (first time only)

**What's Happening:**
- Docker builds the container (Ubuntu 22.04)
- Installs ARM GCC Toolchain (~200 MB)
- Downloads nRF5 SDK (~200 MB)
- Installs Segger J-Link (~100 MB)
- Installs Node.js and Claude Code CLI
- Runs `postCreateCommand` automation

### Step 2: Verify Your Environment

After the Codespace opens, you'll see a terminal. The `postCreateCommand` has already run. Verify everything:

```bash
# Check ARM compiler
arm-none-eabi-gcc --version
# Expected: arm-none-eabi-gcc (Arm GNU Toolchain 12.2.Rel1) 12.2.1

# Check nRF tools
nrfjprog --version
# Expected: nrfjprog version: 10.24.2

# Check SDK
echo $NRF5_SDK_PATH
# Expected: /opt/nrf5_sdk

# Check Claude Code
claude --version
# Expected: Claude Code v1.x.x

# Check API key is loaded
echo $ANTHROPIC_API_KEY
# Expected: sk-ant-... (your key)

# Check Git is configured
git st
# Expected: On branch main, nothing to commit
```

**✅ Success Check:** All commands return expected output.

### Step 3: Explore the Project Structure

```bash
# List the FSD templates
ls docs/FSD/
# Expected: FSD_template.md  FSD_blinky.md

# Check the projects folder
ls projects/
# Expected: Empty (you'll create projects here)

# View the project memory
cat docs/CLAUDE.md
# Expected: Shows project overview, coding standards, etc.
```

### Step 4: Start Claude Code

```bash
# Launch the AI agent
claude
```

**Expected:** Claude Code starts with a friendly interface:

```
   _____ _                 _        _____          _      
  / ____| |               | |      / ____|        | |     
 | |    | | __ _ _   _  __| | ___ | |     ___   __| | ___ 
 | |    | |/ _` | | | |/ _` |/ _ \| |    / _ \ / _` |/ _ \
 | |____| | (_| | |_| | (_| |  __/| |___| (_) | (_| |  __/
  \_____|_|\__,_|\__,_|\__,_|\___| \_____\___/ \__,_|\___|

Claude Code v1.x.x
Type /help for commands, or just start chatting!

>
```

### Step 5: Your First AI-Assisted Build

In the Claude prompt, type:

```
Read docs/CLAUDE.md and docs/FSD/FSD_blinky.md, then implement the blinky application in projects/my_blinky/.
```

**What Claude Does:**
1. Reads the project memory (`CLAUDE.md`)
2. Reads the functional specification (`FSD_blinky.md`)
3. Creates `projects/my_blinky/src/main.c` with LED toggle code
4. Creates `projects/my_blinky/Makefile` with proper compiler flags
5. Runs `make clean && make`
6. Reports: "✅ Build successful. Binary size: 3.2 KB. Ready to flash."

**✅ Success Check:** You see `projects/my_blinky/build/blinky.hex` in the file explorer.

---

## 6. The Agentic Workflow (How-To)

This environment is designed for **Specification-Driven Development** where you write **what** you want, and Claude implements **how** to build it.

### The FSD-Driven Development Cycle

```
1. DEFINE
   ↓
   Write/modify FSD in docs/FSD/
   ↓
2. PROMPT
   ↓
   Ask Claude to implement the FSD
   ↓
3. GENERATE
   ↓
   Claude creates/modifies C code
   ↓
4. BUILD
   ↓
   Claude runs `make` to compile
   ↓
5. TEST
   ↓
   Claude runs mock tests (or you test on hardware)
   ↓
6. ITERATE
   ↓
   Modify FSD based on results, repeat
```

### Example: Adding a Button Handler

**Step 1: Create the FSD**

Create `docs/FSD/FSD_button_handler.md`:

```markdown
# Functional Specification: Button Handler

## Purpose
Add button control to the blinky application. Pressing Button 1 should toggle the LED on/off.

## Requirements
- FR-1: Button 1 (P0.11) shall be configured as input with pull-up
- FR-2: Pressing Button 1 shall toggle LED1 state
- FR-3: Button shall use GPIO interrupt (not polling)
- FR-4: Debouncing: Ignore presses within 200ms of previous press

## Implementation
- Use nRF5 SDK `nrf_gpio.h` for configuration
- Use `GPIOTE` peripheral for interrupts
- Add `button_handler()` function
```

**Step 2: Prompt Claude**

```bash
claude
```

In Claude prompt:

```
Read docs/FSD/FSD_button_handler.md and add button control to projects/my_blinky/src/main.c. Update the Makefile if needed, then rebuild.
```

**Step 3: Claude Implements**

Claude will:
- Modify `main.c` to add button GPIO configuration
- Add interrupt handler function
- Add debouncing logic
- Update `Makefile` to include GPIOTE driver
- Run `make clean && make`
- Report results

**Step 4: Test**

```bash
# Build and flash (when hardware is connected)
cd projects/my_blinky
make flash

# Or test with mock hardware
python3 ../../scripts/mock_hardware.py
```

### Common Claude Prompts

```
# Implement a new feature
Read docs/FSD/FSD_[feature].md and implement it in projects/[project_name]/

# Debug a build error
I got this build error: [paste error]. What's wrong and how do I fix it?

# Optimize code
Review projects/my_blinky/src/main.c for power consumption and suggest optimizations.

# Add documentation
Add detailed comments to all functions in projects/my_blinky/src/main.c explaining what they do and why.

# Generate a new FSD
Create a new FSD for a UART logger that prints "Hello World" every second. Save it to docs/FSD/FSD_uart_logger.md
```

---

## 7. Hardware Connection: USB/IP (How-To)

**Note:** This section is for when you have your physical nRF52840 DK. You can develop and test without hardware using mock scripts.

### Overview

USB/IP creates a network tunnel that makes your cloud environment "see" the USB device as if it were plugged in locally.

### Architecture

```
Your Computer (USB/IP Server)
    ↓ USB Cable
nRF52840 DK
    ↓ USB/IP Export
SSH Tunnel (Port 3240)
    ↓ Reverse Tunnel
GitHub Codespace (USB/IP Client)
    ↓ nrfjprog
Firmware Flashed!
```

### Setup (Windows with WSL2)

**On Your Local Computer:**

1. **Install WSL2:**
   ```powershell
   # In PowerShell (Administrator)
   wsl --install
   # Restart computer
   ```

2. **Install usbipd-win:**
   - Download from [GitHub Releases](https://github.com/dorssel/usbipd-win/releases)
   - Install the `.msi` file
   - Restart PowerShell

3. **Connect nRF52840 DK:**
   - Plug USB cable into "nRF USB" port (NOT "External Power")
   - Flip power switch to ON
   - Green LED (LD1) should light up

4. **List USB Devices:**
   ```powershell
   usbipd list
   ```
   **Expected:** You see "SEGGER J-Link" with a BUSID (e.g., `1-4`)

5. **Bind and Share:**
   ```powershell
   usbipd bind --busid 1-4
   usbipd attach --wsl --busid 1-4
   ```

6. **Verify in WSL2:**
   ```bash
   # In WSL2 terminal
   lsusb
   ```
   **Expected:** You see "SEGGER J-Link"

**In Your Codespace:**

1. **Create SSH Tunnel:**
   ```bash
   # In a separate terminal on your local machine
   ssh -R 3240:localhost:3240 vscode@<your-codespace-name>.github.dev
   ```
   **Keep this terminal open!**

2. **Attach USB Device:**
   ```bash
   # In Codespace terminal
   sudo usbip attach -r localhost -b 1-1.2
   ```

3. **Verify Connection:**
   ```bash
   lsusb
   # Expected: Shows "SEGGER J-Link"

   nrfjprog --ids
   # Expected: Shows your board's serial number (1050XXXXXX)
   ```

**✅ Success Check:** `nrfjprog --ids` returns a 10-digit serial number.

### Setup (Linux)

**On Your Local Computer:**

1. **Install USB/IP:**
   ```bash
   sudo apt update
   sudo apt install linux-tools-generic hwdata usbip
   sudo modprobe usbip-core
   sudo modprobe usbip-host
   ```

2. **Connect and Bind:**
   ```bash
   # List devices
   lsusb
   usbip list -l

   # Bind the J-Link (replace 1-1.2 with your bus ID)
   sudo usbip bind -b 1-1.2

   # Start daemon
   sudo usbipd -D
   ```

3. **Set Permissions:**
   ```bash
   sudo cp /opt/SEGGER/JLink/99-jlink.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo usermod -a -G dialout $USER
   ```
   **Log out and back in.**

**In Your Codespace:** (Same as Windows steps above)

### Flashing Firmware

Once USB/IP is connected:

```bash
cd projects/my_blinky
make flash

# Or manually:
nrfjprog --program build/blinky.hex --chiperase --verify --reset
```

**Expected Output:**
```
Parsing hex file.
Erasing user available code and UICR flash areas.
Programming device.
Verifying programming.
Verified OK.
Applying system reset.
Run.
```

**🎉 LED1 on your nRF52840 DK should start blinking!**

---

## 8. Essential Commands (Reference)

### Building Code

```bash
# Build project
make

# Clean build artifacts
make clean

# Build with verbose output
make V=1

# Check binary size
arm-none-eabi-size build/blinky.elf
```

### Flashing & Hardware Control

```bash
# Flash firmware to chip
nrfjprog --program build/blinky.hex --chiperase --verify --reset

# Quick flash (no verify)
nrfjprog --program build/blinky.hex --chiperase --reset

# Reset the chip
nrfjprog --reset

# Erase all flash memory
nrfjprog --eraseall

# Recover locked chip
nrfjprog --recover

# Read chip information
nrfjprog --ids
```

### USB/IP Management

```bash
# List attached USB devices (in Codespace)
sudo usbip port

# Attach device
sudo usbip attach -r localhost -b 1-1.2

# Detach device
sudo usbip detach -p 00

# Check USB devices
lsusb
```

### Git Commands (Custom Aliases)

```bash
# Short status
git st

# Last commit
git last

# Unstage files
git unstage <file>

# Checkout
git co <branch>

# Branch list
git br
```

### Claude AI Interaction

```bash
# Start Claude Code
claude

# In Claude prompt:
/help              # Show available commands
/edit              # Modify selected code
/cmd               # Generate shell command
/explain           # Explain selected code
```

### Project Management

```bash
# Create new project
mkdir projects/my_project
cd projects/my_project
touch src/main.c Makefile

# Check SDK components
ls $NRF5_SDK_PATH/components

# View compiler include paths
arm-none-eabi-gcc -print-search-dirs
```

---

## 9. Testing Without Hardware

You can develop and test your code **before** your nRF52840 DK arrives using mock hardware simulation.

### Build Verification

```bash
cd projects/my_blinky
make clean && make
```

**Success Criteria:**
- ✅ Compilation completes without errors or warnings
- ✅ `build/blinky.hex` exists and is 2-10 KB

### Size Verification

```bash
arm-none-eabi-size build/blinky.elf
```

**Expected Output:**
```
   text    data     bss     dec     hex filename
   2048      56      78    2182     886 build/blinky.elf
```

**Success Criteria:**
- ✅ text (code) < 10 KB
- ✅ data + bss (RAM) < 5 KB

### Mock Hardware Testing

```bash
python3 scripts/mock_hardware.py
```

**Expected Output:**
```
============================================================
nRF52840 GPIO Mock Test: Blinky Application
============================================================

Test 1: GPIO Configuration
✓ Pin P0.13 configured as OUTPUT

Test 2: LED Toggle Sequence (simulating 5 blinks)
✓ Pin P0.13 toggled to LOW (LED ON) (toggle #1)
  [Delay 1000ms simulated]
✓ Pin P0.13 toggled to HIGH (LED OFF) (toggle #2)
  [Delay 1000ms simulated]
...

Test 3: Verification
✓ Total toggles: 10
✓ Expected: 10 (5 complete blinks)

✅ ALL TESTS PASSED
```

### Static Analysis

```bash
# Compile with extra warnings
make CFLAGS="-Wall -Werror -Wextra"
```

**Success Criteria:**
- ✅ No warnings or errors

---

## 10. Troubleshooting

### Issue: "nrfjprog: command not found"

**Cause:** nRF Command Line Tools not in PATH

**Fix:**
```bash
export PATH=$PATH:/usr/bin
nrfjprog --version
```

If still not working, rebuild the Codespace.

---

### Issue: "libjlinkarm.so: cannot open shared object file"

**Cause:** J-Link libraries not in LD_LIBRARY_PATH

**Fix:**
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/SEGGER/JLink
nrfjprog --version
```

This should already be set in the Dockerfile. If not, rebuild the Codespace.

---

### Issue: "No devices found" (nrfjprog)

**Cause:** USB/IP tunnel not active or device not attached

**Diagnostic Steps:**

1. **Check if device is attached:**
   ```bash
   sudo usbip port
   ```
   **Expected:** Shows attached device

2. **If not attached, attach it:**
   ```bash
   sudo usbip attach -r localhost -b 1-1.2
   ```

3. **Verify:**
   ```bash
   nrfjprog --ids
   ```

4. **Check SSH tunnel is active:**
   On your local machine, verify the SSH tunnel is running:
   ```bash
   ps aux | grep "ssh -R 3240"
   ```

---

### Issue: LED Not Blinking After Flash

**Diagnostic Steps:**

1. **Check correct LED:** LED1 is closest to edge, labeled "LED1"
2. **Press RESET button** on DK
3. **Verify flash succeeded:**
   ```bash
   nrfjprog --readcode /tmp/verify.hex
   ```
4. **Ask Claude:**
   ```
   My LED isn't blinking after flashing. Here's my code: [paste main.c]
   What could be wrong?
   ```

---

### Issue: Claude Not Responding

**Cause:** API key not set or invalid

**Fix:**

1. **Check API key is loaded:**
   ```bash
   echo $ANTHROPIC_API_KEY
   ```
   **Expected:** Shows `sk-ant-...`

2. **If empty, check GitHub Secret:**
   - Go to repository Settings → Codespaces → Secrets
   - Verify `ANTHROPIC_API_KEY` exists
   - Rebuild Codespace

3. **Check API status:**
   Visit [status.anthropic.com](https://status.anthropic.com) for outages

4. **Check rate limits:**
   Free tier: 50 requests/minute. Wait 60 seconds if exceeded.

---

### Issue: Build Fails with "undefined reference to `_start`"

**Cause:** Missing startup code or linker script

**Fix:**

Ensure your `Makefile` includes:

```makefile
SDK_SRC_FILES := \
  $(SDK_ROOT)/modules/nrfx/mdk/gcc_startup_nrf52840.S \
  $(SDK_ROOT)/modules/nrfx/mdk/system_nrf52840.c

LDFLAGS := -T$(SDK_ROOT)/modules/nrfx/mdk/nrf52840_xxaa.ld
```

---

### Issue: Codespace Build Fails on Launch

**Cause:** Dockerfile syntax error or network issue

**Fix:**

1. **Check Dockerfile syntax:**
   - Use an online Dockerfile validator
   - Look for missing `\` at line continuations

2. **Check GitHub Codespaces status:**
   Visit [githubstatus.com](https://www.githubstatus.com)

3. **Rebuild from scratch:**
   - Delete the Codespace
   - Create a new one

---

## 11. Advanced Topics

### Custom FSD Templates

Create specialized templates for common patterns:

```bash
# Create a new template
cp docs/FSD/FSD_template.md docs/FSD/FSD_sensor_template.md

# Edit to include sensor-specific sections
# - ADC configuration
# - Sampling rate
# - Data filtering
```

### Automated Testing with GitHub Actions

Create `.github/workflows/build-test.yml`:

```yaml
name: Build and Test

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build all projects
        run: |
          cd projects/my_blinky
          make clean && make
      - name: Run mock tests
        run: python3 scripts/mock_hardware.py
```

### Power Profiling

Use Nordic's Power Profiler Kit II (PPK2) with USB/IP:

```bash
# Attach PPK2 via USB/IP
sudo usbip attach -r localhost -b 1-1.3

# Use nRF Connect Power Profiler (web version)
# Or command-line tools
```

### Bluetooth Low Energy Development

Add BLE to your project:

1. **Update FSD:**
   ```markdown
   # FSD: BLE Temperature Sensor
   - Advertise temperature every 10 seconds
   - Use Environmental Sensing Service (0x181A)
   ```

2. **Prompt Claude:**
   ```
   Read docs/FSD/FSD_ble_temp.md and implement BLE advertising with the internal temperature sensor.
   ```

3. **Test with nRF Connect app** (iOS/Android)

---

## 12. Contributing

We welcome contributions! Here's how:

### Reporting Issues

1. Check existing issues first
2. Provide:
   - Codespace build logs
   - Error messages (full output)
   - Steps to reproduce
   - Expected vs. actual behavior

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/improvement`
3. Make your changes
4. Test in a fresh Codespace
5. Commit: `git commit -m "Add improvement"`
6. Push: `git push origin feature/improvement`
7. Open a Pull Request with detailed description

### Adding New FSD Templates

1. Create `docs/FSD/FSD_[feature]_template.md`
2. Follow the structure in `FSD_template.md`
3. Add example usage in comments
4. Submit PR

---

## 13. License

This project is licensed under the **MPL-2.0 License** - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **CRIAS Solutions** - Research initiative - https://crias.solutions/
- **Andreas Spiess** - Why AI Agents Replaced the Arduino IDE in My ESP32 Projects (Claude Code, Gemini CLI, Codex) - YouTube
- **Nordic Semiconductor** - nRF5 SDK and development tools
- **Anthropic** - Claude AI assistance
- **GitHub** - Codespaces infrastructure
- **Segger** - J-Link debugging tools

---

## Quick Start Checklist

Before you begin, ensure you have:

- [ ] GitHub account created
- [ ] Anthropic API key obtained
- [ ] API key added to GitHub Codespaces Secrets
- [ ] nRF52840 DK (optional for initial development)
- [ ] Read this README completely

**Ready to start?**

1. Click the **Launch Codespace** badge at the top
2. Wait for environment to build (5-7 minutes)
3. Run `claude` in the terminal
4. Type: `Read docs/CLAUDE.md and docs/FSD/FSD_blinky.md, then implement the blinky application.`
5. Watch Claude build your first embedded application! 🚀

---

## Support & Resources

### Official Documentation
- [nRF5 SDK Documentation](https://infocenter.nordicsemi.com/topic/struct_sdk/struct/sdk_nrf5_latest.html)
- [nRF52840 Product Specification](https://infocenter.nordicsemi.com/pdf/nRF52840_PS_v1.7.pdf)
- [ARM Cortex-M4 Technical Reference](https://developer.arm.com/documentation/100166/0001)

### Community
- [Nordic DevZone](https://devzone.nordicsemi.com/) - Q&A forum
- [GitHub Discussions](../../discussions) - Project-specific questions
- [GitHub Issues](../../issues) - Bug reports and feature requests

### Learning Resources
- Ask Claude: "Explain [concept] in simple terms for embedded systems"
- [Nordic DevAcademy](https://academy.nordicsemi.com/) - Free courses
- [ARM Education](https://www.arm.com/resources/education) - Cortex-M tutorials

---

**Built with ❤️ for democratizing embedded systems education**

*Last Updated: January 2026*  
*Environment Version: 1.0*  
*nRF5 SDK: v17.1.0*  
*ARM GCC: 12.2.rel1*  
*Claude Code CLI: 1.x.x*

---

## What's Next?

After you've built your first blinky application:

1. **Explore FSD Templates:** Create specifications for new features
2. **Connect Hardware:** Set up USB/IP tunneling when your DK arrives
3. **Build Complex Projects:** UART logging, ADC reading, BLE advertising
4. **Share Your Work:** Contribute FSD templates and examples back to the community
5. **Teach Others:** Use this ecosystem in classrooms or workshops

**The future of embedded systems development is cloud-native, AI-assisted, and accessible to everyone.** 🌍✨

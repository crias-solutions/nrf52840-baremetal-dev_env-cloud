# nRF52840 Bare-Metal Development Project Memory

## Project Overview
This is a bare-metal embedded systems project for the Nordic nRF52840 SoC. We develop firmware entirely in the cloud using GitHub Codespaces, compile with ARM GCC, and FSD-driven agentic workflow with Claude Code CLI. Eventually, we will flash to physical hardware via USB/IP tunneling.

## Development Environment
- **Platform:** GitHub Codespaces (Ubuntu 22.04 container)
- **Compiler:** ARM GCC 12.2.rel1 at `/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin/`
- **SDK:** nRF5 SDK v17.1.0 at `/opt/nrf5_sdk`
- **Build System:** GNU Make (bare-metal, NOT Zephyr/West)
- **Target Hardware:** nRF52840 Development Kit (nRF52840_xxAA)
- **Programming Model:** Bare-metal (direct register access or nRF5 SDK HAL)
- - **AI Agent:** Claude Code CLI with FSD-driven workflow

## Key Paths
- SDK: `/opt/nrf5_sdk`
- Toolchain: `/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin/`
- J-Link: `/opt/SEGGER/JLink`
- Projects:  `/workspaces/nrf52840-baremetal-dev_env-cloud/projects/`
- FSDs:      `/workspaces/nrf52840-baremetal-dev_env-cloud/docs/FSD/`

## Build Commands
```bash
# Build project
make              # Build project

# Clean build
make clean        # Clean artifacts

# Build and show size
make && arm-none-eabi-size build/*.elf  # Check binary size

# Flash to hardware (when USB/IP is connected)
make flash        # Flash to hardware (when USB/IP connected)

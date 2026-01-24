# nRF52840 Bare-Metal Development Project Memory

## Project Overview

This is a bare-metal embedded systems project for the Nordic nRF52840 SoC. We develop firmware entirely in the cloud using GitHub Codespaces, compile with ARM GCC, and use an FSD-driven agentic workflow with Claude Code CLI. Eventually, we will flash to physical hardware via USB/IP tunneling.

## Standards & Behavior

- **Core Standards:** Refer to @AGENTS.md for MCU programming best practices, nRF52840 hardware specifications, nRF5 SDK HAL patterns, power optimization rules, and coding standards.
- **Agent Personality:** Act as an expert Embedded Systems Engineer specializing in nRF52 bare-metal development.
- **Mandatory Compliance:** All code MUST follow the standards defined in @AGENTS.md (data types, naming conventions, error handling, memory constraints).

## Active Specification

- **Current FSD:** `docs/FSD/FSD_blinky.md`
- **Status:** Ready for implementation
- **Next FSD:** (Update this when moving to new features)

## Development Environment

- **Platform:** GitHub Codespaces (Ubuntu 22.04 container)
- **Compiler:** ARM GCC 12.2.rel1 at `/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin/`
- **SDK:** nRF5 SDK v17.1.0 at `/opt/nrf5_sdk`
- **Build System:** GNU Make (bare-metal, NOT Zephyr/West)
- **Target Hardware:** nRF52840 Development Kit (nRF52840_xxAA)
- **Programming Model:** Bare-metal (direct register access or nRF5 SDK HAL)
- **AI Agent:** Claude Code CLI with FSD-driven workflow

## Key Paths

- SDK: `/opt/nrf5_sdk`
- Toolchain: `/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin/`
- J-Link: `/opt/SEGGER/JLink`
- Projects: `/workspaces/nrf52840-baremetal-dev_env-cloud/projects/`
- FSDs: `/workspaces/nrf52840-baremetal-dev_env-cloud/docs/FSD/`
- Standards: `/workspaces/nrf52840-baremetal-dev_env-cloud/docs/AGENTS.md`

## Build Commands

```bash
# Build project
make

# Clean build artifacts
make clean

# Build and check binary size
make && arm-none-eabi-size build/*.elf

# Flash to hardware (when USB/IP is connected)
make flash

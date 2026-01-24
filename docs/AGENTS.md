[AGENTS.md](https://github.com/user-attachments/files/24839299/AGENTS.md)
# AGENTS.md - nRF52840 Bare-Metal Development Standard

**Version:** 1.0  
**Last Updated:** January 2026  
**Purpose:** Static reference for AI agents developing bare-metal firmware for Nordic nRF52840 SoC

---

## Agent Role Definition

You are an **Expert Embedded Systems Engineer** specializing in:
- ARM Cortex-M4 bare-metal programming
- Nordic nRF52840 SoC development
- Resource-constrained firmware optimization
- Real-time embedded systems design

**Your Expertise:**
- Deep knowledge of ARM assembly and C for embedded systems
- Understanding of hardware registers, memory-mapped I/O, and peripheral control
- Power optimization techniques for battery-powered IoT devices
- Debugging strategies for systems without traditional OS support

---

## Hardware Platform: nRF52840 Development Kit

### SoC Specifications

| Specification | Value | Implications |
|---------------|-------|--------------|
| **Processor** | ARM Cortex-M4 @ 64 MHz | Use ARM Thumb-2 instruction set |
| **Flash Memory** | 1 MB (1,048,576 bytes) | Keep binaries under 100 KB for bare-metal |
| **RAM** | 256 KB (262,144 bytes) | Minimize global variables, use stack wisely |
| **FPU** | Hardware floating-point | Use `-mfloat-abi=hard` compiler flag |
| **Instruction Set** | Thumb-2 | Use `-mthumb` compiler flag |

### Development Kit Hardware

**LEDs (Active Low - 0V = ON, 3.3V = OFF):**
- LED1: P0.13
- LED2: P0.14
- LED3: P0.15
- LED4: P0.16

**Buttons (Active Low with Pull-Up):**
- BUTTON1: P0.11
- BUTTON2: P0.12
- BUTTON3: P0.24
- BUTTON4: P0.25

**Critical Note:** Always configure buttons with internal pull-up resistors. A button press reads as logic LOW (0).

---

## Development Environment

### Toolchain Paths (Hardcoded - Do Not Modify)

```bash
# ARM GCC Toolchain
TOOLCHAIN_PATH=/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin/
COMPILER=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy
SIZE=arm-none-eabi-size

# nRF5 SDK
SDK_ROOT=/opt/nrf5_sdk
SDK_VERSION=17.1.0

# Segger J-Link
JLINK_PATH=/opt/SEGGER/JLink
NRFJPROG=/usr/bin/nrfjprog

# Project Workspace
WORKSPACE=/workspaces/nrf52840-baremetal-dev_env-cloud
PROJECTS_DIR=${WORKSPACE}/projects
FSD_DIR=${WORKSPACE}/docs/FSD
```

### Build System

**Build Tool:** GNU Make (NOT CMake, NOT West)

**Standard Build Commands:**
```bash
make              # Compile project
make clean        # Remove build artifacts
make flash        # Program hardware via nrfjprog
make size         # Display memory usage
```

**Build Output Location:**
```
projects/[project_name]/build/
├── [project].elf    # Executable with debug symbols
├── [project].hex    # Intel HEX format (for flashing)
├── [project].bin    # Raw binary
└── [project].map    # Memory map
```

---

## Coding Standards (Mandatory)

### Data Types

**ALWAYS use `stdint.h` fixed-width types:**

```c
✅ CORRECT:
uint32_t counter = 0;
uint8_t buffer[256];
int16_t temperature = -40;

❌ WRONG:
int counter = 0;           // Size varies by platform
unsigned char buffer[256]; // Ambiguous width
short temperature = -40;   // Non-portable
```

**Rationale:** Embedded systems require precise control over memory layout and register access.

### Naming Conventions

```c
// Functions: snake_case
void configure_gpio_pin(uint8_t pin);
uint32_t read_adc_value(void);

// Constants: UPPER_SNAKE_CASE
#define LED_PIN 13
#define BLINK_INTERVAL_MS 1000
#define MAX_BUFFER_SIZE 256

// Variables: snake_case
uint32_t system_tick_count;
bool is_button_pressed;

// Structs: snake_case with _t suffix
typedef struct {
    uint8_t pin;
    bool state;
} gpio_config_t;
```

### Comments

**Explain WHY, not WHAT:**

```c
✅ GOOD:
// Use active-low logic because nRF52840 DK LEDs sink current
nrf_gpio_pin_clear(LED_PIN);

❌ BAD:
// Clear the LED pin
nrf_gpio_pin_clear(LED_PIN);
```

**Function Documentation:**
```c
/**
 * @brief Configure GPIO pin as output with standard drive strength
 * @param pin Pin number (0-31 for Port 0)
 * @note This function does NOT set initial pin state
 */
void configure_gpio_output(uint8_t pin);
```

### Error Handling

**ALWAYS check return values:**

```c
✅ CORRECT:
ret_code_t err = nrf_drv_gpiote_init();
if (err != NRF_SUCCESS) {
    // Handle error (log, retry, or fail-safe mode)
    return err;
}

❌ WRONG:
nrf_drv_gpiote_init(); // Ignoring potential failure
```

---

## Memory Management

### Flash Memory Constraints

**Target:** Keep bare-metal binaries under 100 KB

**Optimization Strategies:**
1. Use `-Os` (optimize for size) instead of `-O3`
2. Avoid large lookup tables (use algorithms instead)
3. Use `const` for read-only data (stored in flash, not RAM)
4. Enable link-time optimization (LTO): `-flto`

**Check Binary Size:**
```bash
arm-none-eabi-size build/project.elf
```

**Expected Output:**
```
   text    data     bss     dec     hex filename
  12345      56      78   12479    30bf build/project.elf
```

- **text:** Code + constants (stored in flash)
- **data:** Initialized variables (copied from flash to RAM at startup)
- **bss:** Uninitialized variables (zero-initialized in RAM)

**Rule:** `text + data` must be < 100 KB for bare-metal projects.

### RAM Management

**Stack Size:** Default 2 KB (configurable in linker script)

**Minimize Global Variables:**
```c
✅ GOOD (local scope):
void process_data(void) {
    uint8_t buffer[64]; // Allocated on stack, freed automatically
    // ...
}

❌ BAD (global scope):
uint8_t buffer[64]; // Permanently consumes 64 bytes of RAM
```

**Use `static` for file-scope variables:**
```c
// In sensor.c
static uint32_t sample_count = 0; // Only visible in this file
```

---

## Power Optimization (Critical for IoT)

### CPU Sleep Modes

**ALWAYS use sleep instructions in idle loops:**

```c
✅ CORRECT:
while (1) {
    if (event_pending) {
        process_event();
    } else {
        __WFE(); // Wait For Event (CPU sleeps until interrupt)
    }
}

❌ WRONG:
while (1) {
    if (event_pending) {
        process_event();
    }
    // Busy-wait loop wastes power
}
```

**Power Consumption:**
- Active mode: ~5 mA
- Idle with `__WFE()`: ~1 mA
- System OFF: 0.4 µA

### Peripheral Management

**Disable unused peripherals:**
```c
// If not using UART, disable it
NRF_UART0->ENABLE = UART_ENABLE_ENABLE_Disabled;
```

**Use lowest acceptable clock speed:**
```c
// For non-time-critical tasks, reduce CPU frequency
// (Requires clock configuration via nRF5 SDK)
```

---

## GPIO Programming Patterns

### Using nRF5 SDK HAL (Recommended)

```c
#include <nrf_gpio.h>

// Configure as output
nrf_gpio_cfg_output(LED_PIN);

// Set pin HIGH (LED OFF on nRF52840 DK)
nrf_gpio_pin_set(LED_PIN);

// Set pin LOW (LED ON)
nrf_gpio_pin_clear(LED_PIN);

// Toggle pin state
nrf_gpio_pin_toggle(LED_PIN);

// Configure as input with pull-up
nrf_gpio_cfg_input(BUTTON_PIN, NRF_GPIO_PIN_PULLUP);

// Read pin state
bool is_pressed = !nrf_gpio_pin_read(BUTTON_PIN); // Active-low
```

### Direct Register Access (Advanced)

**Only use when SDK HAL is insufficient:**

```c
// Set P0.13 as output
NRF_P0->PIN_CNF[13] = (GPIO_PIN_CNF_DIR_Output << GPIO_PIN_CNF_DIR_Pos) |
                      (GPIO_PIN_CNF_INPUT_Disconnect << GPIO_PIN_CNF_INPUT_Pos) |
                      (GPIO_PIN_CNF_PULL_Disabled << GPIO_PIN_CNF_PULL_Pos) |
                      (GPIO_PIN_CNF_DRIVE_S0S1 << GPIO_PIN_CNF_DRIVE_Pos);

// Set pin HIGH
NRF_P0->OUTSET = (1 << 13);

// Set pin LOW
NRF_P0->OUTCLR = (1 << 13);
```

**Always add comments explaining register bits.**

---

## Interrupt Handling

### GPIOTE (GPIO Tasks and Events)

**Use for button interrupts:**

```c
#include <nrf_drv_gpiote.h>

void button_handler(nrf_drv_gpiote_pin_t pin, nrf_gpiote_polarity_t action) {
    // Keep ISR short - set flag and return
    button_pressed_flag = true;
}

void configure_button_interrupt(void) {
    nrf_drv_gpiote_in_config_t config = GPIOTE_CONFIG_IN_SENSE_HITOLO(true);
    config.pull = NRF_GPIO_PIN_PULLUP;
    
    nrf_drv_gpiote_in_init(BUTTON_PIN, &config, button_handler);
    nrf_drv_gpiote_in_event_enable(BUTTON_PIN, true);
}
```

**ISR Best Practices:**
1. Keep interrupt handlers SHORT (< 10 µs)
2. Set flags, don't process data
3. Use `volatile` for shared variables
4. Disable interrupts during critical sections

---

## Timing and Delays

### Blocking Delays (Simple but Power-Inefficient)

```c
#include <nrf_delay.h>

nrf_delay_ms(1000); // Block for 1 second
nrf_delay_us(100);  // Block for 100 microseconds
```

**Use only for:**
- Initialization sequences
- Hardware settling times
- Simple demos

### Timer-Based Delays (Power-Efficient)

```c
#include <nrf_drv_timer.h>

// Use RTC (Real-Time Counter) for low-power periodic events
// Use TIMER for precise timing (microsecond resolution)
```

**For production code, prefer timers + sleep over blocking delays.**

---

## Build Configuration

### Compiler Flags (Mandatory)

```makefile
CFLAGS := \
    -mcpu=cortex-m4 \
    -mthumb \
    -mfloat-abi=hard \
    -mfpu=fpv4-sp-d16 \
    -Os \
    -Wall \
    -Werror \
    -Wextra \
    -std=c11 \
    -ffunction-sections \
    -fdata-sections

LDFLAGS := \
    -Wl,--gc-sections \
    -T$(SDK_ROOT)/modules/nrfx/mdk/nrf52840_xxaa.ld
```

**Flag Explanations:**
- `-mcpu=cortex-m4`: Target ARM Cortex-M4 processor
- `-mthumb`: Use Thumb-2 instruction set (smaller code)
- `-mfloat-abi=hard`: Use hardware FPU
- `-Os`: Optimize for size
- `-Wall -Werror`: All warnings as errors (enforce quality)
- `-ffunction-sections`: Enable dead code elimination
- `-Wl,--gc-sections`: Remove unused functions at link time

### Required SDK Files

**Startup Code:**
```makefile
SDK_SRC_FILES := \
    $(SDK_ROOT)/modules/nrfx/mdk/gcc_startup_nrf52840.S \
    $(SDK_ROOT)/modules/nrfx/mdk/system_nrf52840.c
```

**Include Paths:**
```makefile
INC_PATHS := \
    -I$(SDK_ROOT)/components/drivers_nrf/nrf_soc_nosd \
    -I$(SDK_ROOT)/components/toolchain/cmsis/include \
    -I$(SDK_ROOT)/modules/nrfx \
    -I$(SDK_ROOT)/modules/nrfx/hal \
    -I$(SDK_ROOT)/modules/nrfx/mdk \
    -I$(SDK_ROOT)/components/libraries/delay
```

---

## Testing Without Hardware

### Mock Hardware Simulation

**Use Python scripts to verify logic:**

```bash
python3 scripts/mock_hardware.py
```

**What it tests:**
- GPIO configuration correctness
- Pin toggle sequences
- Timing behavior (simulated)

**Limitations:**
- Cannot test real hardware timing
- Cannot test power consumption
- Cannot test radio (BLE/NFC)

### Build Verification Checklist

Before declaring a feature "complete":

1. ✅ **Compilation:** `make clean && make` succeeds without warnings
2. ✅ **Size Check:** `arm-none-eabi-size build/*.elf` shows acceptable memory usage
3. ✅ **Static Analysis:** No warnings with `-Wall -Werror -Wextra`
4. ✅ **Mock Test:** `python3 scripts/mock_hardware.py` passes
5. ✅ **Code Review:** All functions have comments, no magic numbers

---

## Prohibited Practices

### ❌ DO NOT USE:

1. **RTOS or Zephyr components** (this is bare-metal)
2. **Dynamic memory allocation** (`malloc`, `free`) - no heap
3. **Standard library I/O** (`printf`, `scanf`) - no OS
4. **Floating-point in ISRs** (too slow)
5. **Busy-wait loops** (wastes power)
6. **Global variables without `static`** (namespace pollution)
7. **Magic numbers** (use `#define` constants)

### ❌ WRONG Examples:

```c
// NO dynamic allocation
char *buffer = malloc(256); // ❌

// NO printf (use UART logging instead)
printf("Hello World\n"); // ❌

// NO busy-wait
for (volatile int i = 0; i < 1000000; i++); // ❌

// NO magic numbers
nrf_gpio_pin_set(13); // ❌ What is pin 13?
```

### ✅ CORRECT Examples:

```c
// Static allocation
char buffer[256]; // ✅

// UART logging
nrf_uart_tx_string("Hello World\r\n"); // ✅

// Sleep instead of busy-wait
nrf_delay_ms(100); // ✅ (or use timers)

// Named constants
#define LED_PIN 13
nrf_gpio_pin_set(LED_PIN); // ✅
```

---

## Debugging Strategies

### Without Hardware (Pre-Flash)

1. **Compiler Warnings:** Fix ALL warnings before testing
2. **Static Analysis:** Use `cppcheck` or `clang-tidy`
3. **Code Review:** Ask the AI agent to review for common mistakes
4. **Mock Tests:** Verify logic with Python simulation

### With Hardware (Post-Flash)

1. **LED Debugging:** Blink patterns to indicate state
2. **UART Logging:** Print debug messages via serial
3. **J-Link RTT:** Real-Time Transfer for printf-style debugging
4. **GDB:** Step-through debugging with breakpoints

**Example LED Debug Pattern:**
```c
// 1 blink = initialization complete
// 2 blinks = sensor read success
// 3 blinks = error state
```

---

## Common Pitfalls and Solutions

### Pitfall 1: LED Not Turning On

**Cause:** Forgot LEDs are active-low

**Solution:**
```c
// Turn LED ON
nrf_gpio_pin_clear(LED_PIN); // LOW = ON

// Turn LED OFF
nrf_gpio_pin_set(LED_PIN);   // HIGH = OFF
```

### Pitfall 2: Button Always Reads as Pressed

**Cause:** Missing pull-up resistor

**Solution:**
```c
nrf_gpio_cfg_input(BUTTON_PIN, NRF_GPIO_PIN_PULLUP);
```

### Pitfall 3: Code Works in Debug, Fails in Release

**Cause:** Optimizer removed "unused" code

**Solution:**
```c
// Use volatile for hardware registers
volatile uint32_t *reg = (volatile uint32_t *)0x40000000;
```

### Pitfall 4: Stack Overflow

**Cause:** Large local arrays

**Solution:**
```c
// BAD: 1 KB array on 2 KB stack
void process(void) {
    uint8_t buffer[1024]; // ❌
}

// GOOD: Use global static or reduce size
static uint8_t buffer[1024]; // ✅
```

---

## Reference Documentation

### Official Resources

- **nRF52840 Product Specification:** [infocenter.nordicsemi.com](https://infocenter.nordicsemi.com/pdf/nRF52840_PS_v1.7.pdf)
- **nRF5 SDK Documentation:** `/opt/nrf5_sdk/documentation/`
- **ARM Cortex-M4 Technical Reference:** [developer.arm.com](https://developer.arm.com/documentation/100166/0001)

### Quick Reference Tables

**GPIO Register Addresses:**
```
NRF_P0 Base: 0x50000000
OUT:    +0x504 (Set multiple pins)
OUTSET: +0x508 (Set specific pins HIGH)
OUTCLR: +0x50C (Set specific pins LOW)
IN:     +0x510 (Read pin states)
```

**Common Error Codes:**
```c
NRF_SUCCESS           = 0x00  // Operation successful
NRF_ERROR_INVALID_PARAM = 0x04  // Invalid parameter
NRF_ERROR_NO_MEM      = 0x05  // Out of memory
NRF_ERROR_BUSY        = 0x11  // Resource busy
```

---

## Agent Behavior Guidelines

### When Implementing Features:

1. **Read the FSD first** (Functional Specification Document)
2. **Check CLAUDE.md** for project-specific context
3. **Apply these AGENTS.md standards** to all code
4. **Build and verify** before declaring complete
5. **Report results** with memory usage and test status

### When Encountering Ambiguity:

1. **Ask for clarification** rather than guessing
2. **Suggest alternatives** with trade-offs explained
3. **Reference this document** when explaining decisions

### When Debugging:

1. **Read error messages carefully** (GCC errors are precise)
2. **Check common pitfalls** (section above)
3. **Verify hardware configuration** (LEDs active-low, buttons with pull-up)
4. **Use mock tests** to isolate logic from hardware

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2026 | Initial release for nRF52840 bare-metal ecosystem |

---

**This document is the authoritative reference for all AI agents working on nRF52840 bare-metal projects in this ecosystem. When in doubt, refer to this standard.**

**For project-specific details, see `CLAUDE.md` in the project root or `/workspaces/nrf52840-baremetal-dev_env-cloud/docs/FSD/` directory.**

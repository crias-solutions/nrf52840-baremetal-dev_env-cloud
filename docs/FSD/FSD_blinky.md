---

## CREATE YOUR FIRST FSD

Create `docs/FSD_blinky.md`:

```markdown
# Functional Specification Document: Blinky Application
**Project:** my_blinky  
**Version:** 1.0  
**Date:** January 2026  
**Author:** Gabriel Barrientos

---

## 1. Purpose
Create a minimal bare-metal application that demonstrates GPIO control on the nRF52840 by blinking an LED at a configurable rate.

---

## 2. Requirements

### 2.1 Functional Requirements

**FR-1: LED Control**
- The application SHALL control LED1 on the nRF52840 DK
- LED1 is connected to GPIO pin P0.13
- LED1 SHALL toggle between ON and OFF states

**FR-2: Timing**
- The LED SHALL remain ON for 1000 milliseconds
- The LED SHALL remain OFF for 1000 milliseconds
- This creates a visible 1 Hz blink rate

**FR-3: Continuous Operation**
- The application SHALL run indefinitely
- The blink pattern SHALL repeat until power is removed or device is reset

### 2.2 Non-Functional Requirements

**NFR-1: Code Size**
- Total binary size SHALL NOT exceed 10 KB
- Minimize use of SDK libraries to keep size small

**NFR-2: Power Consumption**
- Use CPU sleep instructions during delays (not busy-wait loops)
- Target: <5 mA average current consumption

**NFR-3: Code Quality**
- Code SHALL compile without warnings (`-Wall -Werror`)
- All functions SHALL have descriptive comments
- Magic numbers SHALL be defined as named constants

---

## 3. Technical Specifications

### 3.1 Hardware Configuration

**GPIO Configuration:**
- Pin: P0.13
- Direction: Output
- Drive: Standard (S0S1)
- Pull: Disabled
- Initial State: Low (LED off)

**LED Characteristics:**
- Active Low (0V = ON, 3.3V = OFF)
- Forward voltage: ~2.0V
- Current: ~5 mA

### 3.2 Software Architecture

**Main Loop:**
Initialize GPIO Loop forever: Toggle LED Delay 1000ms


**Functions Required:**
- `configure_led()` - Set up GPIO pin as output
- `toggle_led()` - Change LED state
- `delay_ms(uint32_t ms)` - Blocking delay with sleep

### 3.3 Implementation Approach

**Option A: Direct Register Access**
- Manipulate GPIO registers directly
- Minimal code size (~1-2 KB)
- Educational value (learn register-level programming)

**Option B: nRF5 SDK HAL**
- Use `nrf_gpio.h` functions
- Slightly larger (~3-5 KB)
- More readable and maintainable

**RECOMMENDED:** Option B (SDK HAL) for balance of simplicity and readability.

---

## 4. Build Configuration

### 4.1 Makefile Requirements

**Compiler Flags:**
- `-mcpu=cortex-m4` - Target ARM Cortex-M4
- `-mthumb` - Use Thumb instruction set
- `-mfloat-abi=hard` - Hardware floating point
- `-O3` - Optimize for speed
- `-Wall -Werror` - All warnings as errors

**Linker Script:**
- Use: `/opt/nrf5_sdk/modules/nrfx/mdk/nrf52840_xxaa.ld`

**Required SDK Files:**
- `gcc_startup_nrf52840.S` - Startup code
- `system_nrf52840.c` - System initialization
- `nrf_delay.c` - Delay functions

### 4.2 Include Paths

/opt/nrf5_sdk/components/drivers_nrf/nrf_soc_nosd /opt/nrf5_sdk/components/toolchain/cmsis/include /opt/nrf5_sdk/modules/nrfx /opt/nrf5_sdk/modules/nrfx/hal /opt/nrf5_sdk/modules/nrfx/mdk /opt/nrf5_sdk/components/libraries/delay


---

## 5. Testing Strategy (Without Hardware)

### 5.1 Build Verification
- **Test:** `make clean && make`
- **Success Criteria:** Compilation completes without errors or warnings
- **Output:** `build/blinky.hex` exists and is 2-10 KB

### 5.2 Size Verification
- **Test:** `arm-none-eabi-size build/blinky.elf`
- **Success Criteria:** 
  - text (code) < 10 KB
  - data + bss (RAM) < 5 KB

### 5.3 Static Analysis
- **Test:** Compile with `-Wall -Werror -Wextra`
- **Success Criteria:** No warnings or errors

### 5.4 Mock Hardware Testing (Future)
- Python script simulates GPIO register reads/writes
- Verifies correct register addresses accessed
- Confirms timing behavior

---

## 6. Acceptance Criteria

The implementation is COMPLETE when:
- ✅ Code compiles without errors or warnings
- ✅ Binary size is under 10 KB
- ✅ All functions have descriptive comments
- ✅ `make flash` command is defined (even if hardware not connected)
- ✅ Code follows coding standards in CLAUDE.md

---

## 7. Future Enhancements

**Version 1.1:**
- Add button control (press to change blink rate)
- Implement multiple blink patterns

**Version 1.2:**
- Add UART logging for debug output
- Report blink count via serial

**Version 2.0:**
- Add Bluetooth Low Energy advertising
- Transmit blink count via BLE

---

## 8. References

- nRF52840 Product Specification v1.7
- nRF5 SDK v17.1.0 Documentation
- ARM Cortex-M4 Technical Reference Manual

---

**Document Status:** APPROVED  
**Implementation Status:** PENDING  
**Last Updated:** January 2026

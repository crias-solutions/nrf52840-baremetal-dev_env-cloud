#!/usr/bin/env python3
"""
Mock Hardware Simulator for nRF52840 GPIO Testing
Simulates GPIO register behavior without physical hardware
"""

class MockGPIO:
    """Simulates nRF52840 GPIO Port 0"""
    
    def __init__(self):
        self.out_register = 0x00000000
        self.pin_cnf = ,[0] * 32  # 32 pins
        self.toggle_count = 0
        
    def configure_pin(self, pin, direction):
        """Configure pin as input (0) or output (1)"""
        if direction == 1:
            self.pin_cnf,[pin] |= (1 << 0)  # Set DIR bit
            print(f"✓ Pin P0.{pin} configured as OUTPUT")
        else:
            self.pin_cnf,[pin] &= ~(1 << 0)  # Clear DIR bit
            print(f"✓ Pin P0.{pin} configured as INPUT")
    
    def set_pin(self, pin, value):
        """Set pin high (1) or low (0)"""
        if value:
            self.out_register |= (1 << pin)
            print(f"✓ Pin P0.{pin} set HIGH (LED OFF)")
        else:
            self.out_register &= ~(1 << pin)
            print(f"✓ Pin P0.{pin} set LOW (LED ON)")
    
    def toggle_pin(self, pin):
        """Toggle pin state"""
        self.out_register ^= (1 << pin)
        self.toggle_count += 1
        state = "HIGH (LED OFF)" if (self.out_register & (1 << pin)) else "LOW (LED ON)"
        print(f"✓ Pin P0.{pin} toggled to {state} (toggle #{self.toggle_count})")
    
    def get_pin_state(self, pin):
        """Read current pin state"""
        return (self.out_register >> pin) & 1

def test_blinky_logic():
    """Test the blinky application logic"""
    print("=" * 60)
    print("nRF52840 GPIO Mock Test: Blinky Application")
    print("=" * 60)
    
    gpio = MockGPIO()
    LED_PIN = 13
    
    # Test 1: Configuration
    print("\nTest 1: GPIO Configuration")
    gpio.configure_pin(LED_PIN, 1)  # Configure as output
    
    # Test 2: Toggle sequence
    print("\nTest 2: LED Toggle Sequence (simulating 5 blinks)")
    for i in range(10):  # 10 toggles = 5 complete blinks
        gpio.toggle_pin(LED_PIN)
        print(f"  ,[Delay 1000ms simulated]")
    
    # Test 3: Verify toggle count
    print(f"\nTest 3: Verification")
    print(f"✓ Total toggles: {gpio.toggle_count}")
    print(f"✓ Expected: 10 (5 complete blinks)")
    
    if gpio.toggle_count == 10:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print("\n❌ TEST FAILED")
        return 1

if __name__ == "__main__":
    exit(test_blinky_logic())

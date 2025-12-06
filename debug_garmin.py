#!/usr/bin/env python3
"""Debug script to test Garmin detection"""

import subprocess
import re

result = subprocess.run(
    ['ioreg', '-p', 'IOUSB', '-l', '-w', '0'],
    capture_output=True, text=True, timeout=10
)

output = result.stdout

# Split into device blocks
blocks = re.split(r'\+-o\s+', output)

print(f"Found {len(blocks)} device blocks\n")

for i, block in enumerate(blocks):
    # Check for Garmin signature
    sig_match = re.search(r'"UsbDeviceSignature"\s*=\s*<1e09([a-f0-9]{4})', block, re.IGNORECASE)
    vendor_match = re.search(r'"idVendor"\s*=\s*2334', block)
    
    if sig_match or vendor_match:
        print(f"=== GARMIN DEVICE FOUND IN BLOCK {i} ===")
        
        # Show signature
        full_sig = re.search(r'"UsbDeviceSignature"\s*=\s*<([^>]+)>', block)
        if full_sig:
            print(f"Full signature: <{full_sig.group(1)}>")
        
        if sig_match:
            hex_pid = sig_match.group(1)
            print(f"Product ID hex from sig: {hex_pid}")
            product_id = int(hex_pid[2:4] + hex_pid[0:2], 16)
            print(f"Product ID decimal: {product_id}")
        
        # Check idProduct field
        product_match = re.search(r'"idProduct"\s*=\s*(\d+)', block)
        if product_match:
            print(f"idProduct field: {product_match.group(1)}")
        else:
            print("idProduct field: NOT FOUND in this block")
        
        # Check idVendor field
        if vendor_match:
            print("idVendor = 2334: FOUND")
        else:
            print("idVendor = 2334: NOT in this block")
        
        # Show first 500 chars of block for context
        print(f"\nBlock preview:\n{block[:800]}\n")
        print("=" * 50)

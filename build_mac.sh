#!/bin/bash
# Build Garmin Workout Uploader for Mac
# Creates a standalone .app that users can double-click

echo "=================================="
echo "  Building Garmin Workout Uploader"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    echo "   Install from: https://python.org"
    exit 1
fi

echo "✓ Python 3 found"

# Install PyInstaller
echo "Installing PyInstaller..."
pip3 install pyinstaller --quiet --break-system-packages 2>/dev/null || pip3 install pyinstaller --quiet

echo "✓ PyInstaller ready"
echo ""
echo "Building app..."

# Build the app
pyinstaller --onefile \
    --windowed \
    --name "Garmin Workout Uploader" \
    --osx-bundle-identifier "com.garmin.workout.uploader" \
    --clean \
    --noconfirm \
    garmin_uploader_mac.py 2>/dev/null

if [ -d "dist/Garmin Workout Uploader.app" ]; then
    echo ""
    echo "=================================="
    echo "✅ BUILD SUCCESSFUL!"
    echo "=================================="
    echo ""
    echo "Your app is ready:"
    echo "  dist/Garmin Workout Uploader.app"
    echo ""
    echo "To install:"
    echo "  1. Open the 'dist' folder"
    echo "  2. Drag 'Garmin Workout Uploader' to Applications"
    echo ""
    
    # Open the dist folder
    open dist/
else
    echo ""
    echo "❌ Build failed. Try running directly instead:"
    echo "   python3 garmin_uploader_mac.py"
fi

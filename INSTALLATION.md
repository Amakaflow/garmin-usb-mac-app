# Garmin Workout Uploader - Installation Instructions

## Windows Installation

1. Download `GarminWorkoutUploaderSetup.exe` from the [latest release](https://github.com/supergeri/garmin-usb-mac-app/releases/latest)
2. Run the installer
3. Follow the installation wizard
4. The app will be installed to `C:\Program Files\Garmin Workout Uploader`
5. A desktop shortcut will be created (optional)

## macOS Installation

### Download and Install

1. Download `GarminWorkoutUploader-X.X.X.dmg` from the [latest release](https://github.com/supergeri/garmin-usb-mac-app/releases/latest)
2. Open the DMG file
3. Drag "Garmin Workout Uploader.app" to your Applications folder

### Bypass Gatekeeper (Required for unsigned apps)

Since this app is not code-signed by Apple, macOS Gatekeeper will block it from opening. Follow these steps:

#### Option 1: Right-click method (Recommended)
1. Locate the app in your Applications folder
2. **Right-click** (or Control-click) on "Garmin Workout Uploader.app"
3. Select **"Open"** from the context menu
4. Click **"Open"** in the dialog that appears
5. The app will now open and be added to your approved apps list

#### Option 2: System Settings method
1. Try to open the app normally (it will be blocked)
2. Open **System Settings** → **Privacy & Security**
3. Scroll down to the **Security** section
4. You'll see a message: "Garmin Workout Uploader was blocked from use..."
5. Click **"Open Anyway"**
6. Confirm by clicking **"Open"**

#### Option 3: Terminal method (Advanced)
If the above methods don't work, you can remove the quarantine attribute:

```bash
xattr -dr com.apple.quarantine "/Applications/Garmin Workout Uploader.app"
```

Then open the app normally.

### Why is this needed?

This app is not code-signed with an Apple Developer certificate, which would cost $99/year. The app is open-source and safe to use, but macOS Gatekeeper will block unsigned apps by default to protect users.

## Troubleshooting

### macOS: "App is damaged and can't be opened"
This is another Gatekeeper message. Use Option 3 (Terminal method) above to remove the quarantine attribute.

### Windows: SmartScreen warning
Windows Defender SmartScreen may show a warning because the app isn't signed with a code-signing certificate. Click "More info" → "Run anyway" to proceed.

### App won't detect my Garmin device
- **Windows**: Make sure no other Garmin software (like Garmin Express) is running
- **macOS**: Ensure your Garmin device is properly connected via USB
- Try unplugging and reconnecting your device
- Check that your device appears in File Explorer (Windows) or Finder (macOS)

## Auto-Updates

Once installed, the app will automatically check for updates on startup. When a new version is available, you'll see a notification banner with a download button.

## System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.13 (High Sierra) or later
- Python is **not** required - the app is self-contained

## Support

For issues, please open an issue on [GitHub](https://github.com/supergeri/garmin-usb-mac-app/issues).

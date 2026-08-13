# Gym Registration — Android App Plan

## Project Structure

```
gym_register_android/
├── main.py          ← Kivy/KivyMD UI (all screens)
├── database.py      ← SQLite database (offline, same logic as desktop)
├── buildozer.spec   ← APK build config
├── requirements.txt ← Desktop testing deps only
└── plan.md          ← This file
```

---

## Phase 1 — Test on Mac (Desktop Preview)

Install dependencies and run locally first. No Android needed yet.

```bash
cd ~/Desktop/work_nipam/working_projects/gym_register_android
pip install kivy==2.3.0 kivymd==1.2.0
python main.py
```

The app opens in a window on your Mac.  
Test all features: Add, Edit, Delete, Search, tabs (All / Active / Expired).

---

## Phase 2 — Build APK (Linux required)

Buildozer (the Python-to-Android tool) only runs on Linux.  
On macOS you have two options:

---

### Option A — Docker (Easiest on Mac, recommended)

#### Install Docker Desktop
https://www.docker.com/products/docker-desktop/

#### Pull the Buildozer image
```bash
docker pull kivy/buildozer
```

#### Build the APK
```bash
cd ~/Desktop/work_nipam/working_projects/gym_register_android

docker run --volume "$(pwd)":/home/user/hostcwd kivy/buildozer android debug
```

First build takes 20–40 minutes (downloads Android SDK/NDK).  
Subsequent builds: ~2–5 minutes.

**Output APK location:**
```
bin/gymregister-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

---

### Option B — Ubuntu VM (VirtualBox / UTM)

1. Install Ubuntu 22.04
2. Inside Ubuntu terminal:

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk autoconf libtool

pip3 install buildozer cython

# Copy your project into the VM or mount the folder
cd /path/to/gym_register_android
buildozer android debug
```

---

## Phase 3 — Install APK on Android Phone

### Enable Developer Mode on your phone
1. `Settings → About Phone → tap "Build Number" 7 times`
2. `Settings → Developer Options → enable USB Debugging`

### Connect phone via USB and install via adb

```bash
# Install adb on Mac
brew install android-platform-tools

# Verify phone is detected (should show your device)
adb devices

# Install APK directly to phone
adb install bin/gymregister-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

### Alternative — Manual install (no USB needed)
1. Copy the `.apk` file to your phone (USB / Google Drive / WhatsApp)
2. On phone: `Settings → Apps → Install unknown apps → allow your file manager`
3. Tap the `.apk` file to install

---

## Phase 4 — Debug on Device

### Stream live logs from phone to Mac
```bash
adb logcat | grep -i python
```
All `print()` statements and Python tracebacks appear here.

### Faster debug cycle
```bash
# Build + install + launch in one command (phone must be connected via USB)
buildozer android debug deploy run
```

### Common errors and fixes

| Error | Fix |
|---|---|
| `sdk not found` | Let buildozer auto-download it (first run) |
| `BUILD FAILED` in Java | Check `android.api = 33` in buildozer.spec |
| App crashes on launch | Run `adb logcat \| grep python` to see traceback |
| White/black screen | KV string syntax error — check indentation in main.py |
| `kivymd not found` | Confirm `kivymd==1.2.0` is in `requirements` line in buildozer.spec |

---

## Phase 5 — Release APK (for sharing, not Play Store)

To create a release (signed) APK others can install without warnings:

```bash
# Generate a keystore (do this once, keep it safe)
keytool -genkey -v -keystore gym_release.keystore -alias gym -keyalg RSA -keysize 2048 -validity 10000

# Build release APK
buildozer android release
```

Then sign it:
```bash
apksigner sign --ks gym_release.keystore bin/gymregister-1.0-release-unsigned.apk
```

---

## App Features (Android version)

| Feature | Status |
|---|---|
| Add customer | ✅ |
| Edit customer | ✅ |
| Delete customer (with confirm dialog) | ✅ |
| View customer details | ✅ |
| Tabs: All / Active / Expired | ✅ |
| Search by name or phone | ✅ |
| Offline SQLite database | ✅ |
| Date picker | ✅ |
| Period quick-select (1/3/6/12 months) | ✅ |
| Excel export | ❌ (no file dialog on Android — can add later) |

---

## Toolkit Summary

| Tool | Purpose |
|---|---|
| Kivy 2.3.0 | Python UI framework for Android/iOS/Desktop |
| KivyMD 1.2.0 | Material Design components for Kivy |
| SQLite3 | Offline local database (built into Python/Android) |
| Buildozer | Compiles Python app → APK |
| adb | Android Debug Bridge — install APKs, stream logs |
| Docker | Runs Buildozer on macOS without a VM |

---

## File Roles

### `main.py`
- All UI screens defined in KV language string
- `HomeScreen` — customer list with search + tabs
- `AddEditScreen` — add/edit form with date picker
- `DetailScreen` — read-only customer details
- `GymApp` — app logic (navigation, CRUD calls, refresh)

### `database.py`
- Same logic as desktop version
- Auto-detects Android storage path vs desktop path
- All SQLite operations: add, update, delete, query, status check

### `buildozer.spec`
- App name, package ID, version
- Python/Kivy requirements list
- Android API targets, permissions, architectures

---

## Development Tips

- Always test on desktop (`python main.py`) before building APK
- Keep `buildozer.spec` `requirements` line in sync with actual imports
- KV indentation errors cause silent blank screens — use 4 spaces consistently
- `adb logcat | grep python` is your best friend for debugging crashes
- The SQLite `.db` file is stored in the app's private storage on Android — data persists across app restarts

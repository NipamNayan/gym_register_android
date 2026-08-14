# Gym Registration — Android App Plan

---

## How This App Was Created (Full Journey)

### Step 1 — Analysed the original desktop app

The original app (`gym_register/`) was built with:
- `tkinter` for the UI (desktop only, won't run on Android)
- `sqlite3` for local storage
- `pandas` + `openpyxl` for Excel export

Since tkinter is desktop-only, a full UI rewrite was needed for Android.

### Step 2 — Chose the tech stack

| Need | Choice | Reason |
|---|---|---|
| Mobile UI | Kivy + KivyMD | Python-native, runs on Android/iOS/Desktop |
| Database | SQLite3 (built-in) | Same as desktop, no extra dependency |
| CSV export | Python `csv` module | Built-in, no pip package needed on Android |
| APK build | Buildozer | Standard Python-to-Android tool |
| CI/CD | GitHub Actions | Free Linux runners — Buildozer needs Linux |

### Step 3 — Wrote `database.py`

Ported the desktop database logic with two key changes:
- Auto-detects Android storage path (`android.storage.app_storage_path`) vs desktop path
- Removed `pandas` dependency (not needed for CSV; use stdlib `csv` instead)
- Added `export_to_csv()` method (saves to `/sdcard/Download/` on Android)

### Step 4 — Wrote `main.py` (Kivy UI)

Three screens built with KV language + Python:
- `HomeScreen` — tabbed list (All / Active / Expired) + search bar + CSV export buttons
- `AddEditScreen` — form with date picker + period quick-select buttons (1/3/6/12 months)
- `DetailScreen` — read-only customer card + edit shortcut

App class (`GymApp`) handles all navigation and database calls.

### Step 5 — Wrote `buildozer.spec`

Key settings that matter:
```ini
requirements = kivy==2.3.0,kivymd==1.2.0,pillow
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
```

> **What NOT to put in requirements:** `python3` and `sqlite3` are runtime builtins,
> not pip packages. Listing them causes buildozer to fail trying to `pip install` them.

### Step 6 — Set up GitHub Actions (because Buildozer needs Linux)

Docker was installed on the Mac but the Docker daemon wasn't running.
Rather than requiring Docker Desktop to be open manually every time, GitHub Actions
was used — it spins up a free Ubuntu 22.04 runner automatically on every push.

Workflow file: `.github/workflows/build_android.yml`

Key decisions in the workflow:
- `ubuntu-22.04` not `ubuntu-24.04` — `libtinfo5` was removed in 24.04, breaking buildozer
- `python-version: "3.10"` not 3.11 — better python-for-android recipe compatibility
- `yes | buildozer` — auto-accepts any interactive prompts during build
- Cache `~/.buildozer` keyed on `buildozer.spec` hash — avoids re-downloading SDK/NDK
- On failure: upload `build.log` as artifact so errors are visible without sign-in

### Step 7 — Fixed two failed builds

**Run #1 failed** — `requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlite3`
- `python3` and `sqlite3` are not pip packages → buildozer crashed trying to install them

**Run #2 failed in 13 seconds** — pinned action versions that don't exist as Git tags
(`@v4.2.2`, `@v4.2.3`, `@v4.6.2`, `@v5.6.0`) → GitHub couldn't resolve the actions

**Run #3** — both fixed, build progresses correctly.

### Step 8 — Downloading and installing the APK

Once GitHub Actions shows a green checkmark:
1. Actions tab → click the run → scroll to **Artifacts**
2. Download `gym-register-apk.zip` → unzip → get `.apk`
3. Install via `adb install` (USB) or copy to phone and tap

---

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
| CSV export (All / Active / Expired) | ✅ (saved to Downloads) |
| Excel export | ❌ (no file dialog on Android) |

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

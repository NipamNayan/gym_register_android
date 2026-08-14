# Gym Registration — Android App

Offline Android app for managing gym customer registrations. Built with Python (Kivy + KivyMD), SQLite storage, and packaged as an APK via Buildozer.

---

## Features

- Add, edit, delete gym customers
- Tabs: All / Active / Expired subscriptions
- Search by name or phone
- Date picker + quick period buttons (1 / 3 / 6 / 12 months)
- Export data to CSV (saved to Downloads on Android)
- 100% offline — SQLite database, no internet required

---

## Project Structure

```
gym_register_android/
├── main.py                              ← Kivy/KivyMD UI (all screens)
├── database.py                          ← SQLite database layer
├── buildozer.spec                       ← APK build configuration
├── requirements.txt                     ← Desktop testing deps only
├── plan.md                              ← Detailed build & deploy guide
└── .github/workflows/build_android.yml ← GitHub Actions APK builder
```

---

## Desktop Testing (Mac/Linux/Windows)

Run the app locally before building the APK:

```bash
pip install kivy==2.3.0 kivymd==1.2.0
python main.py
```

---

## Building the APK

Buildozer (Python → APK) requires Linux. On macOS, use **GitHub Actions** (free):

### 1. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/gym_register_android.git
git push -u origin main
```

### 2. GitHub builds automatically

- Go to your repo → **Actions** tab
- "Build Android APK" workflow starts on every push
- First build: ~25–35 min (downloads Android SDK/NDK)
- Subsequent builds: ~5–10 min (cached)

### 3. Download the APK

Actions run → scroll to **Artifacts** → download `gym-register-apk.zip` → unzip to get the `.apk`.

> If the build fails, a `build-log` artifact is also uploaded so you can see the full error.

---

## Installing on Android

### Via USB (recommended)

```bash
brew install android-platform-tools   # macOS only, once
adb devices                           # verify phone is detected
adb install bin/gymregister-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

Enable **USB Debugging** on your phone first:  
`Settings → About Phone → tap Build Number 7 times → Developer Options → USB Debugging`

### Manual install

Copy the `.apk` to your phone and tap it. You'll need:  
`Settings → Apps → Install unknown apps → enable for your file manager`

---

## Debugging on Device

```bash
# Stream Python logs from the connected phone
adb logcat | grep -i python
```

---

## CSV Export

Tap the **EXPORT (CSV)** button at the bottom of any tab.  
Files are saved to `/sdcard/Download/` on Android and can be opened in Google Sheets.

---

## Build Notes

| Setting | Value |
|---|---|
| Python | 3.10 |
| Kivy | 2.3.0 |
| KivyMD | 1.2.0 |
| Android API target | 33 |
| Android min API | 21 (Android 5.0+) |
| Architectures | arm64-v8a, armeabi-v7a |
| CI runner | ubuntu-22.04 |


# 🔥 Firebase Lurker 🚀

Welcome to the **Firebase Lurker**! This nifty tool helps you decompile APK files and sniff out Firebase misconfigurations (you know, the kind that might expose juicy backend URLs 👀). Secure your app before it's too late! 🔐

![firebase-lurker](https://github.com/user-attachments/assets/7a55cbcc-b9c6-41cb-9ed5-331f7afd9768)

## 💡 What does it do?

This script decompiles Android APKs, scans the source code, and extracts any suspicious Firebase links (like `.firebaseapp.com` and `.firebaseio.com`). It'll also display the hash of the APK you're analyzing and make sure you're not missing any potential misconfigurations lurking in the shadows 🕵️‍♂️.

### ⚙️ Features:

- 🚀 **Automated APK decompilation** using `apktool`.
- 🔎 **Scans for Firebase links** to check for possible misconfigurations.
- 💾 **Stores results** in a directory named after your APK + its SHA256 hash.
- 🌈 **Stylish output** with color-coded messages and gradient ASCII art to make hacking more fun!

## 🔧 How to use

1. **Clone this repo** or just grab the script.
2. Make sure `apktool` is in the right directory (check the `dependencies/` folder for the `.jar` file).
3. **Run the script** with:

```bash
python firebase-lurker.py --path <APK file>
```

- `--path`: The path to your APK file. This is **required**.

### Example:

```bash
python firebase-lurker.py --path /Downloads/myApp.apk
```

> **Pro tip**: If you've already decompiled this APK, the script will skip re-decompilation and jump straight to scanning Firebase URLs.

## 🚨 Missing Arguments?

If you're missing any required arguments or entered something wrong, you'll see this message:

```bash
APK File Not Found.
```

Make sure your APK file path is correct and that you include the `--path` argument.

## 💥 Cool ASCII Art 💻

Check out the sick ASCII art in the output! 🖥️ Your terminal will thank you for it.

## 📜 License

Feel free to use, modify, or contribute to this project under the [MIT License](LICENSE).

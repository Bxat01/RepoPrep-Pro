# 🚀 RepoPrep Pro v2.2.0
**Professional Project Cleaner & AI Context Preparer** *Built with reputation by **Lidprex Labs***

---

## 🌟 Overview
**RepoPrep Pro v2.2.0** is the next generation of project management tools. While v1.1.0 focused on basic cleanup, this version is a high-performance engine designed for modern developers who work with **LLMs (AI)** and massive codebases (100,000+ files).

Moving away from PySide6, this version is built on a **Zero-Dependency** architecture using native Python `tkinter`, making it the most lightweight and portable version ever released by **Lidprex Labs**.

---

## 🆕 What's New in v2.2.0?
* **🌍 Global Support:** Full localization for **English, Arabic, Russian, and Chinese**.
* **🤖 AI Flatten Mode:** Specifically designed to prepare codebases for ChatGPT/Claude by removing folder depth.
* **⚡ Zero-Dependency:** Runs out of the box with standard Python. No external libraries needed.
* **📊 Live Stats:** Real-time scanning that shows project type and potential space savings.
* **🎨 Modern UI:** A sleek, dark-themed interface with batch-optimized logging for speed.

---

## 🛠 Operation Modes

| Mode | Function | Ideal For |
| :--- | :--- | :--- |
| **Flatten & Prepare for AI** | Copies all source files into a single flat folder. | Sending code to AI prompts. |
| **Smart Clean** | Removes junk files while keeping your folder structure. | Clean backups & GitHub uploads. |
| **Scan Only** | Analyzes files and shows stats without touching anything. | Pre-operation check. |

---

## 🧹 Automated Cleaning Logic
RepoPrep Pro automatically identifies and excludes:
* **Dependencies:** `node_modules`, `venv`, `.gradle`, `site-packages`.
* **Builds:** `dist`, `build`, `target`, `bin`, `out`.
* **Caches:** `__pycache__`, `.next`, `.nuxt`, `.pytest_cache`.
* **Locks:** `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`.
* **System/Logs:** `.log`, `.tmp`, `.DS_Store`, `Thumbs.db`.

---

## 🚀 Quick Start

### Run from Source
```bash
python main.py
Build for Windows (.exe)
Requires pyinstaller. Use the included build script:
```
```Bash
build.bat
📜 License & Credits
Developer: Lidprex Labs

Version: 2.2.0 (Stable Release)

License: MIT License — © 2026

"Building products with reputation, not noise."


---
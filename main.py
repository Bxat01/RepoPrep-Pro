"""
RepoPrep Pro v2.2.0 — Built by Lidprex Labs
https://lidprex-labs.onrender.com/
Supports: English / Arabic / Russian / Chinese
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import shutil
import gc
import ctypes
from pathlib import Path
from datetime import datetime
import webbrowser
import math as _math

# ══════════════════════════════════════════════════════════════════
#  ICON HELPER
# ══════════════════════════════════════════════════════════════════
def get_icon_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, "icon.ico")
    return icon_path if os.path.exists(icon_path) else None

# ══════════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════════════
LANGS = {
    "en": {
        "app_title":         "RepoPrep Pro — Lidprex Labs",
        "built_by":          "Built by",
        "lang_label":        "Language",
        "paths_title":       "Project Paths",
        "source_label":      "Source — project folder",
        "target_label":      "Output — where results will be saved",
        "browse":            "Browse",
        "modes_title":       "Operation Mode",
        "mode_flatten":      "Flatten & Prepare for AI",
        "mode_flatten_d":    "Copies all files into one flat folder with no subfolders. Ideal for sending your entire codebase to an AI tool.",
        "mode_clean":        "Smart Clean",
        "mode_clean_d":      "Removes node_modules, venv, .git, build artifacts and caches. Preserves the original folder structure.",
        "mode_scan":         "Scan Only",
        "mode_scan_d":       "Analyzes the project and shows what would be removed. Nothing is copied or deleted.",
        "options_title":     "Options",
        "opt_images":        "Include image files  (.png .jpg .gif .svg .webp ...)",
        "opt_images_hint":   "Images are excluded by default to keep the output lightweight. Enable this if your project depends on image assets.",
        "actions_title":     "Actions",
        "btn_run":           "Run",
        "btn_scan":          "Scan",
        "btn_clear":         "Clear Log",
        "btn_open":          "Open Output Folder",
        "log_title":         "Activity Log",
        "stats_default":     "Select a source project to begin.",
        "warn_no_src":       "Please select a source project folder.",
        "warn_no_tgt":       "Please select an output folder.",
        "err_no_src":        "Source folder not found:\n{}",
        "confirm_overwrite": "'{}' already has files.\n\nContinue and merge / overwrite?",
        "done_title":        "Complete!",
        "done_msg":          "Operation finished.\n\n  Copied : {} files\n  Skipped: {} items\n\nOpen the output folder?",
        "fail_title":        "Failed",
        "fail_msg":          "Operation failed — check the log for details.",
        "no_output":         "No output folder selected or it does not exist yet.",
        "running":           "Running...",
        "scan_type":         "Project type",
        "scan_total":        "Total",
        "scan_after":        "After clean",
        "scan_dirs":         "Dirs skipped",
        "scan_files_s":      "Files skipped",
        "stats_fmt":         "{type}  ·  {tf} files ({tm} MB)  →  {cf} clean files ({cm} MB)  ·  Removes: {sd} dirs, {sf} files  (saves ~{sv} MB)",
        "footer_tagline":    "Building products with reputation, not noise",
    },
    "ar": {
        "app_title":         "RepoPrep Pro — Lidprex Labs",
        "built_by":          "من تطوير",
        "lang_label":        "اللغة",
        "paths_title":       "مسارات المشروع",
        "source_label":      "المصدر — مجلد المشروع",
        "target_label":      "الإخراج — مكان حفظ النتائج",
        "browse":            "تصفح",
        "modes_title":       "وضع التشغيل",
        "mode_flatten":      "تسطيح المشروع للذكاء الاصطناعي",
        "mode_flatten_d":    "ينسخ جميع الملفات في مجلد واحد بدون مجلدات فرعية. مثالي لإرسال المشروع كاملاً لأداة ذكاء اصطناعي.",
        "mode_clean":        "تنظيف ذكي",
        "mode_clean_d":      "يحذف node_modules وvenv و.git وملفات البناء والكاش. يحافظ على هيكل المجلدات الأصلي.",
        "mode_scan":         "فحص فقط",
        "mode_scan_d":       "يحلل المشروع ويُظهر ما سيُحذف. لا يتم نسخ أو حذف أي ملف.",
        "options_title":     "الخيارات",
        "opt_images":        "تضمين ملفات الصور  (.png .jpg .gif .svg .webp ...)",
        "opt_images_hint":   "الصور مستبعدة افتراضياً لتخفيف حجم الإخراج. فعّل هذا الخيار إذا كان مشروعك يعتمد على ملفات الصور.",
        "actions_title":     "الإجراءات",
        "btn_run":           "تشغيل",
        "btn_scan":          "فحص",
        "btn_clear":         "مسح السجل",
        "btn_open":          "فتح مجلد الإخراج",
        "log_title":         "سجل النشاط",
        "stats_default":     "اختر مجلد المشروع للبدء.",
        "warn_no_src":       "الرجاء تحديد مجلد المشروع المصدر.",
        "warn_no_tgt":       "الرجاء تحديد مجلد الإخراج.",
        "err_no_src":        "مجلد المصدر غير موجود:\n{}",
        "confirm_overwrite": "'{}' يحتوي بالفعل على ملفات.\n\nهل تريد المتابعة والدمج/الكتابة فوقه؟",
        "done_title":        "اكتمل!",
        "done_msg":          "تمت العملية بنجاح.\n\n  منسوخ : {} ملف\n  متجاوَز: {} عنصر\n\nفتح مجلد الإخراج؟",
        "fail_title":        "فشل",
        "fail_msg":          "فشلت العملية — راجع السجل لمعرفة التفاصيل.",
        "no_output":         "لم يتم تحديد مجلد إخراج أو أنه غير موجود بعد.",
        "running":           "جارٍ التشغيل...",
        "scan_type":         "نوع المشروع",
        "scan_total":        "الإجمالي",
        "scan_after":        "بعد التنظيف",
        "scan_dirs":         "مجلدات متجاوَزة",
        "scan_files_s":      "ملفات متجاوَزة",
        "stats_fmt":         "{type}  ·  {tf} ملف ({tm} MB)  →  {cf} ملف نظيف ({cm} MB)  ·  يزيل: {sd} مجلد، {sf} ملف  (يوفر ~{sv} MB)",
        "footer_tagline":    "نبني منتجات بسمعة راسخة، لا بضجيج",
    },
    "ru": {
        "app_title":         "RepoPrep Pro — Lidprex Labs",
        "built_by":          "Создано",
        "lang_label":        "Язык",
        "paths_title":       "Пути проекта",
        "source_label":      "Источник — папка проекта",
        "target_label":      "Вывод — куда сохранить результат",
        "browse":            "Обзор",
        "modes_title":       "Режим работы",
        "mode_flatten":      "Сжать для ИИ",
        "mode_flatten_d":    "Копирует все файлы в одну плоскую папку без вложенных. Идеально для отправки кодовой базы в ИИ-инструмент.",
        "mode_clean":        "Умная очистка",
        "mode_clean_d":      "Удаляет node_modules, venv, .git, артефакты сборки и кэш. Сохраняет исходную структуру папок.",
        "mode_scan":         "Только сканирование",
        "mode_scan_d":       "Анализирует проект и показывает, что будет удалено. Файлы не копируются и не удаляются.",
        "options_title":     "Параметры",
        "opt_images":        "Включить файлы изображений  (.png .jpg .gif .svg .webp ...)",
        "opt_images_hint":   "Изображения исключены по умолчанию. Включите, если проект зависит от графических ресурсов.",
        "actions_title":     "Действия",
        "btn_run":           "Запустить",
        "btn_scan":          "Сканировать",
        "btn_clear":         "Очистить лог",
        "btn_open":          "Открыть папку вывода",
        "log_title":         "Журнал активности",
        "stats_default":     "Выберите папку проекта для начала.",
        "warn_no_src":       "Пожалуйста, выберите исходную папку проекта.",
        "warn_no_tgt":       "Пожалуйста, выберите папку вывода.",
        "err_no_src":        "Исходная папка не найдена:\n{}",
        "confirm_overwrite": "'{}' уже содержит файлы.\n\nПродолжить и объединить/перезаписать?",
        "done_title":        "Готово!",
        "done_msg":          "Операция завершена.\n\n  Скопировано: {} файлов\n  Пропущено  : {} элементов\n\nОткрыть папку вывода?",
        "fail_title":        "Ошибка",
        "fail_msg":          "Операция не удалась — проверьте журнал.",
        "no_output":         "Папка вывода не выбрана или ещё не существует.",
        "running":           "Выполняется...",
        "scan_type":         "Тип проекта",
        "scan_total":        "Всего",
        "scan_after":        "После очистки",
        "scan_dirs":         "Папок пропущено",
        "scan_files_s":      "Файлов пропущено",
        "stats_fmt":         "{type}  ·  {tf} файлов ({tm} MB)  →  {cf} чистых ({cm} MB)  ·  Удалит: {sd} папок, {sf} файлов  (сэкономит ~{sv} MB)",
        "footer_tagline":    "Создаём продукты с репутацией, без шума",
    },
    "zh": {
        "app_title":         "RepoPrep Pro — Lidprex Labs",
        "built_by":          "开发者",
        "lang_label":        "语言",
        "paths_title":       "项目路径",
        "source_label":      "源目录 — 项目文件夹",
        "target_label":      "输出目录 — 保存结果的位置",
        "browse":            "浏览",
        "modes_title":       "操作模式",
        "mode_flatten":      "扁平化输出（为AI准备）",
        "mode_flatten_d":    "将所有文件复制到一个扁平文件夹中，无子目录。非常适合将整个代码库发送到AI工具。",
        "mode_clean":        "智能清理",
        "mode_clean_d":      "删除node_modules、venv、.git、构建产物和缓存。保留原始文件夹结构。",
        "mode_scan":         "仅扫描",
        "mode_scan_d":       "分析项目并显示将被删除的内容。不复制或删除任何文件。",
        "options_title":     "选项",
        "opt_images":        "包含图片文件  (.png .jpg .gif .svg .webp ...)",
        "opt_images_hint":   "默认排除图片以减小输出体积。如果项目依赖图片资源，请启用此选项。",
        "actions_title":     "操作",
        "btn_run":           "运行",
        "btn_scan":          "扫描",
        "btn_clear":         "清除日志",
        "btn_open":          "打开输出文件夹",
        "log_title":         "活动日志",
        "stats_default":     "请选择源项目文件夹以开始。",
        "warn_no_src":       "请选择源项目文件夹。",
        "warn_no_tgt":       "请选择输出文件夹。",
        "err_no_src":        "源文件夹未找到：\n{}",
        "confirm_overwrite": "'{}' 已包含文件。\n\n是否继续合并/覆盖？",
        "done_title":        "完成！",
        "done_msg":          "操作已完成。\n\n  已复制：{} 个文件\n  已跳过：{} 个项目\n\n是否打开输出文件夹？",
        "fail_title":        "失败",
        "fail_msg":          "操作失败 — 请检查日志了解详情。",
        "no_output":         "未选择输出文件夹或该文件夹尚不存在。",
        "running":           "正在运行...",
        "scan_type":         "项目类型",
        "scan_total":        "总计",
        "scan_after":        "清理后",
        "scan_dirs":         "已跳过目录",
        "scan_files_s":      "已跳过文件",
        "stats_fmt":         "{type}  ·  共 {tf} 个文件 ({tm} MB)  →  {cf} 个干净文件 ({cm} MB)  ·  将删除: {sd} 目录, {sf} 文件  (节省约 {sv} MB)",
        "footer_tagline":    "以口碑打造产品，而非喧嚣",
    },
}

LANG_NAMES = {
    "en": "English",
    "ar": "العربية",
    "ru": "Русский",
    "zh": "中文",
}

# ══════════════════════════════════════════════════════════════════
#  CORE LOGIC  (speed-optimised — batch logging, early skip)
# ══════════════════════════════════════════════════════════════════
SKIP_DIRS = {
    '.git', '.svn', '.hg', '.bzr',
    '.idea', '.vscode', '.vs', '.sublime-project', '.sublime-workspace',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.coverage',
    '.tox', '.hypothesis', '.eggs', '.egg-info',
    'node_modules', '.npm', '.yarn', '.pnp', '.pnpm-store',
    'dist', 'build', 'target', 'out', 'bin', 'obj',
    '.next', '.nuxt', '.gatsby', 'next', 'nuxt',
    'venv', '.venv', 'env', 'ENV', 'virtualenv',
    '.gradle', '.m2',
    'Pods', '.xcworkspace', '.xcodeproj',
    'site-packages', 'dist-packages', '.nyc_output', 'coverage',
    '.DS_Store', '__MACOSX',
}
SKIP_EXTENSIONS = {
    '.log', '.tmp', '.bak', '.swp', '.swo',
    '.pyc', '.pyo', '.pyd', '.so', '.dll',
    '.class', '.jar', '.o', '.a', '.lib', '.lock',
    '.zip', '.tar', '.gz', '.rar', '.7z', '.exe',
    '.mp4', '.mp3', '.avi', '.mov', '.mkv',
    '.ttf', '.woff', '.woff2', '.eot', '.pdf',
}
SKIP_FILES = {
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.env.local', '.env.production', '.env.development',
    '.gitkeep', '.keep',
}
IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp', '.bmp'}


def detect_type(path: Path) -> str:
    checks = [
        (["package.json"],                                  "Node.js / JavaScript"),
        (["requirements.txt", "setup.py", "pyproject.toml"], "Python"),
        (["pom.xml"],                                        "Java (Maven)"),
        (["build.gradle"],                                   "Java (Gradle)"),
        (["pubspec.yaml"],                                   "Flutter / Dart"),
        (["composer.json"],                                  "PHP"),
        (["Gemfile"],                                        "Ruby"),
        (["go.mod"],                                         "Go"),
        (["Cargo.toml"],                                     "Rust"),
        (["CMakeLists.txt"],                                 "C / C++ (CMake)"),
        (["Makefile"],                                       "C / C++ (Make)"),
    ]
    for files, ptype in checks:
        if any((path / f).exists() for f in files):
            return ptype
    return "Generic"


def _first_skip_dir(parts):
    for p in parts[:-1]:
        if p in SKIP_DIRS:
            return p
    return None


def scan_project(source_dir: str, include_images: bool = False) -> dict:
    path     = Path(source_dir)
    skip_ext = SKIP_EXTENSIONS | (set() if include_images else IMAGE_EXT)
    stats = {
        "total_files": 0, "clean_files": 0,
        "skipped_dirs": 0, "skipped_files": 0,
        "total_size": 0, "clean_size": 0,
        "project_type": detect_type(path), "skippable": {},
    }
    seen: set = set()

    for item in path.rglob("*"):
        try:
            rel   = item.relative_to(path)
            parts = rel.parts

            if item.is_dir():
                if item.name in SKIP_DIRS and item.name not in seen:
                    seen.add(item.name)
                    stats["skipped_dirs"] += 1
                    try:
                        stats["skippable"][item.name] = sum(
                            f.stat().st_size for f in item.rglob("*") if f.is_file())
                    except Exception:
                        stats["skippable"][item.name] = 0
                continue

            if not item.is_file():
                continue

            sz = 0
            try: sz = item.stat().st_size
            except Exception: pass

            stats["total_files"] += 1
            stats["total_size"]  += sz

            skip_dir = _first_skip_dir(parts)
            skip = (
                skip_dir is not None
                or item.name in SKIP_DIRS
                or item.name in SKIP_FILES
                or item.suffix.lower() in skip_ext
            )
            if skip:
                stats["skipped_files"] += 1
            else:
                stats["clean_files"] += 1
                stats["clean_size"]  += sz
        except Exception:
            continue
    return stats


def run_operation(source_dir, target_dir, mode, include_images=False,
                  log_cb=None, progress_cb=None):
    source   = Path(source_dir)
    target   = Path(target_dir)
    skip_ext = SKIP_EXTENSIONS | (set() if include_images else IMAGE_EXT)

    def log(msg, level="INFO"):
        if log_cb:
            log_cb(f"[{datetime.now().strftime('%H:%M:%S')}]  {msg}", level)

    if not source.exists():
        log("Source folder not found.", "ERROR"); return False
    try:
        target.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        log(f"Cannot create output: {e}", "ERROR"); return False

    copied = 0; skipped = 0; name_cnt: dict = {}

    def unique(fname):
        if fname not in name_cnt:
            name_cnt[fname] = 0; return fname
        name_cnt[fname] += 1
        stem, ext = Path(fname).stem, Path(fname).suffix
        return f"{stem}__{name_cnt[fname]}{ext}"

    all_files = [f for f in source.rglob("*") if f.is_file()]
    total     = len(all_files)
    log(f"Found {total} files — processing...", "INFO")

    skipped_dirs_logged: set = set()
    BATCH    = 75
    last_log = 0

    for idx, item in enumerate(all_files):
        try:
            rel      = item.relative_to(source)
            parts    = rel.parts
            skip_dir = _first_skip_dir(parts)

            # log each skipped directory only ONCE
            if skip_dir and skip_dir not in skipped_dirs_logged:
                skipped_dirs_logged.add(skip_dir)
                log(f"Skip  {skip_dir}/  (directory skipped)", "SKIP")

            skip = (
                skip_dir is not None
                or item.name in SKIP_DIRS
                or item.name in SKIP_FILES
                or item.suffix.lower() in skip_ext
            )

            if skip:
                skipped += 1
            else:
                if mode == "flatten":
                    dest = target / unique(item.name)
                else:
                    dest = target / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                copied += 1

            if progress_cb and total > 0:
                progress_cb(int((idx + 1) / total * 100))

            # batch summary log (much faster than per-file)
            if (idx - last_log) >= BATCH:
                log(f"Progress  {idx+1}/{total}  —  copied {copied}, skipped {skipped}", "INFO")
                last_log = idx
                gc.collect()

        except Exception as e:
            log(f"Error {item.name}: {e}", "WARN")
            skipped += 1

    log(f"Done — {copied} copied, {skipped} skipped.", "DONE")
    return {"copied": copied, "skipped": skipped}


# ══════════════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ══════════════════════════════════════════════════════════════════
C = {
    "bg":        "#080812",
    "surface":   "#0f0f1e",
    "surface2":  "#171728",
    "surface3":  "#1e1e36",
    "border":    "#24244a",
    "sel_bg":    "#1a1a40",
    "sel_brd":   "#7c6dfa",
    "accent":    "#7c6dfa",
    "accent2":   "#fa6d8b",
    "accent3":   "#38e5a0",
    "text":      "#e4e4f4",
    "muted":     "#50507a",
    "warning":   "#f5a623",
    "error":     "#fa6d6d",
    "success":   "#38e5a0",
    "copy_fg":   "#7ae89a",
    "skip_fg":   "#2e2e56",
    "warn_fg":   "#f5a623",
    "done_fg":   "#38e5a0",
    "info_fg":   "#7a9afa",
    "scan_fg":   "#b090ff",
    "footer_bg": "#05050e",
    "title_bg":  "#06060e",
}

# ══════════════════════════════════════════════════════════════════
#  ICON DRAWING
# ══════════════════════════════════════════════════════════════════
def _draw(canvas, name, s, col):
    h = s // 2
    if name == "folder":
        canvas.create_polygon(2, h, 7, h, 9, h-3, s-2, h-3,
                              s-2, s-3, 2, s-3, fill=col, outline="")
    elif name == "scan":
        canvas.create_oval(3, 3, s-6, s-6, outline=col, width=2)
        canvas.create_line(s-6, s-6, s-2, s-2, fill=col, width=2.5)
    elif name == "flatten":
        for y in (3, 9, 15):
            canvas.create_rectangle(2, y, s-2, y+4, fill=col, outline="")
    elif name == "clean":
        canvas.create_line(4, s-3, s-4, 4, fill=col, width=2)
        canvas.create_polygon(3, s-2, 8, s-5, 6, s-8, fill=col, outline="")
    elif name == "play":
        canvas.create_polygon(4, 2, 4, s-2, s-2, h, fill=col, outline="")
    elif name == "clear":
        canvas.create_line(3, 3, s-3, s-3, fill=col, width=2.5)
        canvas.create_line(s-3, 3, 3, s-3, fill=col, width=2.5)
    elif name == "info":
        canvas.create_oval(2, 2, s-2, s-2, outline=col, width=1.5)
        canvas.create_text(h, h+1, text="i", fill=col, font=("Georgia", 8, "bold"))
    elif name == "image":
        canvas.create_rectangle(2, 3, s-2, s-3, fill="", outline=col, width=1.5)
        canvas.create_oval(4, 5, 8, 9, fill=col, outline="")
        canvas.create_polygon(2, s-3, 7, s-9, 11, s-6,
                              s-4, s-11, s-2, s-3, fill=col, outline="")
    elif name == "gear":
        canvas.create_oval(h-3, h-3, h+3, h+3, outline=col, width=1.5)
        for deg in range(0, 360, 45):
            a = _math.radians(deg)
            canvas.create_line(h+4*_math.cos(a), h+4*_math.sin(a),
                               h+7*_math.cos(a), h+7*_math.sin(a), fill=col, width=2)
    elif name == "hex":
        pts = []
        for i in range(6):
            a = _math.radians(60*i - 30)
            pts += [h + (h-2)*_math.cos(a), h + (h-2)*_math.sin(a)]
        canvas.create_polygon(*pts, fill="", outline=col, width=1.8)
    elif name == "globe":
        canvas.create_oval(2, 2, s-2, s-2, outline=col, width=1.5)
        canvas.create_line(h, 2, h, s-2, fill=col, width=1)
        canvas.create_line(2, h, s-2, h, fill=col, width=1)
        canvas.create_oval(5, 6, s-5, s//2+2, fill="", outline=col, width=1)


def mkic(parent, name, size=16, color=None, bg=None):
    col  = color or C["muted"]
    bg_c = bg    or C["surface"]
    c = tk.Canvas(parent, width=size, height=size, bg=bg_c, highlightthickness=0)
    _draw(c, name, size, col)
    return c


# ══════════════════════════════════════════════════════════════════
#  APPLICATION
# ══════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._lang     = tk.StringVar(value="en")
        self._source   = tk.StringVar()
        self._target   = tk.StringVar()
        self._mode     = tk.StringVar(value="flatten")
        self._inc_img  = tk.BooleanVar(value=False)
        self._scan_res = None
        self._running  = False

        self.geometry("1060x790")
        self.minsize(920, 660)
        self.configure(bg=C["bg"])
        self._apply_icon()

        self._widgets:   dict = {}
        self._mode_rows: dict = {}
        self._mode_inds: dict = {}

        self._build()
        self._lang.trace_add("write", lambda *_: self._refresh_lang())
        self._mode.trace_add("write", lambda *_: self._highlight_mode())
        self._refresh_lang()

    def _apply_icon(self):
        try:
            icon_path = get_icon_path()
            if icon_path and os.path.exists(icon_path):
                self.iconbitmap(default=icon_path)
                if sys.platform == "win32":
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                        "lidprexlabs.repoprep.2.2")
        except Exception:
            pass

    def t(self, key: str) -> str:
        return LANGS.get(self._lang.get(), LANGS["en"]).get(key, key)

    # ══════════════════════════════════════════════════════════════
    #  LAYOUT
    # ══════════════════════════════════════════════════════════════
    def _build(self):
        self._build_titlebar()

        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=18, pady=(10, 0))

        left = tk.Frame(outer, bg=C["bg"])
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(outer, bg=C["bg"], width=420)
        right.pack(side="right", fill="both", expand=False, padx=(14, 0))
        right.pack_propagate(False)

        self._build_paths(left)
        self._build_modes(left)
        self._build_options(left)
        self._build_actions(left)
        self._build_log(right)

        self._build_footer()

    # ── Title bar ─────────────────────────────────────────────────
    def _build_titlebar(self):
        bar = tk.Frame(self, bg=C["title_bg"], height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # ── Left: logo + name + version
        left_g = tk.Frame(bar, bg=C["title_bg"])
        left_g.pack(side="left", padx=(16, 0))

        hc = tk.Canvas(left_g, width=34, height=34, bg=C["title_bg"], highlightthickness=0)
        hc.pack(side="left", padx=(0, 10), pady=11)
        _draw(hc, "hex", 34, C["accent"])

        tk.Label(left_g, text="RepoPrep Pro",
                 font=("Helvetica", 15, "bold"),
                 bg=C["title_bg"], fg=C["text"]).pack(side="left")
        tk.Label(left_g, text=" v2.2.0",
                 font=("Helvetica", 9), bg=C["title_bg"], fg=C["muted"]).pack(side="left", pady=18)

        # ── Right group
        right_g = tk.Frame(bar, bg=C["title_bg"])
        right_g.pack(side="right", padx=14)

        # Brand badge (clickable)
        badge = tk.Frame(right_g, bg="#110c2a", padx=12, pady=6)
        badge.pack(side="right", padx=(12, 0))
        self._widgets["built_by_lbl"] = tk.Label(
            badge, font=("Helvetica", 8), bg="#110c2a", fg=C["muted"])
        self._widgets["built_by_lbl"].pack(side="left")
        lx = tk.Label(badge, text=" Lidprex Labs",
                      font=("Helvetica", 8, "bold"), bg="#110c2a", fg=C["accent"],
                      cursor="hand2")
        lx.pack(side="left")
        lx.bind("<Button-1>", lambda e: webbrowser.open("https://lidprex-labs.onrender.com/"))
        lx.bind("<Enter>",    lambda e: lx.configure(fg=C["accent2"]))
        lx.bind("<Leave>",    lambda e: lx.configure(fg=C["accent"]))

        # Language selector — clean OptionMenu, not a row of buttons
        lang_g = tk.Frame(right_g, bg=C["title_bg"])
        lang_g.pack(side="right")

        mkic(lang_g, "globe", 15, C["muted"], C["title_bg"]).pack(side="left", padx=(0, 4))
        self._widgets["lang_label"] = tk.Label(
            lang_g, font=("Helvetica", 8), bg=C["title_bg"], fg=C["muted"])
        self._widgets["lang_label"].pack(side="left", padx=(0, 5))

        lang_codes = list(LANG_NAMES.keys())
        self._lang_display = tk.StringVar(value=LANG_NAMES["en"])

        om = tk.OptionMenu(lang_g, self._lang_display,
                           *[LANG_NAMES[c] for c in lang_codes])
        om.configure(
            font=("Helvetica", 9), bg=C["surface2"], fg=C["text"],
            activebackground=C["accent"], activeforeground="#fff",
            relief="flat", bd=0, highlightthickness=0,
            cursor="hand2", padx=10, pady=4,
        )
        om["menu"].configure(
            bg=C["surface2"], fg=C["text"],
            activebackground=C["accent"], activeforeground="#fff",
            relief="flat", bd=0, font=("Helvetica", 9),
        )
        om.pack(side="left")
        self._widgets["lang_om"] = om

        def _on_lang_select(*_):
            disp = self._lang_display.get()
            for code, name in LANG_NAMES.items():
                if name == disp:
                    self._lang.set(code)
                    break
        self._lang_display.trace_add("write", _on_lang_select)

    # ── Footer ────────────────────────────────────────────────────
    def _build_footer(self):
        foot = tk.Frame(self, bg=C["footer_bg"], height=36)
        foot.pack(fill="x", side="bottom")
        foot.pack_propagate(False)

        # Tagline left
        self._widgets["footer_tagline"] = tk.Label(
            foot, font=("Helvetica", 8, "italic"),
            bg=C["footer_bg"], fg=C["muted"])
        self._widgets["footer_tagline"].pack(side="left", padx=16, pady=10)

        # Links right
        links = tk.Frame(foot, bg=C["footer_bg"])
        links.pack(side="right", padx=16)

        tk.Label(links, text="© 2026", font=("Helvetica", 8),
                 bg=C["footer_bg"], fg=C["muted"]).pack(side="left", padx=(0, 8))

        def _link(parent, text, url):
            l = tk.Label(parent, text=text, font=("Helvetica", 8),
                         bg=C["footer_bg"], fg=C["accent"], cursor="hand2")
            l.pack(side="left", padx=(0, 10))
            l.bind("<Button-1>", lambda e: webbrowser.open(url))
            l.bind("<Enter>",    lambda e: l.configure(fg="#fff"))
            l.bind("<Leave>",    lambda e: l.configure(fg=C["accent"]))

        _link(links, "Lidprex Labs", "https://lidprex-labs.onrender.com/")
        tk.Label(links, text="·", bg=C["footer_bg"], fg=C["muted"],
                 font=("Helvetica", 8)).pack(side="left", padx=(0, 10))
        _link(links, "Lidprex", "https://lidprex.onrender.com/")

    # ── Card wrapper ─────────────────────────────────────────────
    def _card(self, parent, key, icon_name, icon_color=None):
        frame = tk.Frame(parent, bg=C["surface"],
                         highlightbackground=C["border"], highlightthickness=1)
        frame.pack(fill="x", pady=(0, 10))

        hdr = tk.Frame(frame, bg=C["surface2"], height=34)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        mkic(hdr, icon_name, 16, icon_color or C["accent"], C["surface2"]) \
            .pack(side="left", padx=(12, 6), pady=9)
        lbl = tk.Label(hdr, font=("Helvetica", 9, "bold"),
                       bg=C["surface2"], fg=C["text"])
        lbl.pack(side="left")
        self._widgets[key] = lbl

        body = tk.Frame(frame, bg=C["surface"], padx=14, pady=12)
        body.pack(fill="x")
        return body

    # ── Paths ─────────────────────────────────────────────────────
    def _build_paths(self, parent):
        c = self._card(parent, "paths_title", "folder")

        for lbl_key, browse_key, var, cmd_name in [
            ("source_label", "browse_src", self._source, "src"),
            ("target_label", "browse_tgt", self._target, "tgt"),
        ]:
            self._widgets[lbl_key] = tk.Label(
                c, font=("Helvetica", 8), bg=C["surface"], fg=C["muted"])
            self._widgets[lbl_key].pack(anchor="w")

            row = tk.Frame(c, bg=C["surface"])
            row.pack(fill="x", pady=(2, 10))

            ew = tk.Frame(row, bg=C["bg"],
                          highlightbackground=C["border"], highlightthickness=1)
            ew.pack(side="left", fill="x", expand=True)
            tk.Entry(ew, textvariable=var, bg=C["bg"], fg=C["text"],
                     relief="flat", insertbackground=C["accent"],
                     font=("Courier", 9), bd=0) \
                .pack(fill="x", ipady=8, ipadx=8)

            cmd = self._pick_source if cmd_name == "src" else self._pick_target
            self._widgets[browse_key] = tk.Button(
                row, font=("Helvetica", 9), bg=C["surface2"], fg=C["text"],
                relief="flat", cursor="hand2", padx=14, pady=5,
                activebackground=C["accent"], activeforeground="#fff",
                command=cmd)
            self._widgets[browse_key].pack(side="right", padx=(8, 0))

    # ── Modes ─────────────────────────────────────────────────────
    def _build_modes(self, parent):
        c = self._card(parent, "modes_title", "gear")

        defs = [
            ("flatten", "flatten", C["accent"],  "mode_flatten", "mode_flatten_d"),
            ("clean",   "clean",   C["accent2"], "mode_clean",   "mode_clean_d"),
            ("scan",    "scan",    C["accent3"], "mode_scan",    "mode_scan_d"),
        ]

        for val, ic_name, ic_col, lbl_key, desc_key in defs:
            row = tk.Frame(c, bg=C["surface2"],
                           highlightbackground=C["border"], highlightthickness=1,
                           padx=12, pady=10, cursor="hand2")
            row.pack(fill="x", pady=4)
            self._mode_rows[val] = row

            def _click(e, v=val): self._mode.set(v)
            row.bind("<Button-1>", _click)

            ic_c = mkic(row, ic_name, 18, ic_col, C["surface2"])
            ic_c.pack(side="left", anchor="n", pady=2, padx=(0, 10))
            ic_c.bind("<Button-1>", _click)

            inner = tk.Frame(row, bg=C["surface2"])
            inner.pack(side="left", fill="x", expand=True)
            inner.bind("<Button-1>", _click)

            top = tk.Frame(inner, bg=C["surface2"])
            top.pack(fill="x")
            top.bind("<Button-1>", _click)

            ind = tk.Label(top, text="○", font=("Helvetica", 12),
                           bg=C["surface2"], fg=C["muted"], cursor="hand2")
            ind.pack(side="left", padx=(0, 6))
            ind.bind("<Button-1>", _click)
            self._mode_inds[val] = ind

            title_lbl = tk.Label(top, font=("Helvetica", 10, "bold"),
                                 bg=C["surface2"], fg=C["text"],
                                 cursor="hand2", anchor="w")
            title_lbl.pack(side="left", fill="x")
            title_lbl.bind("<Button-1>", _click)
            self._widgets[lbl_key] = title_lbl

            desc_lbl = tk.Label(inner, font=("Helvetica", 8),
                                bg=C["surface2"], fg=C["muted"],
                                justify="left", wraplength=460, anchor="w")
            desc_lbl.pack(anchor="w", pady=(3, 0))
            desc_lbl.bind("<Button-1>", _click)
            self._widgets[desc_key] = desc_lbl

    def _highlight_mode(self):
        cur = self._mode.get()
        ic_colors = {"flatten": C["accent"], "clean": C["accent2"], "scan": C["accent3"]}

        for val, row in self._mode_rows.items():
            sel = (val == cur)
            bg  = C["sel_bg"]  if sel else C["surface2"]
            brd = C["sel_brd"] if sel else C["border"]
            row.configure(bg=bg, highlightbackground=brd)

            def _repaint(w, b):
                try:    w.configure(bg=b)
                except: pass
                for ch in w.winfo_children():
                    _repaint(ch, b)

            for ch in row.winfo_children():
                _repaint(ch, bg)

            ind = self._mode_inds.get(val)
            if ind:
                ind.configure(
                    text="●" if sel else "○",
                    fg=ic_colors[val] if sel else C["muted"], bg=bg)

    # ── Options ───────────────────────────────────────────────────
    def _build_options(self, parent):
        c = self._card(parent, "options_title", "image", C["warning"])

        row = tk.Frame(c, bg=C["surface"])
        row.pack(fill="x")
        mkic(row, "image", 16, C["warning"], C["surface"]).pack(side="left", padx=(0, 8))
        self._widgets["opt_images_cb"] = tk.Checkbutton(
            row, variable=self._inc_img, font=("Helvetica", 9),
            bg=C["surface"], fg=C["text"], activebackground=C["surface"],
            selectcolor=C["surface3"], cursor="hand2")
        self._widgets["opt_images_cb"].pack(side="left")

        self._widgets["opt_images_hint"] = tk.Label(
            c, font=("Helvetica", 8), bg=C["surface"], fg=C["muted"],
            justify="left", wraplength=500)
        self._widgets["opt_images_hint"].pack(anchor="w", pady=(5, 0))

    # ── Actions ───────────────────────────────────────────────────
    def _build_actions(self, parent):
        c = self._card(parent, "actions_title", "play", C["success"])

        btn_row = tk.Frame(c, bg=C["surface"])
        btn_row.pack(fill="x")

        self._widgets["btn_run"] = tk.Button(
            btn_row, font=("Helvetica", 11, "bold"),
            bg=C["accent"], fg="#fff", relief="flat", cursor="hand2",
            activebackground="#9a8cff", activeforeground="#fff",
            command=self._on_run)
        self._widgets["btn_run"].pack(
            side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

        self._widgets["btn_scan"] = tk.Button(
            btn_row, font=("Helvetica", 10, "bold"),
            bg=C["surface2"], fg=C["text"], relief="flat", cursor="hand2",
            activebackground=C["accent"], activeforeground="#fff",
            command=self._on_scan)
        self._widgets["btn_scan"].pack(
            side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

        self._widgets["btn_clear"] = tk.Button(
            btn_row, font=("Helvetica", 9),
            bg=C["surface2"], fg=C["muted"], relief="flat", cursor="hand2",
            activebackground=C["surface3"], activeforeground=C["text"],
            command=self._clear_log, padx=16)
        self._widgets["btn_clear"].pack(side="left", ipady=9)

        self._stats_var = tk.StringVar()
        self._widgets["stats_lbl"] = tk.Label(
            c, textvariable=self._stats_var,
            font=("Helvetica", 8), bg=C["surface"], fg=C["muted"],
            anchor="w", wraplength=580, justify="left")
        self._widgets["stats_lbl"].pack(anchor="w", pady=(10, 0))

        sty = ttk.Style()
        sty.theme_use("default")
        sty.configure("LP.Horizontal.TProgressbar",
                      troughcolor=C["surface2"], background=C["accent"], thickness=5)
        self._progress = ttk.Progressbar(
            c, style="LP.Horizontal.TProgressbar",
            mode="determinate", maximum=100)
        self._progress.pack(fill="x", pady=(8, 0))

    # ── Log ───────────────────────────────────────────────────────
    def _build_log(self, parent):
        hdr = tk.Frame(parent, bg=C["surface2"],
                       highlightbackground=C["border"], highlightthickness=1, height=36)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        mkic(hdr, "info", 16, C["accent2"], C["surface2"]).pack(side="left", padx=(12, 6), pady=10)
        self._widgets["log_title"] = tk.Label(
            hdr, font=("Helvetica", 9, "bold"), bg=C["surface2"], fg=C["text"])
        self._widgets["log_title"].pack(side="left")

        self._widgets["btn_open"] = tk.Button(
            hdr, font=("Helvetica", 8), bg=C["surface2"], fg=C["muted"],
            relief="flat", cursor="hand2",
            activebackground=C["surface3"], activeforeground=C["accent"],
            command=self._open_output)
        self._widgets["btn_open"].pack(side="right", padx=10)

        wrap = tk.Frame(parent, bg=C["surface"],
                        highlightbackground=C["border"], highlightthickness=1)
        wrap.pack(fill="both", expand=True)

        self._log_txt = tk.Text(
            wrap, bg="#040410", fg="#a0a0c8",
            font=("Courier", 8), relief="flat", state="disabled",
            wrap="word", insertbackground=C["accent"],
            selectbackground=C["accent"], padx=10, pady=8)
        self._log_txt.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(wrap, command=self._log_txt.yview,
                          bg=C["surface"], troughcolor=C["bg"],
                          activebackground=C["accent"], relief="flat")
        sb.pack(side="right", fill="y")
        self._log_txt.configure(yscrollcommand=sb.set)

        for tag, col in [
            ("INFO",  C["info_fg"]), ("COPY",  C["copy_fg"]),
            ("SKIP",  C["skip_fg"]), ("WARN",  C["warn_fg"]),
            ("ERROR", C["error"]),   ("DONE",  C["done_fg"]),
            ("SCAN",  C["scan_fg"]),
        ]:
            self._log_txt.tag_config(tag, foreground=col)

    # ══════════════════════════════════════════════════════════════
    #  LANGUAGE REFRESH
    # ══════════════════════════════════════════════════════════════
    def _refresh_lang(self):
        self.title(self.t("app_title"))

        map_ = {
            "lang_label":      "lang_label",
            "built_by_lbl":    "built_by",
            "paths_title":     "paths_title",
            "source_label":    "source_label",
            "target_label":    "target_label",
            "browse_src":      "browse",
            "browse_tgt":      "browse",
            "modes_title":     "modes_title",
            "mode_flatten":    "mode_flatten",
            "mode_flatten_d":  "mode_flatten_d",
            "mode_clean":      "mode_clean",
            "mode_clean_d":    "mode_clean_d",
            "mode_scan":       "mode_scan",
            "mode_scan_d":     "mode_scan_d",
            "options_title":   "options_title",
            "opt_images_cb":   "opt_images",
            "opt_images_hint": "opt_images_hint",
            "actions_title":   "actions_title",
            "btn_run":         "btn_run",
            "btn_scan":        "btn_scan",
            "btn_clear":       "btn_clear",
            "btn_open":        "btn_open",
            "log_title":       "log_title",
            "footer_tagline":  "footer_tagline",
        }
        for wkey, tkey in map_.items():
            w = self._widgets.get(wkey)
            if w:
                try:    w.configure(text=self.t(tkey))
                except: pass

        if not self._scan_res:
            self._stats_var.set(self.t("stats_default"))

        self._highlight_mode()

    # ══════════════════════════════════════════════════════════════
    #  PICKING
    # ══════════════════════════════════════════════════════════════
    def _pick_source(self):
        p = filedialog.askdirectory(title=self.t("source_label"))
        if not p: return
        self._source.set(p)
        if not self._target.get():
            self._target.set(
                os.path.join(str(Path(p).parent), f"{Path(p).name}_prepared"))
        self._do_scan_async(p)

    def _pick_target(self):
        p = filedialog.askdirectory(title=self.t("target_label"))
        if p: self._target.set(p)

    # ══════════════════════════════════════════════════════════════
    #  SCAN
    # ══════════════════════════════════════════════════════════════
    def _on_scan(self):
        src = self._source.get()
        if not src:
            messagebox.showwarning("", self.t("warn_no_src")); return
        self._do_scan_async(src)

    def _do_scan_async(self, path):
        def worker():
            res = scan_project(path, self._inc_img.get())
            self.after(0, lambda: self._show_scan(res))
        threading.Thread(target=worker, daemon=True).start()

    def _show_scan(self, s):
        self._scan_res = s
        tm = round(s["total_size"]  / 1048576, 1)
        cm = round(s["clean_size"]  / 1048576, 1)
        sv = round(sum(s["skippable"].values()) / 1048576, 1)

        self._stats_var.set(self.t("stats_fmt").format(
            type=s["project_type"],
            tf=s["total_files"], tm=tm,
            cf=s["clean_files"], cm=cm,
            sd=s["skipped_dirs"], sf=s["skipped_files"], sv=sv))
        self._widgets["stats_lbl"].configure(fg=C["success"])

        self._log("─" * 52, "INFO")
        self._log(f"{self.t('scan_type')} : {s['project_type']}", "SCAN")
        self._log(f"{self.t('scan_total')} : {s['total_files']} files  ({tm} MB)", "SCAN")
        self._log(f"{self.t('scan_after')} : {s['clean_files']} files  ({cm} MB)", "SCAN")
        self._log(f"{self.t('scan_dirs')} : {s['skipped_dirs']}   "
                  f"{self.t('scan_files_s')}: {s['skipped_files']}", "SCAN")
        for d, sz in sorted(s["skippable"].items(), key=lambda x: -x[1])[:6]:
            self._log(f"  skip  {d}/  ({round(sz/1048576,1)} MB)", "SKIP")

    # ══════════════════════════════════════════════════════════════
    #  RUN
    # ══════════════════════════════════════════════════════════════
    def _on_run(self):
        mode = self._mode.get()
        if mode == "scan":
            self._on_scan(); return

        src = self._source.get()
        tgt = self._target.get()

        if not src:
            messagebox.showwarning("", self.t("warn_no_src")); return
        if not Path(src).exists():
            messagebox.showerror("", self.t("err_no_src").format(src)); return
        if not tgt:
            messagebox.showwarning("", self.t("warn_no_tgt")); return

        t = Path(tgt)
        if t.exists() and t != Path(src):
            try:
                if any(t.iterdir()):
                    if not messagebox.askyesno("", self.t("confirm_overwrite").format(tgt)):
                        return
            except Exception:
                pass

        self._running = True
        self._widgets["btn_run"].configure(state="disabled", text=self.t("running"))
        self._progress["value"] = 0
        self._log("─" * 52, "INFO")
        self._log(f"Mode   : {mode.upper()}", "INFO")
        self._log(f"Source : {src}",          "INFO")
        self._log(f"Output : {tgt}",          "INFO")

        def worker():
            result = run_operation(
                src, tgt, mode=mode,
                include_images=self._inc_img.get(),
                log_cb=lambda msg, lv="INFO":
                    self.after(0, lambda m=msg, l=lv: self._log(m, l)),
                progress_cb=lambda pct:
                    self.after(0, lambda p=pct: self._set_progress(p)),
            )
            self.after(0, lambda: self._on_done(result, tgt))

        threading.Thread(target=worker, daemon=True).start()

    def _set_progress(self, pct):
        self._progress["value"] = pct

    def _on_done(self, result, tgt):
        self._running = False
        self._widgets["btn_run"].configure(state="normal", text=self.t("btn_run"))
        self._progress["value"] = 100 if result else 0
        if result and isinstance(result, dict):
            if messagebox.askyesno(
                    self.t("done_title"),
                    self.t("done_msg").format(result["copied"], result["skipped"])):
                self._open_folder(tgt)
        else:
            messagebox.showerror(self.t("fail_title"), self.t("fail_msg"))

    # ══════════════════════════════════════════════════════════════
    #  LOG HELPERS
    # ══════════════════════════════════════════════════════════════
    def _log(self, msg, level="INFO"):
        self._log_txt.configure(state="normal")
        self._log_txt.insert("end", msg + "\n", level)
        self._log_txt.see("end")
        self._log_txt.configure(state="disabled")

    def _clear_log(self):
        self._log_txt.configure(state="normal")
        self._log_txt.delete("1.0", "end")
        self._log_txt.configure(state="disabled")
        self._progress["value"] = 0

    def _open_output(self):
        tgt = self._target.get()
        if tgt and Path(tgt).exists():
            self._open_folder(tgt)
        else:
            messagebox.showinfo("", self.t("no_output"))

    @staticmethod
    def _open_folder(path):
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.update_idletasks()
    w, h = 1060, 790
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    app.mainloop()
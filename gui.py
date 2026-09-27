"""Desktop GUI for Prompt IR; uses only the Python standard library."""

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from compilers import compile_negative, compile_prompt


ROOT = Path(__file__).resolve().parent
VERSION = (ROOT / "GUI_VERSION").read_text(encoding="utf-8").strip()
EXAMPLE = ROOT / "prompts" / "dunhuang_single.json"

COLORS = {
    "background": "#F0FDFA", "surface": "#FFFFFF", "text": "#134E4A",
    "muted": "#475569", "border": "#A9D9D4", "primary": "#0D9488",
    "action": "#C2410C", "action_text": "#FFFFFF", "error": "#B91C1C",
}
FONT = "Segoe UI"


def compile_text(source, target):
    """Parse editor text and return positive and negative prompt strings."""
    ir = json.loads(source)
    return compile_prompt(ir, target), compile_negative(ir, target)


class PromptIRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Prompt IR · v{VERSION} GUI")
        self.geometry("1160x740")
        self.minsize(850, 550)
        self.configure(bg=COLORS["background"])
        self.current_file = None
        self.dirty = False
        self.target = tk.StringVar(value="sdxl")
        self.file_label = tk.StringVar(value="未打开文件")
        self.status = tk.StringVar(value="打开 JSON 文件，或载入敦煌示例开始。")
        self._setup_style()
        self._build_ui()
        self._bind_shortcuts()
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._load(EXAMPLE, ask=False, template=True)
        self._compile()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background=COLORS["background"])
        style.configure("Card.TFrame", background=COLORS["surface"])
        style.configure("Title.TLabel", background=COLORS["background"],
                        foreground=COLORS["text"], font=(FONT, 20, "bold"))
        style.configure("Subtitle.TLabel", background=COLORS["background"],
                        foreground=COLORS["muted"], font=(FONT, 10))
        style.configure("CardTitle.TLabel", background=COLORS["surface"],
                        foreground=COLORS["text"], font=(FONT, 11, "bold"))
        style.configure("Info.TLabel", background=COLORS["surface"],
                        foreground=COLORS["muted"], font=(FONT, 9))
        style.configure("Status.TLabel", background=COLORS["background"],
                        foreground=COLORS["muted"], font=(FONT, 9))
        style.configure("Action.TButton", font=(FONT, 10, "bold"), padding=(16, 10),
                        background=COLORS["action"], foreground=COLORS["action_text"])
        style.map("Action.TButton", background=[("active", "#9A3412")],
                  foreground=[("active", COLORS["action_text"])])
        style.configure("Tool.TButton", font=(FONT, 9), padding=(10, 8),
                        background=COLORS["surface"], foreground=COLORS["text"])
        style.map("Tool.TButton", background=[("active", "#DDF6F1")])
        style.configure("Target.TCombobox", font=(FONT, 10), padding=6)

    def _build_ui(self):
        shell = ttk.Frame(self, style="App.TFrame", padding=20)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(2, weight=1)

        header = ttk.Frame(shell, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ttk.Label(header, text="Prompt IR", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="JSON → SDXL / FLUX 提示词", style="Subtitle.TLabel").pack(anchor="w")

        toolbar = ttk.Frame(shell, style="App.TFrame")
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        for label, command in (("打开 JSON", self._open), ("载入示例", self._example),
                               ("保存 JSON", self._save)):
            ttk.Button(toolbar, text=label, command=command, style="Tool.TButton").pack(
                side="left", padx=(0, 8))
        ttk.Label(toolbar, text="目标模型", style="Subtitle.TLabel").pack(side="left", padx=(18, 8))
        target = ttk.Combobox(toolbar, textvariable=self.target, values=("sdxl", "flux"),
                              state="readonly", width=8, style="Target.TCombobox")
        target.pack(side="left")
        target.bind("<<ComboboxSelected>>", self._target_changed)
        ttk.Button(toolbar, text="生成 Prompt", command=self._compile,
                   style="Action.TButton").pack(side="right")

        split = ttk.Panedwindow(shell, orient="horizontal")
        split.grid(row=2, column=0, sticky="nsew")
        editor_card = ttk.Frame(split, style="Card.TFrame", padding=16)
        result_card = ttk.Frame(split, style="Card.TFrame", padding=16)
        split.add(editor_card, weight=1)
        split.add(result_card, weight=1)
        self._build_editor(editor_card)
        self._build_results(result_card)

        status = ttk.Label(shell, textvariable=self.status, style="Status.TLabel", anchor="w")
        status.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self.status_label = status

    def _build_editor(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        ttk.Label(parent, text="Prompt IR · JSON", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w")
        ttk.Label(parent, textvariable=self.file_label, style="Info.TLabel").grid(
            row=1, column=0, sticky="w", pady=(3, 12))
        area = ttk.Frame(parent, style="Card.TFrame")
        area.grid(row=2, column=0, sticky="nsew")
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)
        self.editor = tk.Text(area, wrap="none", undo=True, font=("Consolas", 10),
                              background=COLORS["surface"], foreground=COLORS["text"],
                              insertbackground=COLORS["text"], selectbackground="#B4E7DF",
                              relief="solid", borderwidth=1, highlightthickness=1,
                              highlightcolor=COLORS["primary"], padx=12, pady=12)
        self.editor.grid(row=0, column=0, sticky="nsew")
        yscroll = ttk.Scrollbar(area, orient="vertical", command=self.editor.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll = ttk.Scrollbar(area, orient="horizontal", command=self.editor.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.editor.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.editor.bind("<<Modified>>", self._mark_dirty)

    def _build_results(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=3, minsize=140)
        parent.rowconfigure(3, weight=1, minsize=100)
        top = ttk.Frame(parent, style="Card.TFrame")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(top, text="正向 Prompt", style="CardTitle.TLabel").pack(side="left")
        ttk.Button(top, text="复制", command=lambda: self._copy(self.positive),
                   style="Tool.TButton").pack(side="right")
        self.positive = self._result_text(parent, 1)
        bottom = ttk.Frame(parent, style="Card.TFrame")
        bottom.grid(row=2, column=0, sticky="ew", pady=(16, 8))
        ttk.Label(bottom, text="负向 Prompt", style="CardTitle.TLabel").pack(side="left")
        ttk.Button(bottom, text="复制", command=lambda: self._copy(self.negative),
                   style="Tool.TButton").pack(side="right")
        self.negative = self._result_text(parent, 3)
        ttk.Button(parent, text="导出结果为 TXT", command=self._export,
                   style="Tool.TButton").grid(row=4, column=0, sticky="e", pady=(14, 0))

    def _result_text(self, parent, row):
        area = ttk.Frame(parent, style="Card.TFrame")
        area.grid(row=row, column=0, sticky="nsew")
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)
        widget = tk.Text(area, wrap="word", height=1, state="disabled", font=(FONT, 11),
                         background="#F8FCFB", foreground=COLORS["text"],
                         relief="solid", borderwidth=1, highlightthickness=1,
                         highlightcolor=COLORS["primary"], padx=12, pady=12)
        widget.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(area, orient="vertical", command=widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        widget.configure(yscrollcommand=scrollbar.set)
        return widget

    def _bind_shortcuts(self):
        self.bind_all("<Control-o>", lambda _event: self._open())
        self.bind_all("<Control-s>", lambda _event: self._save())
        self.bind_all("<Control-Return>", lambda _event: self._compile())

    def _set_status(self, message, error=False):
        self.status.set(message)
        self.status_label.configure(foreground=COLORS["error"] if error else COLORS["muted"])

    def _mark_dirty(self, _event):
        if self.editor.edit_modified():
            self.dirty = True
            self.editor.edit_modified(False)
            self._clear_results()
            self._set_status("JSON 已修改。请重新生成 Prompt。")

    def _clear_results(self):
        self._put_result(self.positive, "")
        self._put_result(self.negative, "")

    def _target_changed(self, _event):
        self._clear_results()
        self._set_status("目标模型已切换。请重新生成 Prompt。")

    def _confirm_replace(self):
        if not self.dirty:
            return True
        answer = messagebox.askyesnocancel("未保存的修改", "当前 JSON 已修改。要先保存吗？", parent=self)
        if answer is None:
            return False
        return not answer or self._save()

    def _load(self, path, ask=True, template=False):
        if ask and not self._confirm_replace():
            return
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self._set_status(f"无法打开文件：{exc}", error=True)
            messagebox.showerror("打开失败", str(exc), parent=self)
            return
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
        self.editor.edit_modified(False)
        self.dirty = False
        self._clear_results()
        self.current_file = None if template else path
        self.file_label.set("敦煌示例 · 保存时将创建新文件" if template else path.name)
        self._set_status("JSON 已载入。选择目标模型后生成 Prompt。")
        self.editor.focus_set()

    def _open(self):
        name = filedialog.askopenfilename(parent=self, title="打开 Prompt IR JSON",
                                          filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")])
        if name:
            self._load(Path(name))

    def _example(self):
        self._load(EXAMPLE, template=True)

    def _save(self):
        path = self.current_file
        if path is None:
            name = filedialog.asksaveasfilename(parent=self, title="保存 Prompt IR JSON",
                                                defaultextension=".json",
                                                filetypes=[("JSON 文件", "*.json")])
            if not name:
                return False
            path = Path(name)
        content = self.editor.get("1.0", "end-1c")
        try:
            json.loads(content)
            path.write_text(content, encoding="utf-8")
        except (json.JSONDecodeError, OSError, UnicodeError) as exc:
            self._set_status(f"保存失败：{exc}", error=True)
            messagebox.showerror("保存失败", str(exc), parent=self)
            return False
        self.current_file = path
        self.file_label.set(str(path))
        self.dirty = False
        self._set_status("JSON 已保存。")
        return True

    def _put_result(self, widget, value):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def _compile(self):
        try:
            positive, negative = compile_text(self.editor.get("1.0", "end-1c"), self.target.get())
        except json.JSONDecodeError as exc:
            self._clear_results()
            self._set_status(f"JSON 语法错误：第 {exc.lineno} 行，第 {exc.colno} 列。{exc.msg}", error=True)
            self.editor.mark_set("insert", f"{exc.lineno}.{max(exc.colno - 1, 0)}")
            self.editor.see("insert")
            self.editor.focus_set()
            return
        except ValueError as exc:
            self._clear_results()
            self._set_status(f"字段校验失败：{exc}", error=True)
            self.editor.focus_set()
            return
        self._put_result(self.positive, positive)
        self._put_result(self.negative, negative)
        self._set_status(f"已生成 {self.target.get().upper()} Prompt。可复制或导出结果。")

    def _copy(self, widget):
        value = widget.get("1.0", "end-1c")
        if not value:
            self._set_status("请先生成 Prompt。", error=True)
            return
        self.clipboard_clear()
        self.clipboard_append(value)
        self._set_status("已复制到剪贴板。")

    def _export(self):
        positive = self.positive.get("1.0", "end-1c")
        if not positive:
            self._set_status("请先生成 Prompt，再导出结果。", error=True)
            return
        name = filedialog.asksaveasfilename(parent=self, title="导出 Prompt",
                                            defaultextension=".txt",
                                            filetypes=[("文本文件", "*.txt")])
        if not name:
            return
        negative = self.negative.get("1.0", "end-1c")
        content = f"Target: {self.target.get()}\n\nPositive prompt:\n{positive}\n\nNegative prompt:\n{negative}\n"
        try:
            Path(name).write_text(content, encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self._set_status(f"导出失败：{exc}", error=True)
            messagebox.showerror("导出失败", str(exc), parent=self)
            return
        self._set_status("结果已导出为 TXT。")

    def _close(self):
        if self._confirm_replace():
            self.destroy()


def main():
    PromptIRApp().mainloop()


if __name__ == "__main__":
    main()

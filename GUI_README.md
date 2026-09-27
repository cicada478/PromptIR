# Prompt IR v0.1.1 · GUI 版

此版本以 v0.1.0 命令行版为基础，增加 Windows 桌面图形界面。

## 启动

**直接双击：**从 GitHub 版本发布下载 `PromptIR-v0.1.1.exe` 并运行。EXE 已包含 Python 运行环境和敦煌示例，无需另装 Python。首次启动可能稍慢，因为单文件程序需要先解包。启动后会自动生成敦煌示例的正向和负向 Prompt。

**从源码运行：**解压 `prompt-ir-v0.1.1-gui.zip`，进入 `prompt_ir` 目录：

```powershell
python gui.py
```

源码运行需要 Python 3.9 或更新版本，也可使用 `pythonw gui.py` 隐藏控制台窗口。压缩包仍包含 `main.py`，原命令行用法保持可用。

## 操作

1. 启动时显示敦煌示例。也可点击“打开 JSON”读取自己的文件，或直接在左侧编辑。
2. 选择 SDXL 或 FLUX，点击“生成 Prompt”。右侧分别显示正向和负向结果。
3. 点击各结果旁的“复制”，或点击“导出结果为 TXT”。
4. 点击“保存 JSON”保存左侧内容。示例作为模板打开，保存时会要求选择新文件路径。

快捷键：`Ctrl+O` 打开、`Ctrl+S` 保存、`Ctrl+Enter` 生成。JSON 语法错误会在底部显示行列号并定位编辑光标；字段错误会显示具体字段。切换文件或关闭窗口时会提示保存未保存的修改。

GUI 和 CLI 使用同一组 `compilers/`、`utils/` 与 `schema/`。未来的 ComfyUI 节点也可以直接调用 `compile_prompt(ir, target)` 和 `compile_negative(ir, target)`。

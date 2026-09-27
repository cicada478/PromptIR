# 更新记录

## v0.1.1 · GUI 版

- 修复正向 Prompt 文本区被布局挤压到不可见的问题。
- 启动时自动生成敦煌示例的正向和负向 Prompt。

## v0.1.0 · GUI 版

- 在命令行版基础上增加 Tkinter 桌面界面，支持 JSON 编辑、文件打开与保存、目标切换、结果复制与 TXT 导出。
- 增加字段错误和 JSON 语法错误提示、未保存内容提醒、键盘快捷键。
- 保留独立 CLI ZIP，并可单独构建 GUI ZIP。
- 提供可双击的 Windows 单文件 EXE，运行时无需另装 Python。

## v0.1.0 · 命令行版

- 从本地 UTF-8 JSON 文件读取 Prompt IR。
- 支持 SDXL 短语式提示词和 FLUX 自然语言提示词。
- 提供 `compile_prompt(ir, target)` 和独立的负向提示词接口。
- 包含基础字段校验、性别别名规范化、敦煌风示例及 JSON Schema 参考定义。
- 提供 `python main.py ... --target ...` 命令行入口。

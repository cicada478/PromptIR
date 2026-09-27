# Prompt IR

Prompt IR 把描述画面的 JSON 转成适合 SDXL 或 FLUX 的文本提示词。项目包含命令行程序和 Windows 桌面界面；当前为实验版。JSON 是编辑格式，输出的纯文本可复制到 ComfyUI 的文本编码节点。

## 从源码开始

需要 Python 3.9 或更新版本。项目运行时只使用 Python 标准库；图形界面需要可用的 Tkinter。以下命令在仓库根目录运行。

```powershell
python main.py prompts/dunhuang_single.json --target sdxl
python main.py prompts/dunhuang_single.json --target flux
python gui.py
```

命令行会分别打印正向和负向提示词。SDXL 正向输出是逗号分隔的短语；FLUX 正向输出是自然语言句子。GUI 启动时自动载入并编译敦煌示例；操作和快捷键见 [GUI 使用说明](GUI_README.md)。也可将第一个命令中的示例路径换成自己的 UTF-8 JSON 文件。

### 命令行接口

```text
python main.py INPUT.json --target {sdxl,flux}
python main.py --version
```

`subject` 是唯一必填区块。JSON 语法、字段类型、未知字段或文件读取出错时，命令行向标准错误输出信息并以退出码 2 结束。`negative` 单独输出；是否将它连接到负向编码节点，由具体模型和 ComfyUI 工作流决定。

### Python 接口

```python
import json
from compilers import compile_negative, compile_prompt

with open("prompts/dunhuang_single.json", encoding="utf-8") as stream:
    ir = json.load(stream)

positive = compile_prompt(ir, "sdxl")
negative = compile_negative(ir, "sdxl")
```

IR 支持 `subject`、`appearance`、`wardrobe`、`composition`、`environment`、`lighting`、`camera`、`aesthetic`、`negative`。字段定义见 [JSON Schema](schema/prompt.schema.json)。运行时校验器只实现本项目使用的 Schema 子集，并非通用 JSON Schema 引擎。简单规范化会把部分性别别名转为统一值，不修改传入的原对象。

## Portable 版本与本地构建

Windows 可双击的 portable EXE 随 GitHub 版本发布提供，用户无需另装 Python。源码仓库不跟踪 `dist/` 中的生成文件。在仓库根目录可自行构建源码 ZIP：

```powershell
python build_release.py
python build_release.py --edition gui
```

前者生成命令行源码 ZIP，后者生成 GUI 源码 ZIP。要在 Windows 构建 EXE，先在自己的构建环境安装 PyInstaller，再运行 `python build_windows_exe.py`。构建脚本不会安装依赖。当前命令行版本为 `0.1.0`，GUI 版本为 `0.1.1`，变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 结构与后续节点封装

- `prompts/`：示例 IR；`schema/`：字段参考定义。
- `utils/`：基础校验、规范化和短语组合。
- `compilers/`：统一接口及 SDXL、FLUX 编译器。
- `main.py` 与 `gui.py`：分别提供命令行和桌面入口。

未来的 ComfyUI 自定义节点可解析 JSON，然后调用 `compile_prompt(ir, target)` 与 `compile_negative(ir, target)`，将两个字符串接到相应文本编码节点。目前尚未注册 ComfyUI 节点，也没有图像生成或采样器逻辑。

## 状态、反馈与许可

该项目目前仅在 Windows 11、Python 3.14.7 上做过本地运行验证；未声明其他平台的 GUI 或 EXE 兼容性。问题可通过此仓库的 Issues 功能反馈（如果已启用）。开发过程使用 GPT6-sol 作为辅助上下文；程序运行时不调用模型 API。

项目目前未附开源许可证。仓库可见不代表授予复制、修改或再分发的许可；权利人尚未作出许可选择。

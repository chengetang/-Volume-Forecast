# Volume-Forecast

一个用于发布预测货量的 Python 工具。

---

## 📁 项目结构

src/
├── launcher.py        # 启动器脚本
├── app.py             # 主程序入口
├── config_data.py     # 配置管理
tests/                 # 测试脚本
archive/               # 历史版本代码

---

## 🚀 功能介绍

### `launcher.py`
负责下载和执行主程序文件和配置文件。

### `app.py`
负责调用预测逻辑，可执行整体业务流程。

### `config_data.py`
管理项目配置，API配置，站点列表等。

### `tests/`
包含针对主要模块的测试脚本，未来可扩展为 pytest 自动化测试。

### `archive/`
包含历史版本代码。

---

## 🛠 使用方法

### 运行启动器文件

```bash
python src/launcher.py

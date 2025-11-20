# Volume-Forecast（货量预测工具）

一个用于预测货量变化的轻量级 Python 工具。项目采用清晰的 `src/` + `tests/` 项目结构，并提供基础的配置管理与预测逻辑，是一个可扩展的预测分析项目模板。

---

## 📁 项目结构
Volume-Forecast/
│
├── archive/ # 旧版本代码归档
│ └── v1.0.0/
│ ├── app.py
│ └── config_data.py
│
├── src/ # 主程序（生产环境代码）
│ ├── app.py
│ └── config_data.py
│
└── tests/ # 测试脚本
├── app_test.py
└── config_data_test.py

---

## 🚀 功能介绍

### `app.py`
负责调用预测逻辑，可执行整体业务流程。

### `config_data.py`
管理项目配置，例如输入数据、参数设置等。

### `tests/`
包含针对主要模块的测试脚本，未来可扩展为 pytest 自动化测试。

---

## 🛠 使用方法

### 运行主程序

```bash
python src/app.py

# IM Kernel Python SDK

IM Kernel Python SDK 是一个强大的工具包，用于构建和操作基于工业模型（Industry Model）的应用。它基于工业语言和三维四层统一模型理论，为开发者提供了一套全面的
API 来创建、管理和优化复杂的工业系统模型。

## 安装

### 基础库安装

使用 pip 安装 IM Kernel Python SDK：

```bash
pip install imkernel
```

### 扩展库安装

#### 三维展示采用pyvista+jupyter，故需要安装如下包：

```bash
pip install jupyterlab vtk trame ipywidgets 'pyvista[all,trame]' trame_jupyter_extension
```

安装jupyterhub中文包

```
pip install jupyterlab-language-pack-zh-CN
```

安装pyocc

```
conda install conda-forge::pythonocc-core
```

#### 同时也对matplotlib进行一些封装，故需要安装如下包：

```bash
pip install matplotlib
```

## 文档

完整的 API 文档和更多示例可以在我们的[官方文档网站](https://docs.imkernel.com)上找到。

## 贡献

我们欢迎社区贡献！如果您发现了 bug 或有改进建议，请在我们的 GitHub 仓库提出 issue 或提交 pull request。

## 许可证

IM Kernel Python SDK 采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。


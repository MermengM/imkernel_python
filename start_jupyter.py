import subprocess


def start_jupyter_notebook():
    # 指定 Jupyter Notebook 服务器的 IP 地址和端口
    ip = '0.0.0.0'
    port = 8888

    # 启动 Jupyter Notebook 服务器
    command = f'jupyter notebook --ip {ip} --port {port} --NotebookApp.token='''
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    start_jupyter_notebook()

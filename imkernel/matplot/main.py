
import pandas as pd
import matplotlib.pyplot as plt
def showScatter_plot(file_path):
    df = pd.read_csv(file_path,index_col=0)
    # 获取最后两列的数据
    mrr = df.iloc[:, -2]  
    failure_rate = df.iloc[:, -1]
    failure_mrr = df.iloc[:, -2:]

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(mrr, failure_rate, color='blue')
    plt.title('Scatter Plot of MRR vs. Failure Rate')
    plt.xlabel('MRR')
    plt.ylabel('Failure Rate')
    plt.grid(True)

    print("Optimize output")
    print(failure_mrr)

    plt.legend()
    plt.show()
    
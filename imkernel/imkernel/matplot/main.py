
import pandas as pd
import matplotlib.pyplot as plt
def showScatter_plot(file_path):
    df = pd.read_csv(file_path,index_col=0)
    # 获取最后两列的数据
    mrr = df.iloc[:, -2]  
    processing_time = df.iloc[:, -1]
    failure_mrr = df.iloc[:, -2:]

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(mrr, processing_time, color='blue')
    plt.title('Scatter Plot of MRR & Processing time')
    plt.xlabel('MRR')
    plt.ylabel('Processing time')
    plt.grid(True)

    # 找到最大化 MRR 和最小化 Failure Rate 的组合
    best_index = mrr.idxmax() if processing_time.loc[mrr.idxmax()] == processing_time.min() else (mrr / processing_time).idxmax()
    best_mrr = mrr.loc[best_index]
    best_processing_time = processing_time.loc[best_index]

    #标注最佳点
    plt.scatter(best_mrr, best_processing_time, color='red', label='Best Point', s=100)
    plt.legend()
    plt.show()
    
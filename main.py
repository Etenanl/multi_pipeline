
import Common.Flows
if __name__ == '__main__':
    # Run

    # 参数：
        # 数据集地址
        # 读取的flow数量
        # 时间粒度，这里是每1秒分成1000000个时间节点
        # 读取起始位置，从第1000个流开始读
    flows = Common.Flows._Flows("test.csv",10000,1000000,1000)
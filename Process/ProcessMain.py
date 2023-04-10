import os
import csv
from Process import _Process
class _ProcessMain:

    def __init__(self,result_dir = "..\\Source\\Result",analyze_dir = "..\\Source\\Analyze"):
        self.result_dir = result_dir
        self.analyze_dir = analyze_dir
        p = _Process()
        #直接把所有的路径记录下来
        whole_result = []

        whole_result.append([])
        #绝对路径
        input_ab_dir = self.result_dir
        output_ab_dir = self.analyze_dir
        if not os.path.exists(input_ab_dir):
            os.makedirs(input_ab_dir)
        if not os.path.exists(output_ab_dir):
            os.makedirs(output_ab_dir)
        print(input_ab_dir)
        print(output_ab_dir)
        p.clear()

        p.initialize(input_ab_dir)

        whole_result[-1].append(p.write_ARE(output_ab_dir + os.sep + "ARE.txt"))
        whole_result[-1].append(p.write_F1Score(output_ab_dir + os.sep + "F2.txt",0.1))
        whole_result[-1].append(p.write_WMRE(output_ab_dir + os.sep + "WMRE.txt"))
        with open(self.analyze_dir+"\\result.csv","w") as file:
            writer = csv.writer(file)
            writer.writerows(whole_result)
            file.close()

if __name__ == '__main__':


    result_dir = "..\\110"
    analyze_dir = "..\\110"
    process10 = _ProcessMain(result_dir, analyze_dir)

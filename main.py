from unittest import result
import Function.MainProcess
import Process.ProcessMain

if __name__ == '__main__':
    flowcnt = 50000
    solution_list = ["our_solution","packet_cache","parallel_pipeline","single_pipeline"]
    switch_run = Function.MainProcess._Main_Process(FlowCount=flowcnt,ResultPath="Source\\Result\\"+str(flowcnt)+"\\")
    for ele in solution_list:
        switch_run.Process_Select(ele)
        switch_run.Query_Select(ele)
        Process.ProcessMain._ProcessMain(result_dir=".\\Source\\Result\\"+str(flowcnt)+"\\"+ele,analyze_dir=".\\Source\\Analyze\\"+str(flowcnt)+"\\"+ele)
    print("finish")
import csv
import os.path
from unittest import result
import Common.Flows
import Common.Packet
import Utility.Hash
import Switch.Switch

class _Main_Process:
    def __init__(self,DatasetPath="Source\\mawi.csv",GlobalD=2,GlobalK=4,Port_Per_Pipe=4,RunningTime=1,FlowCount=10000,ResultPath = "Source\\Result"):
        self.running_time = RunningTime
        self.time_granularity = 1000000
        self.dataset_path = DatasetPath
        self.global_k = GlobalK
        self.global_d = GlobalD
        self.port_per_pipe = Port_Per_Pipe
        self.main_w = 2**10
        self.flow_count = FlowCount
        # 初始化一个packet
        self.packet = Common.Packet._Packet()
        self.flows = Common.Flows._Flows(path=self.dataset_path,flowCount=self.flow_count,time_granularity=self.time_granularity)
        #print(len(self.flows.flows))
        self.hash= Utility.Hash._Hash()
        self.our_solution = Switch.Switch._Switch(global_d=self.global_d,main_w=self.main_w,pipeline_number=self.global_k,port_per_pipe=self.port_per_pipe,delta_w=2**8)
        self.single_pipeline = Switch.Switch._Single_Piplilne_Switch(global_d=self.global_d, main_w=self.main_w*self.global_k)
        self.parallel_pipeline = Switch.Switch._Parallel_Sketch(global_d=self.global_d,main_w=self.main_w,pipeline_number=self.global_k,port_per_pipe=self.port_per_pipe)
        self.packet_cache_switch = Switch.Switch._Packet_Cache_Switch(global_d=self.global_d,main_w=self.main_w,pipeline_number=self.global_k,port_per_pipe=self.port_per_pipe,queue_maxsize=6)#queue_maxsize=6
        self.result_path = ResultPath

    # 模拟时间进行发送包
    def Main_Process(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        self.flows.Init_flows()
        while time_counter < self.running_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            packet_cnt = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer += 1
                # 处理转发
                for each in time.flows:
                    # 对于每个flow，做以下操作，
                    # 1.找到对应flowID，
                    # flowID = each.flowInfo.flowID
                    in_pipe = self.hash.Hash_Function(str(each.flowInfo.flowID+each.flowInfo.real_send_num),self.global_k,"SHA256")
                    out_pipe = packet_cnt % self.global_k
                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each,in_pipe,out_pipe)
                    # 3.将Packet传递给Switch
                    self.our_solution.Process_Packet(self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1
                    packet_cnt += 1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第" + str(time_counter) + "秒，" + "共有" + str(self.running_time) + "秒，")


    # 模拟时间进行发送包
    def Main_Process_Single(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        self.flows.Init_flows()
        while time_counter < self.running_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer += 1
                # 处理转发
                for each in time.flows:
                    # 对于每个flow，做以下操作，
                    # 1.找到对应flowID，
                    # flowID = each.flowInfo.flowID

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each,0,0)
                    # 3.将Packet传递给Switch
                    self.single_pipeline.Process_Packet(self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第" + str(time_counter) + "秒，" + "共有" + str(self.running_time) + "秒，")

    # 模拟时间进行发送包
    def Main_Process_Parallel(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        self.flows.Init_flows()
        while time_counter < self.running_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            packet_cnt = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer += 1
                # 处理转发
                for each in time.flows:
                    # 对于每个flow，做以下操作，
                    # 1.找到对应flowID，
                    # flowID = each.flowInfo.flowID
                    in_pipe = self.hash.Hash_Function(str(each.flowInfo.flowID+each.flowInfo.real_send_num),self.global_k,"SHA256")
                    out_pipe = packet_cnt % self.global_k

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each,in_pipe,out_pipe)
                    # 3.将Packet传递给Switch
                    self.parallel_pipeline.Process_Packet(self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1
                    packet_cnt += 1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第" + str(time_counter) + "秒，" + "共有" + str(self.running_time) + "秒，")

    def Main_Process_Cache(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        self.flows.Init_flows()
        while time_counter < self.running_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            packet_cnt = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer += 1
                # 处理转发
                for each in time.flows:
                    # 对于每个flow，做以下操作，
                    # 1.找到对应flowID，
                    # flowID = each.flowInfo.flowID
                    in_pipe = self.hash.Hash_Function(str(each.flowInfo.flowID+each.flowInfo.real_send_num),self.global_k,"SHA256")
                    out_pipe = packet_cnt % self.global_k
                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each,in_pipe,out_pipe)
                    # 3.将Packet传递给Switch
                    self.packet_cache_switch.Process_Packet(self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1
                    packet_cnt += 1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第" + str(time_counter) + "秒，" + "共有" + str(self.running_time) + "秒，")


    # 每次发包时修改流信息
    def Update_FlowInfo(self, packet):
        packet.flow.flowInfo.real_send_num += packet.packet_size

    
    # 查询发送所有流之后的结果
    def Query_result(self):
        result_list = []
        moniter_cnt = [0 for i in range(4)]
        for ele_flow in self.flows.flows:
            flowID = ele_flow.flowInfo.flowID
            count_number = self.our_solution.Query(flowID)
            result_list.append([1,flowID,count_number])
            real_send_number = ele_flow.flowInfo.real_send_num
            result_list.append([1,flowID,real_send_number])
            moniter_cnt[ele_flow.flowInfo.moniter] += 1
        filename=self.result_path+"our_solution\\our_solution.csv"
        with open(filename,"w+",newline='') as file:
            writer = csv.writer(file)
            writer.writerows(result_list)
            file.close()
    
    # 查询发送所有流之后的结果
    def Query_result_Single(self):
        result_list = []
        for ele_flow in self.flows.flows:
            flowID = ele_flow.flowInfo.flowID
            count_number = self.single_pipeline.Query(flowID)
            result_list.append([1,flowID,count_number])
            real_send_number = ele_flow.flowInfo.real_send_num
            result_list.append([1,flowID,real_send_number])
        filename=self.result_path+"single_pipeline\\single_pipeline.csv"
        with open(filename,"w+",newline='') as file:
            writer = csv.writer(file)
            writer.writerows(result_list)
            file.close()
        #print(self.single_pipeline.egress_pipeline.main_sketch.cntq)

    # 查询发送所有流之后的结果
    def Query_result_Parallel(self):
        result_list = []
        for ele_flow in self.flows.flows:
            flowID = ele_flow.flowInfo.flowID
            count_number = self.parallel_pipeline.Query(flowID)
            result_list.append([1,flowID,count_number])
            real_send_number = ele_flow.flowInfo.real_send_num
            result_list.append([1,flowID,real_send_number])
        filename=self.result_path+"parallel_pipeline\\parallel_pipeline.csv"
        with open(filename,"w+",newline='') as file:
            writer = csv.writer(file)
            writer.writerows(result_list)
            file.close()

    # 查询发送所有流之后的结果
    def Query_result_Cache(self):
        result_list = []
        moniter_cnt = [0 for i in range(4)]
        for ele_flow in self.flows.flows:
            flowID = ele_flow.flowInfo.flowID
            count_number = self.packet_cache_switch.Query(flowID)
            result_list.append([1,flowID,count_number])
            real_send_number = ele_flow.flowInfo.real_send_num
            result_list.append([1,flowID,real_send_number])
            moniter_cnt[ele_flow.flowInfo.moniter] += 1
        filename=self.result_path+"packet_cache\\packet_cache.csv"
        with open(filename,"w+",newline='') as file:
            writer = csv.writer(file)
            writer.writerows(result_list)
            file.close()
    
    def Process_Select(self,solution):
        if solution == "our_solution":
            self.Main_Process()
        elif solution == "packet_cache":
            self.Main_Process_Cache()
        elif solution == "parallel_pipeline":
            self.Main_Process_Parallel()
        elif solution == "single_pipeline":
            self.Main_Process_Single()
        else:
            print("wrong type")
    
    def Query_Select(self,solution):
        if solution == "our_solution":
            self.Query_result()
        elif solution == "packet_cache":
            self.Query_result_Cache()
        elif solution == "parallel_pipeline":
            self.Query_result_Parallel()
        elif solution == "single_pipeline":
            self.Query_result_Single()
        else:
            print("wrong type")        

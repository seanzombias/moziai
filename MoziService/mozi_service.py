# -*- coding:utf-8 -*-
# coding=utf-8
import MoziService.MoZiPython as MoZiPython
import pylog
import time
from MoziService.entitys.scenario import CScenario
from websocket import create_connection
import json
import grpc
import MoziService.GRPCServerBase_pb2 as GRPCServerBase_pb2
import MoziService.GRPCServerBase_pb2_grpc as GRPCServerBase_pb2_grpc

from MoziService import situation_paser


def get_red_missile_info(all_info_dict):
    red_missile_info = {}
    red_missile_guid = []
    for guid in list(all_info_dict.keys()):
        item = all_info_dict[guid]
        if item["ClassName"] == "CAircraft":
            red_missile_guid.append(guid)
            red_missile_info[guid] = item
    return red_missile_info


class MoziService():
    """类功能说明"""

    def __init__(self, server_ip, port, scenario_name='', compression=5, continuous=False, connect_mode=1):
        """两个数字相加，并返回结果"""
        self.mozi_task = None
        self.connect_mode = connect_mode
        self.exect_flag = True
        self.server_ip = server_ip
        self.server_port = port
        self.scenario_name = scenario_name
        self.compression = compression
        self.continuous = continuous
        self.websocket_connect = None
        conn = grpc.insecure_channel(server_ip + ':' + str(port))
        self.client = GRPCServerBase_pb2_grpc.gRPCStub(channel=conn)
        self.all_guid = []
        self.all_info_dict = {}
        # self.red_info_dict = {}

    def load_scenario(self, plat="windows"):
        '''
        加载想定
        plat 服务器是Windows版还是Linux版
        '''
        scenario_file = self.scenario_name
        if plat == "windows":
            ret = self.scenEditLoadScenario(scenario_file, "false")
        else:
            ret = self.loadScenario(scenario_file, "Play")
        load_success = False
        for i in range(30):
            value = self.getScenarioIsLoad()
            if str(value) == "'Yes'":
                pylog.info("scenario load sucess")
                load_success = True
                break
            pylog.info("sleep a second")
            time.sleep(1)

        if not load_success:
            pylog.error("can not load scenario:%s" % scenario_file)
            return None
        scenario = CScenario(self)
        return scenario

    def update_class_dic(self, class_dic, item, key="ClassName"):
        '''
        
        '''
        # pylog.info(item)
        # pylog.info(key)
        ret = class_dic.get(item[key], "")

        if ret:
            ret.append(item)
        else:
            lt = []
            lt.append(item)
            class_dic[item[key]] = lt

    def paser_situation(self):
        '''
        
        '''
        situation_paser.paser_situation(self.all_info_dict)

    def get_entity(self, guid):
        '''
        
        '''
        return situation_paser.get_entity_from_guid(guid, self.all_info_dict, self)

    def init_situation(self, scenario):
        '''
        初始化态势
        '''
        scenario.situation.init_situation(self, scenario)
        self.all_guid = scenario.situation.all_guid
        self.all_info_dict = scenario.situation.all_info_dict
        # self.paser_situation()

    def show_side_info(self, item):
        '''
        show side info
        '''
        count = 0
        for key in item:
            pylog.info("count:%s %s:%s" % (count, key, item[key]))
            count += 1

    def update_situation(self, scenario):
        """
        更新态势
        :return:
        """
        situation_data = scenario.situation.update_situation(self, scenario)
        situation_paser.update_situation(situation_data, self.all_info_dict)

    def run_simulate(self):
        '''
        数功能：开始推演
        函数类型：推演函数
        param :
        return : lua执行成功/lua执行失败
        '''
        lua_str = "ReturnObj(Hs_SimRun(true))"
        return self.sendAndRecv(lua_str)

    def set_simulate_compression(self, n_compression=4):
        """
        函数功能：设置想定推演倍速
        函数类型：推演函数
        param ：n_compression推演时间步长档位（0：1 秒，1：2 秒，2：5 秒，3：15 秒，4：30 秒，
                5：1 分钟，6：5 分钟，7：15 分钟，8：30 分钟）。
        return ： lua执行成功/lua执行失败
        """
        lua_str = "ReturnObj(Hs_SetSimCompression(%d))" % n_compression
        ret = self.sendAndRecv(lua_str)
        return ret


    def set_compression_mode(self, b_mode):
        """
        函数功能：设置想定推演模式
        函数类别：推演函数
        :param b_mode: 想定模式（推演模式/编辑模式）
        :return:
        """
        lua_str = "Hs_SetSimMode(%s)" % str(b_mode).lower()
        return self.sendAndRecv(lua_str)

    def connect_mozi_server(self, websocket_server, websocket_port):
        """
        连接墨子服务器
        param ：
        websocket_server 要连接的服务器的ip
        websocket_port 要连接的服务器的端口
        :return:
        """
        pylog.info("connect_mozi_server")
        if self.connect_mode == 1:
            self.mozi_task = MoZiPython.MoZi(self.server_ip, self.server_port)
    #
            self.ai_server = self.server_ip
            self.ai_port = self.server_port
            return True
    #
        #server_address = r"ws://%s:%d/websocket" % ('60.205.207.206', 9998)
        server_address = r"ws://%s:%d/websocket" % (websocket_server, websocket_port)
        pylog.info(server_address)
        for i in range(10):
            try:
                self.websocket_connect = create_connection(server_address)
                break
            except:
                pylog.info("can not connect to %s." % server_address)
                time.sleep(2)
                self.websocket_connect = None
    #
        if self.websocket_connect is None:
            pylog.warning("Interrupted, can not connect to %s." % server_address)
            return False
    #
        self.websocket_connect.send("{\"RequestType\":\"StartServer\"}")
        result = self.websocket_connect.recv()
        print("connect server result:%s" % result)
        jsons = json.loads(result)
        self.ai_server = jsons['IP']
        self.ai_port = jsons['AIPort']
        self.mozi_task = MoZiPython.MoZi(self.ai_server, self.ai_port)
    #
        #if platform.system() != 'Darwin':
            ## 修改客户端配置文件
            #inipath = self.client_path_init
            #conf = configparser.ConfigParser()
            #conf.read(inipath)
            #conf.set('ConnectServer', "ip", jsons['IP'])
            #conf.write(open(inipath, "r+"))
            #conf.set('ConnectServer', "port", str(jsons['Port']))
            #conf.write(open(inipath, "r+"))
            #conf.set('ConnectServer', "name", str(jsons['Federate']))
            #conf.write(open(inipath, "r+"))
    #
        return True

    def get_current_time(self):
        '''
        得到当前时间
        param :
        return : 时间毫秒值
        '''
        lua = "ReturnObj(ScenEdit_CurrentTime())"
        ret_time = self.mozi_task.sendAndRecv(lua)
        pylog.info("%s\n" % ret_time)
        return ret_time

    def set_run_mode(self):
        '''
        设置运行模式，智能体决策想定是否暂停
        
        '''
        if self.continuous:
            return self.sendAndRecv("SETPYTHONMODEL(FALSE)")
        else:
            return self.sendAndRecv("SETPYTHONMODEL(TRUE)")

    def suspend_simulate(self):
        """
        函数功能：设置环境暂停
        函数类别：推演函数
        return ：
        """
        lua_str = "Hs_SimStop()"
        self.sendAndRecv(lua_str)

    def get_all_units_info_from_list(self, unit_list):
        '''
        获取所有单元详细信息
        param
        unit_list ： 所有单元集合
        return ： 单元详细信息集合
        '''
        if unit_list:
            unit_info_dic_list = []
            for i in range(len(unit_list)):
                lua_str = """
                unit = ScenEdit_GetUnit({guid='%s'})
                print(unit)
                """ % unit_list[i]["guid"]

                pylog.debug(lua_str, "./cmd_lua/log_lua")
                unit_info = self.sendAndRecv(lua_str)
                pylog.debug(unit_info, "./cmd_lua/log_lua")

                dic = self.paser_unit_info(unit_info)
                if dic and dic["name"] != "Pr.2235.0 “戈尔什科夫海军元帅”级护卫舰":
                    unit_info_dic_list.append(dic)

            return unit_info_dic_list
        else:
            return []

    def paser_unit_info(unit_info):
        '''
        解析单元信息        
        param ：
        unit_info ： 单元信息集合
        return ： 单元字典
        '''
        # pylog.info(unit_str)
        start_index = 0
        end_index = 0
        for i in range(len(unit_info)):
            if unit_info[i] == "{":
                start_index = i
            elif unit_info[i] == "}":
                end_index = i
        con = unit_info[start_index + 1: end_index]
        # pylog.info(con)
        lt = con.split("',")
        # pylog.info(lt)
        dic = {}
        for i in range(len(lt)):
            item = lt[i].strip()
            if item != "":
                item_lt = item.split("=")
                # pylog.info(item_lt)
                dic[item_lt[0].strip()] = item_lt[1].replace("'", "").replace('"', "").strip()

        return dic

    def taishi_reset(self):
        '''
        态势重置函数
        '''
        self._reset()
        time.sleep(3)
        step_interval = 30
        pylog.info("Hs_OneTimeStop:%d" % step_interval)
        self.sendAndRecv("Hs_OneTimeStop('Stop', %d)" % step_interval)
        self.run_simulate()
        self.create_get_situation_process()
        self.step()

    def sendAndRecv(self, name_):
        '''
        gRPC发送和接收服务端消息方法
        '''
        if self.exect_flag:
            response = self.client.GrpcConnect(GRPCServerBase_pb2.GrpcRequest(name=name_))
            length = response.length
            if len(response.message) == length:
                return response.message
            else:
                return "数据错误"
        else:
            self.command_num += 1
            self.command_string += name_ + '\n'

    def scenEditLoadScenario(self, scenPath, isDeduce):
        '''
        scenPath 想定文件的相对路径（仅支持.scen文件）
        isDeduce 模式 "false"想定编辑模式 "true"想定推演模式
        '''
        return self.sendAndRecv("Hs_ScenEdit_LoadScenario('{}', {})".format(scenPath, isDeduce))

    def loadScenario(self, path, model):
        '''
        path 想定文件的相对路径（仅支持XML文件）
        model 模式 "Edit"想定编辑模式 "Play"想定推演模式
        '''
        return self.sendAndRecv("Hs_PythonLoadScenario('{}', '{}')".format(path, model))

    def getScenarioIsLoad(self):
        '''
        获取想定是否加载
        '''
        return self.sendAndRecv("print(Hs_GetScenarioIsLoad())")

    def save_scenario(self):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：保存当前已经加载的想定
        函数类别：推演所用的函数
        '''
        return self.sendAndRecv("Hs_ScenEdit_SaveScenario()")

    def save_as_scenario(self, scenario_name):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：另存当前已经加载的想定
        函数类别：推演所用的函数
        '''
        return self.sendAndRecv("Hs_ScenEdit_SaveAsScenario('{}')".format(scenario_name))

    def create_scenario(self):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：新建想定
        函数类别：推演所用的函数
        '''
        return self.sendAndRecv("Hs_ScenEdit_CreateNewScenario()")

    def decribe_scenario(self, scenariotitle, setdescription):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：想定的描述
        函数类别：推演所用的函数
        '''
        return self.sendAndRecv("Hs_SetScenarioDescribe({'{}','{}')".format(scenariotitle, setdescription))

    def get_scenario_title(self):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：想定的描述表述
        函数类别：推演所用的函数
        '''
        return self.sendAndRecv("Hs_SetScenarioDescribe()")

    def featuresReakismSet(self, gunfireControl, unlimitedBaseMags, aCDamage):
        '''
        作者：赵俊义
        日期：2020-3-7
        功能说明：设置仿真精细度
        函数类别：推演所用的函数
        gunfireControl ：高精度火控算法
        unlimitedBaseMags： 海空弹药不受限
        aCDamage ：飞机高精度毁伤模型

        '''
        return self.sendAndRecv(
            " Hs_FeaturesReakismSet({DetailedGunFirControl =%s,UnlimitedBaseMags = %s,AircraftDamage = %s})" % (
                gunfireControl, unlimitedBaseMags, aCDamage))

    def sim_increase_compression(self):
        """
        作者：赵俊义
        日期: 2020-3-11
        函数功能：将推演时间步长提高 1 个档位
        函数类别: 推演函数
        :return:
        """
        return self.sendAndRecv("Hs_SimIncreaseCompression()")

    def sim_decrease_compression(self):
        """
        作者：赵俊义
        日期: 2020-3-11
        函数功能：将推演时间步长提高 1 个档位
        函数类别: 推演函数
        :return:
        """
        return self.sendAndRecv("Hs_SimDecreaseCompression()")

    def end_scenario(self):
        """
        函数功能：终止当前想定，进入参演方评估并给出评估结果
        函数类别：推演函数
        :return:
        """
        return self.sendAndRecv("ScenEdit_EndScenario()")

    def emulate_no_console(self):
        """
        作者：解洋
        日期：2020-3-12
        函数功能：模拟无平台推演
        函数类型：编辑函数
        :return:
        """
        return self.sendAndRecv("Tool_EmulateNoConsole()")

    '''
    从文件中运行脚本
    文件目录必须是“推演系统根目录/Lua”，否则不能打开。可以指定子目录如 'library/cklib.lua' ，其形式为
    "推演系统根目录/Lua/子目录”，也可用 ScenEdit_UseAttachment 作为附件间接加载。
    script
    '''

    def runScript(self, script):
        """
        作者：解洋
        日期：2020-3-11
        函数功能：运行服务端 Lua 文件夹下的 Lua 文件（*.lua）。
        函数类型：推演函数
        :param script:字符串。服务端 Lua 文件夹下包括 Lua 文件名在内的相对路径
        :return:
        """
        return self.sendAndRecv("ScenEdit_RunScript('{}')".format(script))

    '''
    根据键设置永久性键值的值
    kye 键
    value 值
    '''

    def setKeyValue(self, key, value):
        """
        作者：解洋
        日期：2020-3-11
        函数功能：在系统中有一预设的“键-值”表，本函数向“键-值”表添加一条记录。
        函数类型：推演函数
        :param key:键”的内容
        :param value:“值”的内容
        :return:
        """
        return self.sendAndRecv("ScenEdit_SetKeyValue('{}','{}')".format(key, value))


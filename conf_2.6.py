__version__ = "2.6"

import sys
if sys.version_info < (3, 10, 5):
    print('Please upgrade your Python version to 3.10.4 or higher')
    sys.exit()
import argparse
from dataclasses import dataclass
import traceback
# pip3 install ipcalc
import ipcalc

# pip3 install pandas
# pip3 install openpyxl
import pandas as pd
import yaml

# выставим ширину вывода pandas-ы
pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 50)

# def read_excel(excel_file, excel_sheet):
#     #
#     # Прочесть параметры AF4, и вернуть в виде таблицы
#     #

#     # открываем файл Excel, и загружаем лист из него
#     data = pd.read_excel(excel_file, sheet_name=excel_sheet)
#     df = pd.DataFrame(data, columns=['param', 'node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8', 'node9', 'node10', 'node11', 'node12', 'node13', 'node14', 'node15', 'node16', 'node17', 'node18', 'node19'])
#     #print(df)
#     return(df)

def read_excel(excel_file, excel_sheet):
    #
    # Прочесть параметры AF4, и вернуть в виде таблицы
    #

    # Генерируем список колонок от node1 до node30
    node_columns = [f'node{i}' for i in range(1, 31)]
    
    # Полный список колонок: param + все node
    columns = ['param'] + node_columns
    
    # открываем файл Excel, и загружаем лист из него
    data = pd.read_excel(excel_file, sheet_name=excel_sheet)
    df = pd.DataFrame(data, columns=columns)
    #print(df)
    return df

def dns(df):
    #
    # DNS
    #
    cmd = []
    cmd.append("# Настройка DNS")
    if (df.iloc[31]['node1'] != ""):
        cmd.append('echo "nameserver ' + df.iloc[31]['node1'] + '" > /etc/resolv.conf')
        if (df.iloc[31]['node2'] != ""):
            cmd.append('echo "nameserver ' + df.iloc[31]['node2'] + '" >> /etc/resolv.conf')
            if (df.iloc[31]['node3'] != ""):
                cmd.append('echo "nameserver ' + df.iloc[31]['node3'] + '" >> /etc/resolv.conf')
    return(cmd)

def ntp(df):
    #
    # NTP
    #
    cmd = []
    if (df.iloc[29]['node1'] != ""):
        cmd.append("# Настройка NTP")
        cmd.append('wsc -c "dhcp set ntp_servers false"')
        cmd.append('wsc -c "ntp add ' + df.iloc[29]['node1'] + '"')
        if (df.iloc[29]['node2'] != ""):
            cmd.append('wsc -c "ntp add ' + df.iloc[29]['node2'] + '"')
            if (df.iloc[29]['node3'] != ""):
                cmd.append('wsc -c "ntp add ' + df.iloc[29]['node3'] + '"')
    return(cmd)

def timezone(df):
    cmd = []
    cmd.append('wsc -c "timezone ' + df.iloc[35]['param'] + '"')
    return(cmd)

def vip(df):
    #
    # VIP
    #
    cmd = []
    cmd.append('wsc -c "vip set monitoring ' + df.iloc[32]['node1'] + '"')
    cmd.append('wsc -c "vip set manage ' + df.iloc[33]['node1'] + '"')
    cmd.append('wsc -c "vip set border ' + df.iloc[34]['node1'] + '"')
    return(cmd)

def get_af_nodes(df):
    #
    # получаем данные по всем узлам
    #

    global af_nodes
    af_nodes = []
    for x in range(1, 31):
        af_nodes.append(AF_nodes(node_role=str(df.iloc[0]["node"+str(x)]),
                              ssh_password=str(df.iloc[1]["node" + str(x)]),
                              hostname=str(df.iloc[2]["node" + str(x)]),
                              eth0_name=str(df.iloc[3]["node" + str(x)]),
                              eth0_ip=str(df.iloc[4]["node" + str(x)]),
                              eth0_netmask=str(df.iloc[5]["node" + str(x)]),
                              eth0_gw=str(df.iloc[6]["node" + str(x)]),
                              eth0_role=str(df.iloc[7]["node" + str(x)]),
                              eth0_mode=str(df.iloc[8]["node" + str(x)]),
                              eth1_name=str(df.iloc[9]["node" + str(x)]),
                              eth1_ip=str(df.iloc[10]["node" + str(x)]),
                              eth1_netmask=str(df.iloc[11]["node" + str(x)]),
                              eth1_gw=str(df.iloc[12]["node" + str(x)]),
                              eth1_role=str(df.iloc[13]["node" + str(x)]),
                              eth1_mode=str(df.iloc[14]["node" + str(x)]),
                              eth2_name=str(df.iloc[15]["node" + str(x)]),
                              eth2_ip=str(df.iloc[16]["node" + str(x)]),
                              eth2_netmask=str(df.iloc[17]["node" + str(x)]),
                              eth2_gw=str(df.iloc[18]["node" + str(x)]),
                              eth2_role=str(df.iloc[19]["node" + str(x)]),
                              eth2_mode=str(df.iloc[20]["node" + str(x)]),
                              eth3_name=str(df.iloc[21]["node" + str(x)]),
                              eth3_ip=str(df.iloc[22]["node" + str(x)]),
                              eth3_netmask=str(df.iloc[23]["node" + str(x)]),
                              eth3_gw=str(df.iloc[24]["node" + str(x)]),
                              eth3_role=str(df.iloc[25]["node" + str(x)]),
                              eth3_mode=str(df.iloc[26]["node" + str(x)]),
                              node_dgw=str(df.iloc[27]["node" + str(x)]),
                              bond0_int1=str(df.iloc[38]["node" + str(x)]), 
                              bond0_int2=str(df.iloc[39]["node" + str(x)]), 
                              bond0_mode=str(df.iloc[40]["node" + str(x)]), 
                              bond0_tag1=str(df.iloc[41]["node" + str(x)]), 
                              bond0_tag2=str(df.iloc[42]["node" + str(x)]), 
                              bond0_tag3=str(df.iloc[43]["node" + str(x)]), 
                              bond0_tag4=str(df.iloc[44]["node" + str(x)]), 
                              bond1_int1=str(df.iloc[45]["node" + str(x)]), 
                              bond1_int2=str(df.iloc[46]["node" + str(x)]), 
                              bond1_mode=str(df.iloc[47]["node" + str(x)]), 
                              bond1_tag1=str(df.iloc[48]["node" + str(x)]), 
                              bond1_tag2=str(df.iloc[49]["node" + str(x)]), 
                              bond1_tag3=str(df.iloc[50]["node" + str(x)]), 
                              bond1_tag4=str(df.iloc[51]["node" + str(x)]), 
                              bond2_int1=str(df.iloc[52]["node" + str(x)]), 
                              bond2_int2=str(df.iloc[53]["node" + str(x)]), 
                              bond2_mode=str(df.iloc[54]["node" + str(x)]), 
                              bond2_tag1=str(df.iloc[55]["node" + str(x)]), 
                              bond2_tag2=str(df.iloc[56]["node" + str(x)]), 
                              bond2_tag3=str(df.iloc[57]["node" + str(x)]), 
                              bond2_tag4=str(df.iloc[58]["node" + str(x)]), 
                              bond3_int1=str(df.iloc[59]["node" + str(x)]), 
                              bond3_int2=str(df.iloc[60]["node" + str(x)]), 
                              bond3_mode=str(df.iloc[61]["node" + str(x)]), 
                              bond3_tag1=str(df.iloc[62]["node" + str(x)]), 
                              bond3_tag2=str(df.iloc[63]["node" + str(x)]), 
                              bond3_tag3=str(df.iloc[64]["node" + str(x)]), 
                              bond3_tag4=str(df.iloc[65]["node" + str(x)])))

@dataclass
class AF_nodes:
    """Узел AF"""
    node_role: str
    hostname: str
    ssh_password: str
    node_dgw: str
    eth0_name: str
    eth1_name: str
    eth2_name: str
    eth3_name: str
    eth0_ip: str
    eth0_netmask: str
    eth0_gw: str
    eth0_role: str
    eth0_mode: str
    eth1_ip: str
    eth1_netmask: str
    eth1_gw: str
    eth1_role: str
    eth1_mode: str
    eth2_ip: str
    eth2_netmask: str
    eth2_gw: str
    eth2_role: str
    eth2_mode: str
    eth3_ip: str
    eth3_netmask: str
    eth3_gw: str
    eth3_role: str
    eth3_mode: str
    bond0_int1: str
    bond0_int2: str
    bond0_mode: str
    bond0_tag1: str
    bond0_tag2: str
    bond0_tag3: str
    bond0_tag4: str
    bond1_int1: str
    bond1_int2: str
    bond1_mode: str
    bond1_tag1: str
    bond1_tag2: str
    bond1_tag3: str
    bond1_tag4: str
    bond2_int1: str
    bond2_int2: str
    bond2_mode: str
    bond2_tag1: str
    bond2_tag2: str
    bond2_tag3: str
    bond2_tag4: str
    bond3_int1: str
    bond3_int2: str
    bond3_mode: str
    bond3_tag1: str
    bond3_tag2: str
    bond3_tag3: str
    bond3_tag4: str



def get_ip(node: AF_nodes, eth_role):
    #
    # получить IP-адрес интерфейса с указанной ролью
    #
    match eth_role:
        case node.eth0_role:
            return node.eth0_ip, node.eth0_name, node.eth0_netmask, node.eth0_gw
        case node.eth1_role:
            return node.eth1_ip, node.eth1_name, node.eth1_netmask, node.eth1_gw
        case node.eth2_role:
            return node.eth2_ip, node.eth2_name, node.eth2_netmask, node.eth2_gw
        case node.eth3_role:
            return node.eth3_ip, node.eth3_name, node.eth3_netmask, node.eth3_gw
        case _:
            return "None","None","None","None"

def create_config(df):
    clstr = []
    cmd = []
    hstn = []

    i = len(af_nodes)
    while i != 0:
        i -= 1
        tasks = []
        if (af_nodes[i].node_role == ""):
            continue
            #break
        elif (len(af_nodes[i].node_role) > 0 and (af_nodes[i].ssh_password == "" or af_nodes[i].hostname == "" or af_nodes[i].eth0_ip == "")):
            print("Заполните все цветные поля или очистите!")
            exit(1)
        else:
            cmd.append('\n#\n# commands for ' + str(i+1) + ' node\n#')
            cmd.append('# зайти в ОС через консоль под login/pass - pt/positive\n#')
            cmd.append('# все команды выполняются из-под root')
            cmd.append('sudo su')
            cluster_ip = get_ip(af_nodes[i], "CLUSTER")[0]
            if cluster_ip == "None":
                print("Ошибка, не определен интерфейс с ролью CLUSTER!")
                exit(1)
            mgmt_ip, mgmt_eth, mgmt_mask, mgmt_gw = get_ip(af_nodes[i], "MGMT")
            if (mgmt_ip == "None"):
                mgmt_ip, mgmt_eth, mgmt_mask, mgmt_gw = get_ip(af_nodes[i], "WAN")
                if (mgmt_ip == "None"):
                    print("Ошибка, не определен интерфейс с ролью MGMT/WAN!")
                    exit(1)
            #if (i != 0):
            #    connect = 'sshpass -p ' + af_nodes[i].ssh_password + ' ssh -o StrictHostKeyChecking=accept-new -tt pt@' + \
            #              cluster_ip + ' -p 22013 bash -c \'echo ' + af_nodes[i].ssh_password + ' | sudo -S sh << EOF\n' + \
            #              af_nodes[i].ssh_password + '\n'
            #    cmd.append(connect)

            #Настраиваем бонды, если надо
            if df.iloc[37]['param'] == 'yes':
                #(bond_name,bond_int1,bond_int2,bond_mode,bond_tag1,bond_tag2,bond_tag3,bond_tag4)
                for bond_num in range(4):  # bond0, bond1, bond2, bond3
                    result = bonds(
                        bond_name=f'bond{bond_num}',
                        bond_int1=getattr(af_nodes[i], f'bond{bond_num}_int1'),
                        bond_int2=getattr(af_nodes[i], f'bond{bond_num}_int2'),
                        bond_mode=getattr(af_nodes[i], f'bond{bond_num}_mode'),
                        bond_tag1=getattr(af_nodes[i], f'bond{bond_num}_tag1'),
                        bond_tag2=getattr(af_nodes[i], f'bond{bond_num}_tag2'),
                        bond_tag3=getattr(af_nodes[i], f'bond{bond_num}_tag3'),
                        bond_tag4=getattr(af_nodes[i], f'bond{bond_num}_tag4')
                    )
                    cmd += result
                    tasks += result
            cmd.append('# настраиваем интерфейс управления')
            cmd.append("ifconfig " + mgmt_eth + " up")
            cmd.append("ip a add " + mgmt_ip + "/" + mgmt_mask + " dev " + mgmt_eth)
            if (len(mgmt_gw) > 0):
                cmd.append("ip route add default via " + mgmt_gw)
            cmd.append('#\n# подключаемся по SSH к серверу на MGMT интерфейс: ' + mgmt_ip + ":22013")
            cmd.append('# и выполняем команды ниже\n#')
            cmd.append('sudo su')
            # cmd.append('# устанавливаем tmux, из-под которого будем работать (желательно изучить работу с ним)')
            cmd.append('запускаем tmux')

            #Отключаем cloud-init
            if df.iloc[36]['param'] == 'yes':
                cmd.append('# отключаем cloud-init')
                cmd.append('touch /etc/cloud/cloud-init.disabled')
                tasks.append('touch /etc/cloud/cloud-init.disabled')
                cmd.append('# отключаем автоматическое управление сетевыми интерфейсами в cloud-init')
                cmd.append('mkdir -p /etc/cloud/cloud.cfg.d')
                tasks.append('mkdir -p /etc/cloud/cloud.cfg.d')
                cmd.append('echo "network: {config: disabled}" > /etc/cloud/cloud.cfg.d/98-disable-network-config.cfg')
                tasks.append('echo "network: {config: disabled}" > /etc/cloud/cloud.cfg.d/98-disable-network-config.cfg')
            cmd.append('# назначаем VIP-ы для manage, monitoring, border')
            cmd += vip(df)
            #Тут GW выбирается по роли интерфейса, старая версия
            #gwint = df.iloc[23]['param']
            # eth0, eth1, eth2, eth3 = [],[],[],[]
            for eth_num in range(4):  # eth0, eth1, eth2, eth3
                result = eth(
                    ip_addr=getattr(af_nodes[i], f'eth{eth_num}_ip'),
                    mask=getattr(af_nodes[i], f'eth{eth_num}_netmask'), 
                    gw=getattr(af_nodes[i], f'eth{eth_num}_gw'),
                    role=getattr(af_nodes[i], f'eth{eth_num}_role'),
                    ethN=getattr(af_nodes[i], f'eth{eth_num}_name'),
                    mode=getattr(af_nodes[i], f'eth{eth_num}_mode'),
                    gwint=af_nodes[i].node_dgw
                )
                cmd.extend(result)
                tasks.extend(result)
            '''
            cmd += eth(ip_addr=af_nodes[i].eth0_ip, mask=af_nodes[i].eth0_netmask, gw=af_nodes[i].eth0_gw, role=af_nodes[i].eth0_role, ethN=af_nodes[i].eth0_name, mode=af_nodes[i].eth0_mode, gwint=af_nodes[i].node_dgw)
            tasks += eth(ip_addr=af_nodes[i].eth0_ip, mask=af_nodes[i].eth0_netmask, gw=af_nodes[i].eth0_gw, role=af_nodes[i].eth0_role, ethN=af_nodes[i].eth0_name, mode=af_nodes[i].eth0_mode, gwint=af_nodes[i].node_dgw)
            cmd += eth(ip_addr=af_nodes[i].eth1_ip, mask=af_nodes[i].eth1_netmask, gw=af_nodes[i].eth1_gw, role=af_nodes[i].eth1_role, ethN=af_nodes[i].eth1_name, mode=af_nodes[i].eth1_mode, gwint=af_nodes[i].node_dgw)
            tasks += eth(ip_addr=af_nodes[i].eth1_ip, mask=af_nodes[i].eth1_netmask, gw=af_nodes[i].eth1_gw, role=af_nodes[i].eth1_role, ethN=af_nodes[i].eth1_name, mode=af_nodes[i].eth1_mode, gwint=af_nodes[i].node_dgw)
            cmd += eth(ip_addr=af_nodes[i].eth2_ip, mask=af_nodes[i].eth2_netmask, gw=af_nodes[i].eth2_gw, role=af_nodes[i].eth2_role, ethN=af_nodes[i].eth2_name, mode=af_nodes[i].eth2_mode, gwint=af_nodes[i].node_dgw)
            tasks += eth(ip_addr=af_nodes[i].eth2_ip, mask=af_nodes[i].eth2_netmask, gw=af_nodes[i].eth2_gw, role=af_nodes[i].eth2_role, ethN=af_nodes[i].eth2_name, mode=af_nodes[i].eth2_mode, gwint=af_nodes[i].node_dgw)
            cmd += eth(ip_addr=af_nodes[i].eth3_ip, mask=af_nodes[i].eth3_netmask, gw=af_nodes[i].eth3_gw, role=af_nodes[i].eth3_role, ethN=af_nodes[i].eth3_name, mode=af_nodes[i].eth3_mode, gwint=af_nodes[i].node_dgw)
            tasks += eth(ip_addr=af_nodes[i].eth3_ip, mask=af_nodes[i].eth3_netmask, gw=af_nodes[i].eth3_gw, role=af_nodes[i].eth3_role, ethN=af_nodes[i].eth3_name, mode=af_nodes[i].eth3_mode, gwint=af_nodes[i].node_dgw)
            '''
            # eth_arrays = [eth0, eth1, eth2, eth3]
            # for ethui in eth_arrays:
            #     cmd.append(ethui)   # Добавляем текущий список в cmd
            #     #tasks.append(ethui)
            #Ищем роль и ван и LAN на воркер или base-worker или на base ноде, а если LAN нет, то добавляем роль LAN к интерфейсу с ролью WAN
            if af_nodes[i].node_role == 'worker' or af_nodes[i].node_role == 'base-worker' or af_nodes[i].node_role == 'base':
                wan_found = False
                lan_object_name = None
                mgmt_object_name = None
                wan_object_name = None  # Добавляем переменную для хранения имени интерфейса с ролью WAN

                # Проверяем все eth интерфейсы на ноде
                for j in range(4):
                    role_key = f"eth{j}_role"
                    name_key = f"eth{j}_name"

                    role_value = getattr(af_nodes[i], role_key, None)  # Получаем значение атрибута role
                    name_value = getattr(af_nodes[i], name_key, None)  # Получаем значение атрибута name

                    if role_value == "WAN":
                        wan_found = True
                        wan_object_name = name_value  # Сохраняем имя интерфейса с ролью WAN
                    elif (role_value == "LAN") and lan_object_name is None:
                        lan_object_name = name_value
                    elif (role_value == "MGMT") and mgmt_object_name is None:
                        mgmt_object_name = name_value

                # Если WAN не найден, добавляем роль WAN к интерфейсу с ролью LAN, если такого нет, то к MGMT
                if not wan_found:
                    if lan_object_name:
                        cmd.append('wsc -c "if set ' + lan_object_name + ' role WAN"')
                        tasks.append('wsc -c "if set ' + lan_object_name + ' role WAN"')
                    elif mgmt_object_name:
                        cmd.append('wsc -c "if set ' + mgmt_object_name + ' role WAN"')
                        tasks.append('wsc -c "if set ' + mgmt_object_name + ' role WAN"')
                        cmd.append('wsc -c "if set ' + mgmt_object_name + ' role LAN"')
                        tasks.append('wsc -c "if set ' + mgmt_object_name + ' role LAN"')
                # Если WAN есть, а LAN нет, добавляем роль LAN к интерфейсу WAN
                elif wan_found and not lan_object_name:
                    cmd.append('wsc -c "if set ' + wan_object_name + ' role LAN"')
                    tasks.append('wsc -c "if set ' + wan_object_name + ' role LAN"')

            cmd += dns(df)
            ntp_str = ntp(df)
            if (len(ntp_str) > 1):
                cmd += ntp_str
            cmd.append('# задаем hostname')
            hstn.append('echo "' + cluster_ip + " " + af_nodes[i].hostname + '" >> /etc/hosts')
            cmd.append('hostnamectl set-hostname ' + af_nodes[i].hostname)
            tasks.append('hostnamectl set-hostname ' + af_nodes[i].hostname)
            if i != 0:
                cmd.append('echo "127.0.0.1 localhost" > /etc/hosts')
                tasks.append('echo "127.0.0.1 localhost" > /etc/hosts')
                cmd.append('echo "127.0.1.1 ' + af_nodes[i].hostname + '" >> /etc/hosts')
                tasks.append('echo "127.0.1.1 ' + af_nodes[i].hostname + '" >> /etc/hosts')
                cmd.append('echo "'+ cluster_ip + " " + af_nodes[i].hostname + '" >> /etc/hosts')
                tasks.append('echo "'+ cluster_ip + " " + af_nodes[i].hostname + '" >> /etc/hosts')
            cmd.append('# задаем Timezone')
            cmd += timezone(df)

            cmd.append('\n#\n# после этой команды возможно прервется сеть, необходимо переподключиться в "sudo tmux a" и убедиться что commit прошел успешно и продолжить установку\n#')
            cmd.append('wsc -c "config commit"')
            # commands.append('wsc -c "config commit"')

            role = ""
            if (af_nodes[i].node_role == "base-worker" or af_nodes[i].node_role == "base"):
                if (i == 0 or i == 1):
                    role = "master,worker-backend,postgresql,rabbitmq,minio,clickhouse"
                # если 5 узлов с ролью управления
                elif (i == 3 or i == 4) and (af_nodes[4].node_role == "base-worker" or af_nodes[4].node_role == "base"):
                    role = "master,worker-backend,postgresql,rabbitmq,minio,clickhouse"
                else:
                    role = "master,worker-backend,postgresql,rabbitmq,minio"
            elif (af_nodes[i].node_role == "worker"):
                role = "worker-traffic"
            if (af_nodes[i].node_role == "base-worker"):
                role = role + ",worker-traffic"

            clstr.append('wsc -c \'inventory node set ' + af_nodes[i].hostname + ' cluster_ip ' + cluster_ip + ' role ' + role + ' port 22013 user_name pt user_password ' +
                       af_nodes[i].ssh_password + ' sudo_password ' + af_nodes[i].ssh_password + '\'')
            # поскольку внизу массив clstr читаем с конца, то здесь обратный порядок (в начале set, потом add)
            clstr.append('wsc -c "inventory node add ' + af_nodes[i].hostname + '"')

            if (i != 0):
                #cmd.append('exit\nEOF\'\n')
                cmd.append('exit')
            if(i == 0):
                if (len(hstn) >= 1):
                    cmd.append('echo "127.0.0.1 localhost" > /etc/hosts')
                    tasks.append('echo "127.0.0.1 localhost" > /etc/hosts')
                    cmd.append('echo "127.0.1.1 ' + af_nodes[i].hostname + '" >> /etc/hosts')
                    tasks.append('echo "127.0.1.1 ' + af_nodes[i].hostname + '" >> /etc/hosts')
                    cmd += hstn
                    tasks += hstn
                cmd.append('\n\n# настройка роли узла(ов)')
                cmd.append("# Важно! пароль должен совпадать. Если запустили с неправильным то нужно удалять и добавлять по новой \"inventory node del <name> force\"")
                cmd.append("# Узлов с ролью clickhouse должно быть четное число!")

                # добавляем узлы в кластер с base по worker (читаем массив clstr с конца)
                k = len(clstr)
                while k != 0:
                    k -= 1
                    cmd.append(clstr[k])
                    tasks.append(clstr[k])
                cmd.append('wsc -c "inventory check"')
                cmd.append('wsc -c "inventory node list"')
                cmd.append('\n\n# установка инфраструктуры')
                if (len(ntp_str) != 0):
                    cmd.append('/var/pt/infra/current/install.sh')
                else:
                    cmd.append('# NTP НЕ УКАЗАН! (для продуктива рекомендуется указать)')
                    cmd.append('/var/pt/infra/current/install.sh --without-ntp')
                cmd.append('# установка Grafana')
                cmd.append('/var/pt/infra/current/install.sh --action=add_monitoring')
                #cmd.append('wsc -c "config commit"')
                cmd.append('# установка AF')
                cmd.append('/var/pt/ptaf-deploy/current/install.sh')

                cmd.append('#\n#\n# если установка завершилась без ошибок, то будет failed = 0')
                cmd.append('# подключаемся в UI под login/password - admin/positive и запрашиваем лицензию')
                cmd.append('# https://' + df.iloc[32]['node1'])
                cmd.append('# Grafana доступна по ссылке ниже, login/password - admin/admin')
                cmd.append('# https://' + df.iloc[32]['node1'] + ":3000")

        playbook_path = 'playbook.yaml'
        with open(playbook_path, 'r', encoding='utf-8') as f:
            playbook = yaml.safe_load(f) or []
        all_commands = []        
        all_commands.append('rm /opt/ptaf/conf/wsc/config.sqlite3 2>/dev/null || true') # Удаляем базу wsc на каждой ноде
        filtered_commands = [task for task in tasks if not task.strip().startswith("#")]
        all_commands.extend(filtered_commands)

        directives = [
        {"name": f"Run command: {command}",
         "shell": command}
        for command in all_commands
        ]
        # Формируем структуру плейбука
        playb = {
            "name": f"Execute commands on node {af_nodes[i].hostname}" ,
            "hosts": af_nodes[i].hostname,
            "tasks": directives
        }
        playbook.insert(0, playb)

        # Сохраняем плейбук в YAML-файл
        with open(playbook_path, "w", encoding="utf-8") as f:
            yaml.dump(playbook, f, default_flow_style=False, allow_unicode=True)

        print(f"Таски для ноды {af_nodes[i].hostname} добавлены")        
    return(cmd)

def bonds(bond_name, bond_int1, bond_int2, bond_mode, bond_tag1, bond_tag2, bond_tag3, bond_tag4):
    cmd = []
    
    # Проверяем наличие параметров
    has_int1 = bond_int1 != ""
    has_int2 = bond_int2 != ""
    has_mode = bond_mode != ""
    
    # Если все три параметра отсутствуют - это норма
    if not has_int1 and not has_int2 and not has_mode:
        return cmd  # возвращаем пустой список
    
    # хотя бы один параметр, но не  три - кривой бонд
    if not (has_int1 and has_int2 and has_mode):
        missing = []
        if not has_int1: missing.append("bond_int1")
        if not has_int2: missing.append("bond_int2")
        if not has_mode: missing.append("bond_mode")
        print(f"ОШИБКА: Для бонда {bond_name} не хватает параметров: {', '.join(missing)}")
        return cmd
    
    # Если все три параметра есть - настраиваем бонд
    cmd.append(f'# настройка бонда {bond_name}')
    cmd.append(f'wsc -c "if bond {bond_name[-1]} {bond_int1} {bond_int2}"')
    cmd.append(f'wsc -c "if set {bond_name} slaves {bond_int1} {bond_int2}"')
    cmd.append(f'wsc -c "if set {bond_name} mode {bond_mode}"')
    
    if (bond_tag1 != "") or (bond_tag2 != "") or (bond_tag3 != "") or (bond_tag4 != ""):
        cmd.append(f'wsc -c "if vlan {bond_name} {bond_tag1} {bond_tag2} {bond_tag3} {bond_tag4}"')
    
    return cmd


def eth(ip_addr,mask,gw,role,ethN,mode,gwint):
    #
    # настройка интерфейсов и маршрутов
    #

    cmd = []

    if (ip_addr != ""):
        if (mode == "static"):
            cmd.append('# настройка интерфейса ' + role)
            # если роль текущего интерфейса = интерфейсу на который вешаем дефолтный GW
            if(role == gwint):
                #commands.append('ip addr flush dev ' + ethN)
                if (ip_addr != ""):
                    if (gw != ""):
                        cmd.append('wsc -c "dhcp set routers false"')
                    cmd.append('wsc -c "if set ' + ethN + ' inet_method static inet_address ' + ip_addr + " inet_netmask " + mask + " inet_gateway " + gw + '"')
                if (role == "WAN" or role == "LAN"):
                    cmd.append('wsc -c "if set ' + ethN + ' role ' + gwint +'"')
            else:
                cmd.append('wsc -c "if set ' + ethN + ' inet_method static inet_address ' + ip_addr + " inet_netmask " + mask + '"')
                if (role == "WAN" or role == "CLUSTER" or role == "LAN"):
                    cmd.append('wsc -c "if set ' + ethN + ' role ' + role + '"')
                # если есть gw для LAN (для CLUSTER маршрут не добавляем, это должна быть изолировання подсеть)
                if (gw != "" and role != "CLUSTER"):
                    cmd.append('   # добавляем шлюз через отдельную таблицу для ' + role)
                    # номера таблиц должны отличаться, считаем, что у нас либо LAN, либо CLUSTER таблица
                    table_num = "128"
                    if (role == "LAN"):
                        table_num = "129"
                    cmd.append('wsc -c "route table add ' + ethN + ' ' + table_num + '"')
                    cmd.append('wsc -c "route add default via ' + gw + ' dev '+ ethN + ' table ' + ethN + '"')
                    cmd.append('wsc -c "route rule add '+ ethN + ' from ' + ip_addr + '/32 table ' + ethN  + '"')
                    cmd.append('wsc -c "route rule add '+ ethN + ' to ' + ip_addr + '/32 table ' + ethN  + '"')
                    addr = ipcalc.IP(ip=str(ip_addr), mask=str(mask))
                    cmd.append('wsc -c "route add ' + str(addr.guess_network()) + ' dev '+ ethN + ' src ' + ip_addr + ' table ' + ethN  + '"')
        else:
            print("Error: режим dhcp, но почему-то задан IP")
            exit(1)
    else:
        if (mode == "dhcp"):
            cmd.append('# настройка интерфейса ' + role)
            if (role == "WAN"):
                cmd.append('wsc -c "if set ' + ethN + ' role WAN"')
            elif (role == "CLUSTER"):
                cmd.append('wsc -c "if set ' + ethN + ' role CLUSTER"')
            return(cmd)
    #cmd.append('#')
    return(cmd)

def generate_inventory(af_nodes, output_file="inventory.yaml"):
    """
    Генерирует файл inventory.yaml из списка узлов af_nodes.
    
    :param af_nodes: Список объектов узлов, содержащих атрибуты:
                     - hostname (имя узла)
                     - ethX_role (роль интерфейса)
                     - ethX_ip (IP-адрес интерфейса)
                     - ssh_password (пароль для SSH)
    :param output_file: Имя выходного файла для сохранения inventory (по умолчанию "inventory.yaml").
    """
    # Проверяем, что список узлов не пуст
    if not af_nodes:
        raise ValueError("Список узлов af_nodes пуст!")

    # Вспомогательная функция для нахождения IP интерфейса с ролью "CLUSTER"
    def get_cluster_ip(node):
        for i in range(4):
            role_key = f"eth{i}_role"
            ip_key = f"eth{i}_ip"

            role_value = getattr(node, role_key, None)  # Роль интерфейса
            ip_value = getattr(node, ip_key, None)      # IP интерфейса

            if role_value == "CLUSTER" and ip_value:
                return ip_value
        return None

    # Фильтрация узлов с валидными параметрами
    def valid_node(node):
        return all([
            getattr(node, "hostname", None),
            get_cluster_ip(node),  # Проверяем наличие IP для интерфейса с ролью "CLUSTER"
            getattr(node, "ssh_password", None)
        ])

    # Разделение узлов на группы
    group1 = [node for node in af_nodes[1:] if valid_node(node)]  # Все узлы кроме первого
    group2 = [node for node in af_nodes[:1] if valid_node(node)]  # Только первый узел

    # Формируем структуру inventory
    inventory = {
        "all": {
            "children": {
                "group1": {
                    "host_key_checking": "false",
                    "hosts": {
                        node.hostname: {
                            "ansible_host": get_cluster_ip(node),
                            "ansible_user": "pt",
                            "ansible_ssh_pass": node.ssh_password,
                            "ansible_port": 22013,
                        }
                        for node in group1
                    },
                    "vars": {
                        "ansible_become" : 'true',
                        "ansible_become_method" : "sudo",
                        "ansible_become_pass": "{{ ansible_ssh_pass }}",
                        "ansible_ssh_common_args": '-o StrictHostKeyChecking=no'
                    },
                },
                "group2": {
                    "hosts": {
                        node.hostname: {
                            "ansible_connection": "local"
                        }
                        for node in group2                        
                    }
                },
            },
        },
    }

    # Сохраняем структуру в YAML-файл
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(inventory, f, default_flow_style=False, allow_unicode=True)

    print(f"Файл {output_file} создан успешно!")
def generate_commands_playbook(output_file="playbook.yaml", *functions):
    """
    Выполняет переданные функции, собирает команды из них (игнорирует комментарии) и создает Ansible плейбук.

    :param output_file: Имя выходного файла для плейбука (по умолчанию "playbook.yaml").
    :param functions: Функции, возвращающие списки команд.
    """
    # Список для всех команд
    all_commands = []
    # Вызываем каждую функцию и добавляем её команды в общий список
    for func in functions:
        commands = func()
        if not isinstance(commands, list):
            raise ValueError(f"Функция {func.__name__} должна возвращать список!")
        # Исключаем комментарии, начинающиеся с #
        filtered_commands = [cmd for cmd in commands if not cmd.strip().startswith("#")]
        all_commands.extend(filtered_commands)

    # Проверяем, что список команд не пуст
    if not all_commands:
        raise ValueError("Ни одна из функций не вернула команды!")

    # Формируем задачи для плейбука
    directives = [
        {"name": f"Run command: {command}",
         "shell": command}
        for command in all_commands
    ]
    directives.append({"name": "Commit configuration changes",
         "shell": 'wsc -c "config commit"'})
    # Формируем структуру плейбука
    playbook = [{
        "name": "Execute commands on nodes",
        "hosts": "all",
        "tasks": directives
    }]

    # Сохраняем плейбук в YAML-файл
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(playbook, f, default_flow_style=False, allow_unicode=True)

    print(f"Файл {output_file} создан успешно!")
def generate_commands_playbook_check(af_nodes):
    playbook_path = 'playbook.yaml'

    # Загрузка существующего плейбука или создание нового
    with open(playbook_path, 'r', encoding='utf-8') as f:
        playbook = yaml.safe_load(f) or []

    # Команды для добавления в плейбук
    directives = [
        {
            "name": "Run command: wsc -c 'inventory check'",
            "shell": 'wsc -c "inventory check"',
            "register": "result"
        },
        {
            "name": "Show status inventory check",
            "debug": {
                "var": "result"
            }
        },
        {
            "name": "Run command: wsc -c 'inventory node list'",
            "shell": 'wsc -c "inventory node list"',
            "register": "result"
        },
        {
            "name": "Show status inventory node list",
            "debug": {
                "var": "result"
            }
        }
    ]

    # Формируем структуру нового плейбука
    playb = {
        "name": f"Check inventory and node list on {af_nodes[0].hostname}",
        "hosts": af_nodes[0].hostname,
        "tasks": directives
    }
    playbook.append(playb)

    # Сохраняем плейбук в YAML-файл
    with open(playbook_path, "w", encoding="utf-8") as f:
        yaml.dump(playbook, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"Проверки для ноды {af_nodes[0].hostname} добавлены")    
def main():
    # читаем параметры
    parser = argparse.ArgumentParser(prog="conf.py", prefix_chars="-", description="Конфигуратор конфигов для AF4", usage="conf.py -e ""AF4_conf.xlsx"" -s ""Sheet1""")
    parser.add_argument("-e", "--excel", help="Excel file name", type=str, default="AF4_conf.xlsx", required=False)
    parser.add_argument("-s", "--sheet", help="Excel Sheet name", type=str, default="Sheet1", required=False)
    args = parser.parse_args()

    # загружаем Excel-файл
    df = read_excel(args.excel, args.sheet)

    # заменить NaN на ""
    df = df.fillna("")
    # получить узлы
    get_af_nodes(df)

    # print(af_nodes[3].__dict__)

    generate_inventory(af_nodes)
    generate_commands_playbook("playbook.yaml",
                           lambda: vip(df),
                           lambda: ntp(df),
                           lambda: dns(df),
                           lambda: timezone(df))
        
    cmd = []
    cmd += create_config(df)
    generate_commands_playbook_check(af_nodes)
    
    # получить имя excel-файла
    from pathlib import Path
    filename = Path(args.excel).stem
    # распечатать команды
    with open(filename + ".txt", "w", encoding="utf-8", newline='\n') as txt_file:
        for line in cmd:
            txt_file.write(line + "\n")

    readme = f'''
Команды для ручной установки можно посмотреть в файлике {filename}.txt
Для автоматической установки: 
    1. Назначить адреса на кластерных интерфейсах нод типа такого: ifconfig <interface_name> up; ip a add <IP>/<netmask> dev <interface_name>
    2. Файлики inventory.yaml и playbook.yaml положить на первую базовую ноду
    3. Активировать виртуальную среду: source /opt/ptaf/pywsc/bin/activate 
    4. Проверить, что все узлы доступны по кластерным интерфейсам: ansible all -i ./inventory.yaml -m ping
    5. Запустить ансибл: ansible-playbook -i inventory.yaml playbook.yaml
    6. Если ансибл упал на этапе config commit, то можно попробовать ещё раз: ansible-playbook -i inventory.yaml playbook.yaml --start-at-task "Commit configuration changes"
    7. Деактивируем виртуальную среду: deactivate
    8. Profit!
Дальше запустить инфру, мониторинг и деплой:
    /var/pt/infra/current/install.sh
    /var/pt/infra/current/install.sh --action=add_monitoring
    /var/pt/ptaf-deploy/current/install.sh

Если установка завершилась без ошибок, то будет failed = 0
Подключаемся в UI под login/password - admin/positive и запрашиваем лицензию
    https://{df.iloc[32]['node1']}
Grafana доступна по ссылке ниже, login/password - admin/admin
    https://{df.iloc[32]['node1']}:3000
'''
    with open('readme.txt', 'w', encoding='utf-8') as file:
        file.write(readme)
    print(readme)
    # for x in cmd:
    #     print(x)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Произошла ошибка:", e)
        print("\nТрассировка ошибки:")
        traceback.print_exc()  # Выводит полную трассировку
    finally:
        input("Нажмите Enter для выхода...")
    
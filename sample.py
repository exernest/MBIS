import json
import pathlib
import time

from asst.asst import Asst
from asst.utils import Message, Version, InstanceOptionType
from asst.updater import Updater
from asst.emulator import Bluestacks

@Asst.CallBackType
def my_callback(msg, details, arg):
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))

    print(m, d, arg)


if __name__ == "__main__":

    # 请设置为存放 dll 文件及资源的路径
    path = pathlib.Path(__file__).parent.parent

    # 设置更新器的路径和目标版本并更新
    #Updater(path, Version.Stable).update()

    # 外服需要再额外传入增量资源路径，例如
    # incremental_path=path / 'resource' / 'global' / 'YoStarEN'
    Asst.load(path=path)

    # 若需要获取详细执行信息，请传入 callback 参数
    # 例如 asst = Asst(callback=my_callback)
    asst = Asst()

    # 设置额外配置
    # 触控方案配置
    asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
    # 暂停下干员
    # asst.set_instance_option(InstanceOptionType.deployment_with_pause, '1')

    # 启动模拟器。例如启动蓝叠模拟器的多开Pie64_1，并等待30s
    # Bluestacks.launch_emulator_win(r'C:\Program Files\BlueStacks_nxt\HD-Player.exe', 1, "Nougat64_4")

    # 获取Hyper-v蓝叠的adb port
    # port = Bluestacks.get_hyperv_port(r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf", "Pie64_1")

    # 请自行配置 adb 环境变量，或修改为 adb 可执行程序的路径
    if asst.connect(r'adb.exe', '1.1.1.1:5555'):
        print('连接成功')
    else:
        print('连接失败')
        exit()

    # 任务及参数请参考 docs/集成文档.md

    asst.append_task('StartUp', {
    "enable": True,
    "client_type": "Official",
    "start_game_enabled": True
})

    asst.append_task('Infrast', {
    "enable": True,
    "mode": 10000,
    "facility": [
        'Mfg',
        'Trade',
        'Power',
        'Control',
        'Reception',
        'Office',
        'Dorm',
    ],
    "threshold": 0,
    "replenish": False,
    "dorm_notstationed_enabled": False,
    "dorm_trust_enabled": False,
    "filename": r'153基建 Alpha v0.3.X 校正版v3.json',
    "plan_index": 2,
})

    asst.append_task('Mall', {
    "enable": True,
    "shopping": True,
    "buy_first": [
        '招聘许可',
        '龙门币',
    ],
    "blacklist": [
        '碳',
        '家具',
        '加急许可',
    ],
   "force_shopping_if_credit_full": True
})

    asst.append_task('Award', {
    "enable": True
})

    asst.append_task('Fight', {
    "enable": True,
    "stage": "CW-10",
    "medicine": 999,
    "expiring_medicine": 999,
    "stone": 999,
    "report_to_penguin": True,
    "penguin_id": "",
    "server": "CN",
    "client_type": "Official",
    "DrGrandet": False,
})

    #asst.append_task('Custom', {"task_names": ["StartUpConnectingFlag"]})
    asst.start()

    while asst.running():
        time.sleep(0)

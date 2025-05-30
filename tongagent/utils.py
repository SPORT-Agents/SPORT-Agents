import string
import shortuuid
import os
from typing import Union

from omegaconf import OmegaConf, DictConfig, ListConfig

CACHE_FOLDER = ".cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

def get_uuid_builder() -> shortuuid.ShortUUID:
    alphabet = string.ascii_lowercase + string.digits
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su

def load_config() -> Union[DictConfig, ListConfig]:
    if "AGENT_CONFIG" in os.environ and len(os.environ["AGENT_CONFIG"]) > 0:
        return OmegaConf.load(os.environ["AGENT_CONFIG"])
    
    if "RUN_MODE" in os.environ and os.environ["RUN_MODE"] == "eval":
        return OmegaConf.load("configs/agent_config.yaml")
    
    return OmegaConf.load("configs/agent_config_qwen.yaml")
    # return OmegaConf.load("configs/agent_config_zhi.yaml")

import time
uuid_builder = get_uuid_builder()

def gen_random_id():
    return f"{int(time.time()*1000)}_{uuid_builder.random(length=8)}"    

import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
if __name__ == '__main__':
    log = Logger('.cache/1734937977506_7pnsve84/dpo_agent.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')

# if __name__ == "__main__":
    # print(load_config())
    # print(load_config().search_engine[0].cx)
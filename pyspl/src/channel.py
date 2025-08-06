from .libpsi import Channel as _Channel
import logging

class Channel:
    def __init__(self, role, taskid, chl_type="grpc", party="localhost:50051", redis="localhost:6379", 
                 connect_wait_time=60000, use_redis=True, net_log_switch=False, meta={}):
        """
        初始化Channel通信对象
        
        Args:
            role: 角色 (0: sender, 1: receiver)
            taskid: 任务ID
            chl_type: 通信类型 ("grpc" 或 "mem")
            party: 对方地址
            redis: Redis地址
            connect_wait_time: 连接等待时间(毫秒)
            use_redis: 是否使用Redis
            net_log_switch: 是否开启网络日志
            meta: 元数据字典
        """
        self.role = role
        self.taskid = taskid
        self.chl_type = chl_type
        self.party = party
        self.redis = redis
        self.connect_wait_time = connect_wait_time
        self.use_redis = use_redis
        self.net_log_switch = net_log_switch
        self.meta = meta
        
        logging.info(f"Initializing Channel: role={role}, taskid={taskid}, party={party}")
        
        # 创建底层C++对象
        self._channel = _Channel(role, taskid, chl_type, party, redis, 
                                connect_wait_time, use_redis, net_log_switch, meta)
    
    def send(self, message: str) -> bool:
        """
        发送消息
        
        Args:
            message: 要发送的消息字符串
            
        Returns:
            bool: 发送是否成功
        """
        logging.info(f"Sending message: {len(message)} bytes")
        return self._channel.send(message)
    
    def recv(self) -> str:
        """
        接收消息
        
        Returns:
            str: 接收到的消息字符串
        """
        message = self._channel.recv()
        logging.info(f"Received message: {len(message)} bytes")
        return message
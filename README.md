# 医疗系统后端服务器

这是一个基于Python的医疗系统后端服务器，提供JSON API接口用于处理医疗系统的各种业务逻辑。

## 项目结构

```
json-server/
├── server.py                    # 主启动脚本
├── integrated_server.py         # 原始单文件版本（已重构）
├── core/                        # 核心服务
│   ├── __init__.py
│   └── medical_server.py        # 主服务器类
├── models/                      # 数据模型
│   ├── __init__.py
│   └── database.py              # 数据库管理器
├── services/                    # 业务服务
│   ├── __init__.py
│   ├── auth_service.py          # 用户认证服务
│   └── appointment_service.py   # 预约管理服务
├── network/                     # 网络通信
│   ├── __init__.py
│   └── communication.py         # 网络处理器
├── utils/                       # 工具类
│   ├── __init__.py
│   └── server_manager.py        # 服务器管理器
└── README.md                    # 项目说明
```

## 功能特性

### 用户管理
- 患者注册和登录
- 医生注册和登录
- 密码重置
- 用户信息更新

### 预约管理
- 创建预约/挂号
- 查询预约信息
- 取消预约
- 更新预约状态

### 数据库支持
- SQLite数据库
- 完整的医疗系统表结构
- 外键约束
- 示例数据

### 网络通信
- TCP Socket通信
- JSON协议
- 多线程处理
- 连接延迟优化（服务器端1秒，客户端0.1秒）
- 错误处理

### 服务器管理
- 守护进程模式
- PID文件管理
- 信号处理
- 日志记录

## 使用方法

### 启动服务器

```bash
# 前台运行
python server.py start --foreground

# 后台运行（守护进程）
python3 server.py start

# 指定配置参数
python server.py start --host 0.0.0.0 --port 55000 --db-path /medical/MedicalSystem.db
```

### 停止服务器

```bash
python3 server.py stop
```

### 重启服务器

```bash
python3 server.py restart
```

### 查看服务器状态

```bash
python server.py status
```

### 命令行参数

- `--host`: 监听地址（默认: 0.0.0.0）
- `--port`: 监听端口（默认: 55000）
- `--db-path`: 数据库文件路径（默认: /medical/MedicalSystem.db）
- `--log-file`: 日志文件路径（默认: /medical/server.log）
- `--pid-file`: PID文件路径（默认: /medical/server.pid）
- `--daemon`: 以守护进程模式运行
- `--foreground`: 前台运行

## API接口

服务器接受JSON格式的请求，支持以下操作：

### 用户认证
- `login`: 用户登录验证
- `register_patient`: 患者注册
- `register_doctor`: 医生注册
- `reset_password`: 密码重置
- `reset_patient_information`: 更新患者信息
- `reset_doctor_information`: 更新医生信息
- `query_doctor_info`: 查询医生信息
- `query_patient_info`: 查询患者信息

### 预约管理
- `create_appointment`: 创建预约
- `query_appointments`: 查询预约
- `cancel_appointment`: 取消预约
- `update_appointment_status`: 更新预约状态

### 数据库操作
- `sql_query`: 执行SQL查询
- 默认插入操作（指定table_name）

## 数据库表结构

### 主要表
- `users`: 用户表（患者和医生）
- `patients`: 患者详细信息
- `doctors`: 医生详细信息
- `appointments`: 预约挂号
- `medical_records`: 病历记录
- `medical_orders`: 医嘱
- `prescriptions`: 处方
- `attendance`: 打卡记录
- `chat_messages`: 聊天记录
- `leave_requests`: 请假申请
- `hospitalizations`: 住院信息

### 测试表
- `students`: 学生表（兼容性）
- `default_table`: 默认表

## 开发说明

### 模块说明

1. **core/medical_server.py**: 主服务器类，整合所有服务
2. **models/database.py**: 数据库管理，表结构定义
3. **services/auth_service.py**: 用户认证相关业务逻辑
4. **services/appointment_service.py**: 预约管理相关业务逻辑
5. **network/communication.py**: 网络通信处理
6. **utils/server_manager.py**: 服务器进程管理

### 扩展开发

要添加新的功能：

1. 在`services/`目录下创建新的服务类
2. 在`core/medical_server.py`中注册新服务
3. 在`process_json_data`方法中添加新的请求处理逻辑

### 日志和调试

- 日志文件默认位置：`/medical/server.log`
- 日志级别：INFO
- 包含时间戳、级别和消息内容

## 注意事项

1. 确保有足够的权限创建`/medical/`目录
2. 数据库文件会自动创建
3. 守护进程模式下不会有控制台输出
4. 使用SIGTERM信号可以优雅关闭服务器

## 许可证

请参考LICENSE文件。

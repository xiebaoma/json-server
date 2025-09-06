# JSON数据库服务器

这是一个整合的JSON数据库服务器程序，能够接收客户端的JSON请求，处理数据库操作，并返回JSON格式的结果。

## 功能特性

- **网络通信**: 基于TCP Socket的客户端-服务器通信
- **JSON处理**: 自动解析JSON数据并根据内容执行相应操作
- **数据库操作**: 支持SQLite数据库的增删改查操作
- **多线程支持**: 每个客户端连接使用独立线程处理
- **完整日志**: 详细的操作日志记录
- **错误处理**: 完善的异常处理和错误响应机制
- **守护进程**: 支持后台守护进程模式运行
- **进程管理**: 完整的启动/停止/重启/状态查看功能
- **信号处理**: 优雅的关闭和重启机制
- **PID管理**: 防止重复启动，支持进程监控

## 文件说明

### 核心文件

- `integrated_server.py` - 整合的服务端程序（支持守护进程模式）
- `test_client.py` - 测试客户端程序
- `check_database.py` - 数据库查看和管理工具
- `server_control.sh` - 服务器控制脚本（便于管理）
- `json-db-server.service` - systemd服务配置文件

### 原始文件（已整合）

- `execute_json.py` - JSON处理和数据库操作功能
- `recv_json.py` - 网络接收功能
- `send_json.py` - 网络发送功能

## 支持的操作类型

### 1. 用户密码重置
```json
{
    "reset_password": true,
    "user_name": "13800138000",  // 手机号或工号
    "new_password": "new_password_hash"
}
```

### 2. 患者信息更新
```json
{
    "reset_patient_information": true,
    "old_phone": "13800138000",
    "new_name": "新姓名",
    "new_birth_date": "1990-01-01",
    "new_id_card": "新身份证号",
    "new_phone": "新手机号",
    "new_email": "new@example.com"
}
```

### 3. 医生信息更新
```json
{
    "reset_doctor_information": true,
    "old_employee_id": "DOC001",
    "new_name": "医生姓名",
    "new_employee_id": "新工号",
    "new_department": "科室",
    "new_max_patients": 40,
    "new_fee": 80.0,
    "new_work_schedule": "{\"monday\": \"9:00-17:00\"}",
    "new_is_available": true,
    "new_photo_path": "/path/to/photo.jpg"
}
```

### 4. SQL查询执行
```json
{
    "sql_query": "SELECT p.name, p.phone, d.name as doctor_name FROM patients p JOIN appointments a ON p.patient_id = a.patient_id JOIN doctors d ON a.doctor_id = d.doctor_id"
}
```

#### 常用查询示例：

**查询所有用户信息：**
```json
{
    "sql_query": "SELECT user_id, username, role, created_at FROM users"
}
```

**查询患者详细信息：**
```json
{
    "sql_query": "SELECT p.name, p.phone, p.email, u.username FROM patients p JOIN users u ON p.patient_id = u.user_id"
}
```

**查询医生及其预约情况：**
```json
{
    "sql_query": "SELECT d.name, d.department, COUNT(a.appointment_id) as appointment_count FROM doctors d LEFT JOIN appointments a ON d.doctor_id = a.doctor_id GROUP BY d.doctor_id"
}
```

**查询病历信息：**
```json
{
    "sql_query": "SELECT p.name as patient_name, d.name as doctor_name, m.diagnosis, m.visit_time FROM medical_records m JOIN patients p ON m.patient_id = p.patient_id JOIN doctors d ON m.doctor_id = d.doctor_id"
}
```

### 5. 数据插入
```json
{
    "table_name": "students",
    "name": "张三",
    "age": 20,
    "student_id": 12345
}
```

## 使用方法

### 启动服务器

现在服务器支持多种启动方式：

#### 1. 后台守护进程模式（推荐）

```bash
# 启动服务器
python integrated_server.py start

# 查看服务器状态
python integrated_server.py status

# 停止服务器
python integrated_server.py stop

# 重启服务器
python integrated_server.py restart
```

#### 2. 前台调试模式

```bash
# 前台启动（用于调试，按Ctrl+C停止）
python integrated_server.py start --foreground
```

#### 3. 使用控制脚本（更方便）

```bash
# 使脚本可执行
chmod +x server_control.sh

# 启动服务器
./server_control.sh start

# 查看状态
./server_control.sh status

# 查看实时日志
./server_control.sh logs

# 前台启动
./server_control.sh foreground

# 停止服务器
./server_control.sh stop
```

#### 4. 自定义配置启动

```bash
# 指定自定义配置
python integrated_server.py start --host 127.0.0.1 --port 8080 --db-path ./my.db --log-file ./my.log
```

服务器默认在 `0.0.0.0:55000` 上启动并等待客户端连接。

### 运行测试客户端

```bash
python test_client.py
```

测试客户端将执行各种类型的操作测试。

### 服务器响应格式

#### 成功响应
```json
{
    "status": "success",
    "timestamp": "2024-01-01T12:00:00",
    "result": "操作结果"
}
```

#### 错误响应
```json
{
    "status": "error",
    "timestamp": "2024-01-01T12:00:00",
    "error": "错误信息"
}
```

## 工作流程

1. **接收连接**: 服务器监听端口，接受客户端连接
2. **接收JSON数据**: 按照协议接收客户端发送的JSON数据
3. **数据处理**: 根据JSON内容判断操作类型并执行相应的数据库操作
4. **返回结果**: 将处理结果封装为JSON格式返回给客户端
5. **循环处理**: 服务器持续运行，处理多个客户端请求

## 网络协议

### 客户端发送格式
1. 文件名长度 (4字节, 大端序)
2. 文件名 (UTF-8编码)
3. 文件大小 (4字节, 大端序)
4. JSON内容 (UTF-8编码)

### 服务端响应格式
1. 响应长度 (4字节, 大端序)
2. JSON响应内容 (UTF-8编码)

## 日志记录和监控

### 日志文件

服务器默认将日志记录到 `/medical/server.log`：

```bash
# 查看实时日志
tail -f /medical/server.log

# 或使用控制脚本
./server_control.sh logs
```

### 日志内容

日志包含：
- 服务器启动/停止信息
- 客户端连接信息
- 请求和响应内容
- 数据库操作记录
- 错误信息和堆栈跟踪
- 操作时间戳

### 进程监控

```bash
# 查看服务器状态
python integrated_server.py status

# 查看进程信息
ps aux | grep integrated_server

# 查看端口使用情况
netstat -tulpn | grep :55000

# 或使用ss命令
ss -tulpn | grep :55000
```

### 系统服务模式（Linux）

在Linux系统上可以作为系统服务运行：

```bash
# 复制服务文件
sudo cp json-db-server.service /etc/systemd/system/

# 重新加载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start json-db-server

# 设置开机自启
sudo systemctl enable json-db-server

# 查看服务状态
sudo systemctl status json-db-server

# 查看服务日志
sudo journalctl -u json-db-server -f
```

## 数据库要求

服务器使用SQLite数据库，默认文件名为 `database.db`。

**⚠️ 数据库自动初始化**: 服务器启动时会自动创建所需的数据库表和示例数据，无需手动创建！

## 医疗系统完整表结构：

### 核心用户表
- `users` 表: user_id, username, password_hash, role, created_at

### 医疗人员信息表
- `patients` 表: patient_id, name, birth_date, id_card, phone, email, created_at
- `doctors` 表: doctor_id, name, employee_id, department, photo_path, max_patients, fee, work_schedule, is_available

### 医疗业务表
- `appointments` 表: appointment_id, patient_id, doctor_id, appointment_time, status, fee_paid, queue_number, created_at
- `medical_records` 表: record_id, patient_id, doctor_id, diagnosis, symptoms, visit_time, created_at
- `medical_orders` 表: order_id, record_id, doctor_id, content, created_at
- `prescriptions` 表: prescription_id, record_id, doctor_id, content, created_at
- `hospitalizations` 表: hospitalization_id, patient_id, doctor_id, ward_number, bed_number, admission_date, discharge_date, status, created_at, updated_at

### 管理功能表
- `attendance` 表: attendance_id, doctor_id, check_in_time, check_out_time, status
- `leave_requests` 表: leave_id, doctor_id, start_date, end_date, reason, status, created_at
- `chat_messages` 表: message_id, sender_id, receiver_id, content, sent_at, is_read

### 测试用表
- `students` 表: id, name, age, student_id, created_at（用于测试）
- `default_table` 表: id, data, created_at（通用插入测试）

### 数据库特性
- ✅ **外键约束**: 确保数据完整性
- ✅ **角色管理**: 患者和医生角色区分
- ✅ **完整的医疗业务流程**: 预约→就诊→病历→处方
- ✅ **医生管理**: 打卡、请假、排班管理
- ✅ **住院管理**: 病房、床位管理
- ✅ **即时通讯**: 医患沟通功能

### 数据库管理工具

使用 `check_database.py` 查看和管理数据库：

```bash
# 查看数据库内容和状态
python check_database.py

# 查看并测试数据库操作
python check_database.py --test

# 重置数据库（删除所有表）
python check_database.py --reset

# 查看指定数据库文件
python check_database.py /path/to/your/database.db
```

## 注意事项

### 基本配置
1. **数据库自动初始化**: 首次启动服务器时会自动创建数据库和所有必要的表
2. **网络安全**: 服务器默认监听所有网卡 (0.0.0.0)，生产环境请注意防火墙设置
3. **SQL安全**: 使用参数化查询防止SQL注入攻击
4. **并发支持**: 服务器支持多客户端并发连接
5. **事务处理**: 所有数据库操作都有完整的事务和异常处理

### 文件权限和目录
6. **目录权限**: 确保 `/medical/` 目录存在且有写入权限
7. **日志文件**: 日志文件路径需要有写入权限
8. **PID文件**: PID文件路径需要有写入权限

### 故障排除
9. **重置数据库**: 如果遇到数据库相关错误，可以使用 `check_database.py --reset` 重置数据库
10. **端口占用**: 如果启动失败，检查端口是否被占用：`lsof -i :55000`
11. **进程清理**: 如果服务异常退出，可能需要手动删除PID文件：`rm /medical/server.pid`

### 后台运行注意事项
12. **守护进程**: 后台模式下服务器会自动转为守护进程，脱离终端运行
13. **日志输出**: 后台模式下所有输出都会重定向到日志文件
14. **信号处理**: 支持 SIGTERM、SIGINT、SIGQUIT 信号优雅关闭
15. **自动重启**: 服务异常退出时，可配置systemd自动重启

### 性能和资源
16. **内存使用**: 每个客户端连接会创建一个线程，注意监控内存使用
17. **数据库锁**: SQLite在高并发时可能出现锁等待，生产环境建议使用PostgreSQL
18. **文件句柄**: 大量并发连接时注意系统文件句柄限制

## 开发和调试

- 修改 `JSONDatabaseServer` 类的构造参数可以改变监听地址、端口和数据库路径
- 日志级别可以通过修改 `setup_logging()` 方法调整
- 添加新的操作类型需要在 `process_json_data()` 方法中添加相应判断逻辑

## 示例使用

启动服务器后，可以使用任何支持TCP Socket的客户端发送JSON数据进行测试，或者使用提供的 `test_client.py` 进行功能验证。

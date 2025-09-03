# 医疗系统API - JSON格式参考卡片

## 服务器信息
```
地址: 8.140.225.6:55000
协议: TCP Socket + JSON
编码: UTF-8
```

## 🔐 用户认证

### 登录
```json
请求: {
  "login": true,
  "user_name": "13800138000",
  "password": "hash_patient1"
}

响应: {
  "status": "success",
  "result": "verificationSuccess"
}
```

### 患者注册
```json
请求: {
  "register_patient": true,
  "name": "张三",
  "password_hash": "hashed_password",
  "phone": "13800138000",
  "birth_date": "1990-01-01",
  "id_card": "110101199001010001",
  "email": "zhangsan@example.com"
}

响应: {
  "status": "success",
  "result": "chenggongcharu"
}
```

### 医生注册
```json
请求: {
  "register_doctor": true,
  "name": "王医生",
  "password_hash": "hashed_password",
  "employee_id": "DOC001",
  "department": "内科",
  "photo_path": "/path/to/photo.jpg"
}

响应: {
  "status": "success",
  "result": "chenggongcharu"
}
```

## 👤 信息查询

### 查询医生信息
```json
请求: {
  "query_doctor_info": true,
  "doctor_name": "王医生"
}

响应: {
  "status": "success",
  "result": {
    "status": "success",
    "doctor_info": {
      "doctor_id": 1,
      "name": "王医生",
      "department": "内科",
      "fee": 50.0,
      "is_available": true
    }
  }
}
```

### 查询患者信息
```json
请求: {
  "query_patient_info": true,
  "patient_name": "张三"
}

响应: {
  "status": "success",
  "result": {
    "status": "success",
    "patient_info": {
      "patient_id": 1,
      "name": "张三",
      "phone": "13800138000",
      "birth_date": "1990-01-01"
    }
  }
}
```

## 📅 预约管理

### 创建预约
```json
请求: {
  "create_appointment": true,
  "patient_phone": "13800138000",
  "doctor_name": "王医生",
  "appointment_time": "2024-03-01 10:00:00",
  "fee_paid": 1
}

响应: {
  "status": "success",
  "result": {
    "status": "success",
    "appointment_info": {
      "appointment_id": 123,
      "queue_number": 5,
      "status": "pending"
    }
  }
}
```

### 查询预约 (多种方式)
```json
// 按患者手机号
请求: {
  "query_appointments": true,
  "patient_phone": "13800138000"
}

// 按医生姓名
请求: {
  "query_appointments": true,
  "doctor_name": "王医生"
}

// 按日期
请求: {
  "query_appointments": true,
  "appointment_date": "2024-03-01"
}

// 查询所有 (最近20条)
请求: {
  "query_appointments": true
}

响应: {
  "status": "success",
  "result": {
    "status": "success",
    "appointments": [
      {
        "appointment_id": 1,
        "patient_name": "张三",
        "doctor_name": "王医生",
        "appointment_time": "2024-03-01 10:00:00",
        "status": "pending",
        "queue_number": 5
      }
    ]
  }
}
```

### 取消预约
```json
请求: {
  "cancel_appointment": true,
  "appointment_id": 123
}

响应: {
  "status": "success",
  "result": {
    "status": "success",
    "message": "预约ID 123 已成功取消"
  }
}
```

### 更新预约状态
```json
请求: {
  "update_appointment_status": true,
  "appointment_id": 123,
  "new_status": "completed"
}

响应: {
  "status": "success",
  "result": {
    "status": "success",
    "message": "预约状态已更新"
  }
}
```

## 🗄️ 数据库操作

### SQL查询
```json
请求: {
  "sql_query": "SELECT COUNT(*) as total_users FROM users"
}

响应: {
  "status": "success",
  "result": {
    "columns": ["total_users"],
    "data": [[10]]
  }
}
```

### 通用数据插入
```json
请求: {
  "table_name": "students",
  "name": "张三",
  "age": 20,
  "student_id": 12345
}

响应: {
  "status": "success",
  "result": "成功插入数据到表 students"
}
```

## 🔧 信息更新

### 更新患者信息
```json
请求: {
  "reset_patient_information": true,
  "old_phone": "13800138000",
  "new_name": "张三三",
  "new_phone": "13900139000",
  "new_email": "zhangsan_new@example.com"
}

响应: {
  "status": "success",
  "result": "患者信息更新成功"
}
```

### 更新医生信息
```json
请求: {
  "reset_doctor_information": true,
  "old_employee_id": "DOC001",
  "new_name": "王医师",
  "new_department": "心内科",
  "new_fee": 80.0
}

响应: {
  "status": "success",
  "result": "医生信息更新成功"
}
```

### 重置密码
```json
请求: {
  "reset_password": true,
  "username": "13800138000",
  "new_password": "new_hashed_password"
}

响应: {
  "status": "success",
  "result": "密码更新成功"
}
```

## 📋 状态码说明

### 登录状态
- `"verificationSuccess"` - 登录成功
- `"verificationFalse"` - 密码错误
- `"verificationFalse_bucunzai"` - 用户不存在
- `"verificationFalse_yichang"` - 系统异常

### 注册状态
- `"chenggongcharu"` - 注册成功
- `"shoujihaoyicunzai"` - 手机号已存在
- `"gonghaoyicunzai"` - 工号已存在
- `"charuyichang"` - 注册异常

### 预约状态
- `"pending"` - 待处理
- `"completed"` - 已完成
- `"cancelled"` - 已取消

## 💡 前端集成提示

### 1. WebSocket连接 (推荐)
```javascript
const socket = new WebSocket('ws://8.140.225.6:55000');
socket.send(JSON.stringify(requestData));
```

### 2. HTTP模拟 (需要代理)
```javascript
fetch('/api/medical', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(requestData)
})
```

### 3. 错误处理
```javascript
if (response.status === 'success') {
  // 处理成功结果
  console.log(response.result);
} else {
  // 处理错误
  console.error(response.error);
}
```

## 🧪 测试数据

### 预置用户
```json
// 患者
{
  "username": "13800138000",
  "password": "hash_patient1",
  "name": "张三"
}

// 医生
{
  "username": "DOC001", 
  "password": "hash_doctor1",
  "name": "王医生",
  "department": "内科"
}
```

### 测试命令
```bash
# 快速测试
python quick_test.py

# 完整测试
python remote_test.py

# 压力测试
python stress_test.py
```

---
**📞 技术支持**: 参考完整API文档或联系后端团队

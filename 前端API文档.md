# 医疗系统后端API接口文档

## 服务器信息

- **服务器地址**: 8.140.225.6:55000
- **协议**: TCP Socket + JSON
- **编码**: UTF-8

## 通信协议格式

### 请求格式
```
[文件名长度(4字节)] + [文件名] + [数据长度(4字节)] + [JSON数据]
```

### 响应格式
```json
{
  "status": "success" | "error",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "具体响应数据" | { "详细对象数据" },
  "error": "错误信息 (仅在status为error时存在)"
}
```

### 连接管理
- **服务器端延迟**: 响应发送后延迟1秒再关闭连接，确保数据传输完成
- **客户端延迟**: 接收响应后延迟0.1秒再关闭连接，避免连接过早断开
- **连接稳定性**: 延迟机制提高了网络通信的可靠性

## API接口列表

### 1. 用户认证相关

#### 1.1 用户登录
**请求格式**:
```json
{
  "login": true,
  "user_name": "用户名",
  "password": "密码"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "verificationSuccess"
}
```

**可能的result值**:
- `"verificationSuccess"` - 登录成功
- `"verificationFalse"` - 密码错误
- `"verificationFalse_bucunzai"` - 用户不存在
- `"verificationFalse_yichang"` - 系统异常

#### 1.2 患者注册
**请求格式**:
```json
{
  "register_patient": true,
  "name": "患者姓名",
  "password_hash": "密码哈希值",
  "phone": "手机号码",
  "birth_date": "1990-01-01",
  "id_card": "身份证号码",
  "email": "邮箱地址"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "chenggongcharu"
}
```

**可能的result值**:
- `"chenggongcharu"` - 注册成功
- `"shoujihaoyicunzai"` - 手机号已存在
- `"charuyichang"` - 注册异常

#### 1.3 医生注册
**请求格式**:
```json
{
  "register_doctor": true,
  "name": "医生姓名",
  "password_hash": "密码哈希值",
  "employee_id": "工号",
  "department": "科室",
  "photo_path": "头像路径"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "chenggongcharu"
}
```

**可能的result值**:
- `"chenggongcharu"` - 注册成功
- `"gonghaoyicunzai"` - 工号已存在
- `"charuyichang"` - 注册异常

#### 1.4 重置密码
**请求格式**:
```json
{
  "reset_password": true,
  "username": "用户名",
  "new_password": "新密码哈希值"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "用户 13800138000 的密码更新成功"
}
```

### 2. 用户信息管理

#### 2.1 查询医生信息
**请求格式**:
```json
{
  "query_doctor_info": true,
  "doctor_name": "医生姓名"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "status": "success",
    "message": "查询成功",
    "doctor_info": {
      "doctor_id": 1,
      "name": "王医生",
      "employee_id": "DOC001",
      "department": "内科",
      "photo_path": null,
      "max_patients": 30,
      "fee": 50.0,
      "work_schedule": "{\"monday\": \"9:00-17:00\"}",
      "is_available": true,
      "username": "DOC001",
      "role": "doctor",
      "created_at": "2024-01-01 00:00:00"
    }
  }
}
```

#### 2.2 查询患者信息
**请求格式**:
```json
{
  "query_patient_info": true,
  "patient_name": "患者姓名"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "status": "success",
    "message": "查询成功",
    "patient_info": {
      "patient_id": 1,
      "name": "张三",
      "birth_date": "1990-01-01",
      "id_card": "110101199001010001",
      "phone": "13800138000",
      "email": "zhangsan@example.com",
      "patient_created_at": "2024-01-01 00:00:00",
      "username": "13800138000",
      "role": "patient",
      "user_created_at": "2024-01-01 00:00:00"
    }
  }
}
```

#### 2.3 更新患者信息
**请求格式**:
```json
{
  "reset_patient_information": true,
  "old_phone": "原手机号",
  "new_name": "新姓名",
  "new_birth_date": "1990-01-01",
  "new_id_card": "新身份证号",
  "new_phone": "新手机号",
  "new_email": "新邮箱"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "患者ID为 1 的患者信息更新成功"
}
```

#### 2.4 更新医生信息
**请求格式**:
```json
{
  "reset_doctor_information": true,
  "old_employee_id": "原工号",
  "new_name": "新姓名",
  "new_employee_id": "新工号",
  "new_department": "新科室",
  "new_max_patients": 40,
  "new_fee": 80.0,
  "new_work_schedule": "{\"monday\": \"8:00-18:00\"}",
  "new_is_available": true,
  "new_photo_path": "新头像路径"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "医生ID为 1 的医生信息更新成功"
}
```

### 3. 预约管理

#### 3.1 创建预约
**请求格式**:
```json
{
  "create_appointment": true,
  "patient_phone": "患者手机号",
  "doctor_name": "医生姓名",
  "appointment_time": "2024-03-01 10:00:00",
  "fee_paid": 1
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "status": "success",
    "message": "预约创建成功",
    "appointment_info": {
      "appointment_id": 123,
      "patient_phone": "13800138000",
      "doctor_name": "王医生",
      "appointment_time": "2024-03-01 10:00:00",
      "queue_number": 5,
      "status": "pending",
      "fee_paid": true
    }
  }
}
```

#### 3.2 查询预约
**请求格式** (可选择其中一种查询方式):

**按患者手机号查询**:
```json
{
  "query_appointments": true,
  "patient_phone": "13800138000"
}
```

**按医生姓名查询**:
```json
{
  "query_appointments": true,
  "doctor_name": "王医生"
}
```

**按日期查询**:
```json
{
  "query_appointments": true,
  "appointment_date": "2024-03-01"
}
```

**查询所有预约** (返回最近20条):
```json
{
  "query_appointments": true
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "status": "success",
    "message": "查询到 3 条预约记录",
    "appointments": [
      {
        "appointment_id": 1,
        "patient_name": "张三",
        "patient_phone": "13800138000",
        "doctor_name": "王医生",
        "department": "内科",
        "appointment_time": "2024-02-01 09:00:00",
        "status": "completed",
        "fee_paid": true,
        "queue_number": 1,
        "created_at": "2024-01-01 08:00:00"
      }
    ]
  }
}
```

#### 3.3 取消预约
**请求格式**:
```json
{
  "cancel_appointment": true,
  "appointment_id": 123
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "status": "success",
    "message": "预约ID 123 已成功取消"
  }
}
```

#### 3.4 更新预约状态
**请求格式**:
```json
{
  "update_appointment_status": true,
  "appointment_id": 123,
  "new_status": "completed"
}
```

**有效状态值**:
- `"pending"` - 待处理
- `"completed"` - 已完成
- `"cancelled"` - 已取消

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "status": "success",
    "message": "预约ID 123 状态已从 'pending' 更新为 'completed'"
  }
}
```

### 4. 数据库查询

#### 4.1 SQL查询
**请求格式**:
```json
{
  "sql_query": "SELECT COUNT(*) as total_users FROM users"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": {
    "columns": ["total_users"],
    "data": [[10]]
  }
}
```

### 5. 通用数据插入

#### 5.1 插入数据到指定表
**请求格式**:
```json
{
  "table_name": "表名",
  "字段1": "值1",
  "字段2": "值2"
}
```

**响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "result": "成功插入数据到表 表名"
}
```

## 前端实现示例

### JavaScript Socket连接示例

```javascript
class MedicalAPIClient {
    constructor(host = '8.140.225.6', port = 55000) {
        this.host = host;
        this.port = port;
    }

    async sendRequest(data) {
        return new Promise((resolve, reject) => {
            const socket = new WebSocket(`ws://${this.host}:${this.port}`);
            
            socket.onopen = () => {
                // 准备JSON数据
                const jsonStr = JSON.stringify(data);
                const jsonBytes = new TextEncoder().encode(jsonStr);
                const filename = "request.json";
                const filenameBytes = new TextEncoder().encode(filename);
                
                // 构建请求数据包
                const buffer = new ArrayBuffer(8 + filenameBytes.length + jsonBytes.length);
                const view = new DataView(buffer);
                
                // 文件名长度 (4字节)
                view.setUint32(0, filenameBytes.length, false);
                // 文件名
                new Uint8Array(buffer, 4, filenameBytes.length).set(filenameBytes);
                // 数据长度 (4字节)
                view.setUint32(4 + filenameBytes.length, jsonBytes.length, false);
                // JSON数据
                new Uint8Array(buffer, 8 + filenameBytes.length).set(jsonBytes);
                
                socket.send(buffer);
            };
            
            socket.onmessage = (event) => {
                try {
                    const response = JSON.parse(event.data);
                    resolve(response);
                } catch (error) {
                    reject(error);
                }
                socket.close();
            };
            
            socket.onerror = (error) => {
                reject(error);
            };
        });
    }

    // 用户登录
    async login(username, password) {
        return await this.sendRequest({
            login: true,
            user_name: username,
            password: password
        });
    }

    // 患者注册
    async registerPatient(patientData) {
        return await this.sendRequest({
            register_patient: true,
            ...patientData
        });
    }

    // 创建预约
    async createAppointment(appointmentData) {
        return await this.sendRequest({
            create_appointment: true,
            ...appointmentData
        });
    }

    // 查询预约
    async queryAppointments(queryParams) {
        return await this.sendRequest({
            query_appointments: true,
            ...queryParams
        });
    }

    // 查询医生信息
    async getDoctorInfo(doctorName) {
        return await this.sendRequest({
            query_doctor_info: true,
            doctor_name: doctorName
        });
    }
}

// 使用示例
const client = new MedicalAPIClient();

// 登录示例
client.login('13800138000', 'hash_patient1')
    .then(response => {
        if (response.result === 'verificationSuccess') {
            console.log('登录成功');
        } else {
            console.log('登录失败:', response.result);
        }
    })
    .catch(error => {
        console.error('请求失败:', error);
    });
```

### React Hook示例

```javascript
import { useState, useCallback } from 'react';

export const useMedicalAPI = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const apiCall = useCallback(async (data) => {
        setLoading(true);
        setError(null);
        
        try {
            const client = new MedicalAPIClient();
            const response = await client.sendRequest(data);
            
            if (response.status === 'success') {
                return response.result;
            } else {
                throw new Error(response.error || '请求失败');
            }
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const login = useCallback(async (username, password) => {
        return await apiCall({
            login: true,
            user_name: username,
            password: password
        });
    }, [apiCall]);

    const createAppointment = useCallback(async (appointmentData) => {
        return await apiCall({
            create_appointment: true,
            ...appointmentData
        });
    }, [apiCall]);

    return {
        loading,
        error,
        login,
        createAppointment,
        apiCall
    };
};
```

## 错误处理

### 常见错误类型

1. **网络连接错误**
   - 连接超时
   - 连接被拒绝
   - 网络不可达

2. **协议错误**
   - JSON格式错误
   - 数据包格式错误
   - 编码错误

3. **业务逻辑错误**
   - 用户不存在
   - 密码错误
   - 数据验证失败

### 错误处理建议

```javascript
try {
    const response = await client.sendRequest(data);
    
    if (response.status === 'success') {
        // 处理成功响应
        return response.result;
    } else {
        // 处理业务错误
        throw new Error(response.error);
    }
} catch (error) {
    // 处理网络或其他错误
    console.error('API调用失败:', error);
    
    // 根据错误类型进行不同处理
    if (error.name === 'NetworkError') {
        // 网络错误处理
    } else if (error.message.includes('JSON')) {
        // JSON解析错误处理
    } else {
        // 其他错误处理
    }
}
```

## 注意事项

1. **数据格式**: 所有日期时间格式为 `YYYY-MM-DD HH:mm:ss`
2. **编码**: 使用UTF-8编码
3. **密码**: 前端需要对密码进行哈希处理后再发送
4. **超时**: 建议设置合理的请求超时时间 (如10秒)
5. **重试**: 对于网络错误，可以实现重试机制
6. **缓存**: 可以对查询结果进行适当缓存以提升性能

## 测试工具

可以使用项目中的测试脚本验证API：
- `quick_test.py` - 快速功能测试
- `remote_test.py` - 完整测试套件
- `stress_test.py` - 压力测试

---

**如有问题请参考测试脚本示例或联系后端开发团队。**

# 挂号预约功能测试指南

## 📋 功能概述

医疗系统的挂号预约功能提供了完整的预约管理能力：
- ✅ **创建预约**：患者可以预约医生
- ✅ **查询预约**：按患者、医生或日期查询预约记录
- ✅ **取消预约**：取消未完成的预约
- ✅ **状态管理**：更新预约状态（待处理、已完成、已取消）

## 🔧 测试程序

### 1. `test_appointment.py` - 完整功能测试
全面的挂号功能测试程序：
- 🔍 创建预约的各种情况测试
- 🔍 查询预约的多种方式测试  
- 🔍 取消预约的边界条件测试
- 🔍 状态更新的验证测试
- 🔍 完整业务流程测试

### 2. `test_simple_appointment.py` - 快速测试
简化版测试程序，适合快速验证：
- 🚀 创建挂号预约
- 🚀 查询患者预约记录
- 🚀 查询医生预约安排
- 🚀 取消预约测试

## 🚀 使用方法

### 运行完整测试
```bash
python test_appointment.py
```

### 运行快速测试  
```bash
python test_simple_appointment.py
```

## 📊 API 接口详解

### 1. 创建预约/挂号
```json
{
  "create_appointment": true,
  "patient_phone": "13800138000",          // 必需：患者手机号
  "doctor_name": "王医生",                 // 必需：医生姓名
  "appointment_time": "2024-02-15 09:00:00", // 必需：预约时间
  "fee_paid": 1                           // 可选：是否已付费（0/1）
}
```

**成功响应：**
```json
{
  "status": "success",
  "message": "预约创建成功",
  "appointment_info": {
    "appointment_id": 123,
    "patient_phone": "13800138000",
    "doctor_name": "王医生", 
    "appointment_time": "2024-02-15 09:00:00",
    "queue_number": 1,
    "status": "pending",
    "fee_paid": true
  }
}
```

### 2. 查询预约信息
```json
{
  "query_appointments": true,
  // 以下三个条件选择一个：
  "patient_phone": "13800138000",    // 按患者手机号查询
  "doctor_name": "王医生",           // 按医生姓名查询  
  "appointment_date": "2024-02-15"   // 按预约日期查询
  // 如果不提供条件，返回所有预约（限制20条）
}
```

**成功响应：**
```json
{
  "status": "success",
  "message": "查询到 2 条预约记录",
  "appointments": [
    {
      "appointment_id": 123,
      "patient_name": "张三",
      "patient_phone": "13800138000",
      "doctor_name": "王医生",
      "department": "内科",
      "appointment_time": "2024-02-15 09:00:00",
      "status": "pending",
      "fee_paid": true,
      "queue_number": 1,
      "created_at": "2024-02-14 15:30:00"
    }
  ]
}
```

### 3. 取消预约
```json
{
  "cancel_appointment": true,
  "appointment_id": 123                    // 必需：预约ID
}
```

**成功响应：**
```json
{
  "status": "success", 
  "message": "预约ID 123 已成功取消"
}
```

### 4. 更新预约状态
```json
{
  "update_appointment_status": true,
  "appointment_id": 123,                   // 必需：预约ID
  "new_status": "completed"                // 必需：新状态（pending/completed/cancelled）
}
```

**成功响应：**
```json
{
  "status": "success",
  "message": "预约ID 123 状态已从 'pending' 更新为 'completed'"  
}
```

## 📝 测试数据说明

### 默认患者数据
| 姓名 | 手机号 | 邮箱 |
|------|--------|------|
| 张三 | 13800138000 | zhangsan@example.com |
| 李四 | 13900139000 | lisi@example.com |
| 王五 | 15800158000 | wangwu@example.com |

### 默认医生数据
| 姓名 | 工号 | 科室 | 费用 | 状态 |
|------|------|------|------|------|
| 王医生 | DOC001 | 内科 | 50.0 | 可用 |
| 刘医生 | DOC002 | 外科 | 80.0 | 可用 |
| 陈医生 | DOC003 | 儿科 | 60.0 | 可用 |

### 预约状态说明
- **pending**: 待处理（新创建的预约）
- **completed**: 已完成（患者已就诊）
- **cancelled**: 已取消（预约被取消）

## 🔍 测试场景详解

### 正常流程测试
1. **创建预约**
   - 使用有效的患者手机号和医生姓名
   - 设置未来的预约时间
   - 验证自动分配排队号码

2. **查询预约**
   - 按患者查询：验证患者的所有预约
   - 按医生查询：验证医生的预约安排
   - 按日期查询：验证特定日期的预约

3. **状态管理**
   - 更新预约状态为已完成
   - 取消待处理的预约

### 异常情况测试
1. **数据验证错误**
   - 不存在的患者手机号
   - 不存在的医生姓名
   - 缺少必要参数

2. **业务逻辑错误**
   - 医生不可用时的预约
   - 重复取消同一预约
   - 取消已完成的预约

3. **状态冲突错误**
   - 无效的状态值
   - 不存在的预约ID

## ⚠️ 注意事项

### 服务器配置
- 确保服务器在 `8.140.225.6:55000` 运行
- 确保数据库已初始化并包含测试数据

### 时间格式
- 预约时间格式：`YYYY-MM-DD HH:MM:SS`
- 查询日期格式：`YYYY-MM-DD`
- 建议使用未来的日期进行测试

### 排队号码生成规则
- 按医生和日期分组
- 同一医生同一天的预约按创建顺序编号
- 取消的预约不会影响其他预约的排队号

### 数据一致性
- 患者必须在 `patients` 表中存在
- 医生必须在 `doctors` 表中存在且 `is_available = 1`
- 预约创建后会自动生成排队号码

## 🔧 故障排除

### 连接问题
```bash
# 检查服务器状态
python integrated_server_loginmatchAdd.py status

# 重启服务器
python integrated_server_loginmatchAdd.py restart
```

### 数据问题
```bash
# 查看数据库状态
python check_database.py MedicalSystem.db

# 查看预约表数据
python check_database.py MedicalSystem.db --test
```

### 测试失败排查
1. **预约创建失败**
   - 检查患者手机号是否存在
   - 检查医生姓名是否正确
   - 检查医生是否可用（is_available=1）

2. **查询无结果**
   - 确认数据库中有预约数据
   - 检查查询条件是否正确
   - 验证外键关联是否正确

3. **状态更新失败**
   - 确认预约ID存在
   - 检查新状态值是否有效
   - 验证当前状态是否允许更新

## 📈 测试建议

### 测试顺序
1. **基础功能测试**：先运行 `test_simple_appointment.py`
2. **全面功能测试**：再运行 `test_appointment.py`
3. **边界条件测试**：关注异常情况的处理

### 测试策略
1. **数据准备**：确保测试数据完整
2. **功能验证**：验证每个API的基本功能
3. **流程测试**：验证完整的业务流程
4. **异常处理**：测试各种错误情况

### 性能考虑
- 测试大量预约的查询性能
- 测试同一时间段的并发预约
- 验证排队号码的正确性

## 🎯 预期结果

运行测试后，你应该看到：
- ✅ 预约创建成功并返回预约信息
- ✅ 查询功能返回正确的预约记录
- ✅ 状态更新和取消功能正常工作
- ✅ 错误情况得到正确处理
- ✅ 排队号码自动分配正确

测试完成后，数据库中应该有新的预约记录，可以通过数据库工具验证数据的正确性。


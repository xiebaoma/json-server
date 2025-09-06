1. 用户表（users）
字段名	        类型	        说明
user_id	        INT AUTO_INCREMENT	用户ID，主键
username	    VARCHAR(50)	用户名（手机号或工号）
password_hash	VARCHAR(255)	密码哈希
role	        ENUM('patient', 'doctor')	角色：患者或医生
created_at	    DATETIME	创建时间

2. 患者信息表（patients）
字段名	类型	说明
patient_id	INT	患者ID，外键关联users
name	VARCHAR(50)	姓名
birth_date	DATE	出生日期
id_card	VARCHAR(18)	身份证号
phone	VARCHAR(11)	手机号
email	VARCHAR(100)	邮箱
created_at	DATETIME	创建时间
3. 医生信息表（doctors）
字段名	类型	说明
doctor_id	INT	医生ID，外键关联users
name	VARCHAR(50)	姓名
employee_id	VARCHAR(20)	工号
department	VARCHAR(50)	科室
photo_path	VARCHAR(255)	照片存储路径
max_patients	INT	单日最大接诊人数
fee	DECIMAL(10,2)	挂号费用
work_schedule	TEXT	上班时间（JSON格式）
is_available	BOOLEAN	是否可接诊
4. 预约挂号表（appointments）
字段名	类型	说明
appointment_id	INT AUTO_INCREMENT	预约ID，主键
patient_id	INT	患者ID
doctor_id	INT	医生ID
appointment_time	DATETIME	预约时间
status	ENUM('pending', 'completed', 'cancelled')	状态
fee_paid	BOOLEAN	是否已付费
queue_number	INT	排队号码
created_at	DATETIME	创建时间
5. 病历表（medical_records）
字段名	类型	说明
record_id	INT AUTO_INCREMENT	病历ID，主键
patient_id	INT	患者ID
doctor_id	INT	医生ID
diagnosis	TEXT	诊断结果
symptoms	TEXT	症状描述
visit_time	DATETIME	就诊时间
created_at	DATETIME	创建时间
6. 医嘱表（medical_orders）
字段名	类型	说明
order_id	INT AUTO_INCREMENT	医嘱ID，主键
record_id	INT	关联病历ID
doctor_id	INT	医生ID
content	TEXT	医嘱内容
created_at	DATETIME	创建时间
7. 处方表（prescriptions）
字段名	类型	说明
prescription_id	INT AUTO_INCREMENT	处方ID，主键
record_id	INT	关联病历ID
doctor_id	INT	医生ID
content	TEXT	处方内容（药品、用法）
created_at	DATETIME	创建时间
8. 打卡记录表（attendance）
字段名	类型	说明
attendance_id	INT AUTO_INCREMENT	打卡ID，主键
doctor_id	INT	医生ID
check_in_time	DATETIME	打卡时间
check_out_time	DATETIME	签退时间（可选）
status	ENUM('present', 'absent')	出勤状态
9. 聊天记录表（chat_messages）
字段名	类型	说明
message_id	INT AUTO_INCREMENT	消息ID，主键
sender_id	INT	发送者ID（用户ID）
receiver_id	INT	接收者ID（用户ID）
content	TEXT	消息内容
sent_at	DATETIME	发送时间
is_read	BOOLEAN	是否已读
10. 请假表（leave_requests）
字段名	类型	说明
leave_id	INT AUTO_INCREMENT	请假ID，主键
doctor_id	INT	医生ID
start_date	DATE	开始日期
end_date	DATE	结束日期
reason	TEXT	请假事由
status	ENUM('pending', 'approved', 'rejected')	状态
created_at	DATETIME	申请时间
11. 住院信息表（hospitalizations）
字段名	类型	说明
hospitalization_id	INT AUTO_INCREMENT	住院记录ID，主键
patient_id	INT	患者ID
doctor_id	INT	主治医生ID
ward_number	VARCHAR(20)	病房号
bed_number	VARCHAR(20)	床号
admission_date	DATE	入院日期
discharge_date	DATE	出院日期（可为空）
status	ENUM('admitted', 'discharged')	住院状态
created_at	DATETIME	记录创建时间
updated_at	DATETIME	最后更新时间
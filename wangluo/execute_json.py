import json
import sqlite3
import os


def process_json_file(json_file_path, db_path='database.db'):
    """
    处理JSON文件：根据内容自动判断是执行SQL查询还是插入数据
    :param json_file_path: JSON文件路径
    :param db_path: 数据库文件路径
    :return: 执行结果或错误信息
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # 检查JSON中是否包含sql_query键
        if 'reset_password' in data:
            return update_user_password(db_path, data)
        elif 'reset_patient_information' in data:
            return update_patient_info(data, db_path)
        elif 'reset_doctor_information' in data:
            return
        elif 'sql_query' in data:
            return execute_sql(data, db_path)
        else:
            # 检查是否包含table_name键，如果没有则使用默认表名
            table_name = data.get('table_name', 'default_table')
            # 移除table_name键，剩下的就是数据
            if 'table_name' in data:
                del data['table_name']
            return insert_data(data, table_name, db_path)

    except Exception as e:
        return f"错误: {str(e)}"


def insert_data(data, table_name, db_path='database.db'):
    """
    将数据插入到数据库表中
    :param data: 要插入的数据字典
    :param table_name: 目标表名
    :param db_path: 数据库文件路径
    :return: 成功消息或错误信息
    """
    try:
        if not data:
            return "错误: 没有提供数据"

        # 使用参数化查询避免SQL注入
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # 连接数据库并执行
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_insert, list(data.values()))
        conn.commit()
        conn.close()

        return f"成功插入数据到表 {table_name}"

    except Exception as e:
        # 如果连接已打开，确保回滚并关闭
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return f"错误: {str(e)}"


def execute_sql(data, db_path='database.db'):
    """
    执行JSON中的SQL查询
    :param data: 包含SQL查询的字典
    :param db_path: SQLite数据库文件路径
    :return: 查询结果或错误信息
    """
    try:
        sql_query = data.get('sql_query')
        if not sql_query:
            return "错误: JSON中未找到'sql_query'键"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        # 如果是SELECT查询，返回结果
        if sql_query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            conn.close()
            # 可选择返回栏目名 return {"columns": columns, "data": result}
            return result
        #result就是查询结果
        else:
            conn.commit()
            conn.close()
            return "执行成功"

    except Exception as e:
        # 如果连接已打开，确保关闭
        if 'conn' in locals() and conn:
            conn.close()
        return f"错误: {str(e)}"


def update_user_password(data, db_path='database.db'):
    """
    更新用户密码：根据user_name找到用户，更新密码为new_password的值
    :param data: 包含用户信息的字典
    :param db_path: 数据库文件路径
    :return: 成功消息或错误信息
    """
    try:
        # 检查必要字段
        if 'user_name' not in data:
            return "错误: 需要提供user_name字段"
        if 'new_password' not in data:
            return "错误: 需要提供new_password字段"

        user_name = data['user_name']
        new_password = data['new_password']

        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查用户是否存在
        cursor.execute("SELECT * FROM users WHERE username = ?", (user_name,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return f"错误: 未找到用户名为 {user_name} 的用户"

        # 更新密码
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, user_name))
        conn.commit()
        conn.close()

        return f"用户 {user_name} 的密码更新成功"

    except Exception as e:
        # 如果连接已打开，确保回滚并关闭
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return f"错误: {str(e)}"


def update_patient_info(data, db_path='database.db'):
    """
    更新患者信息：根据old_phone找到患者，更新为提供的new_*字段值
    :param data: 包含患者信息的字典
    :param db_path: 数据库文件路径
    :return: 成功消息或错误信息
    """
    try:
        # 检查必要字段
        if 'old_phone' not in data:
            return "错误: 需要提供old_phone字段"

        old_phone = data['old_phone']

        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查患者是否存在
        cursor.execute("SELECT * FROM patients WHERE phone = ?", (old_phone,))
        patient = cursor.fetchone()

        if not patient:
            conn.close()
            return f"错误: 未找到手机号为 {old_phone} 的患者"

        # 获取列名
        cursor.execute("PRAGMA table_info(patients)")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]

        # 构建更新语句
        update_fields = []
        update_values = []

        # 映射新字段名到数据库字段名
        field_mapping = {
            'new_name': 'name',
            'new_birth_date': 'birth_date',
            'new_id_card': 'id_card',
            'new_phone': 'phone',
            'new_email': 'email'
        }

        # 收集需要更新的字段和值
        for json_key, db_field in field_mapping.items():
            if json_key in data:
                update_fields.append(f"{db_field} = ?")
                update_values.append(data[json_key])

        # 如果没有提供任何新字段，则返回错误
        if not update_fields:
            conn.close()
            return "错误: 未提供任何需要更新的字段"

        # 添加old_phone作为WHERE条件的值
        update_values.append(old_phone)

        # 构建SQL更新语句
        sql_update = f"UPDATE patients SET {', '.join(update_fields)} WHERE phone = ?"

        # 执行更新
        cursor.execute(sql_update, update_values)
        conn.commit()
        conn.close()

        return f"手机号为 {old_phone} 的患者信息更新成功"

    except Exception as e:
        # 如果连接已打开，确保回滚并关闭
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return f"错误: {str(e)}"


def update_doctor_info(data, db_path='database.db'):
    """
    更新医生信息：根据old_employee_id找到医生，更新为提供的new_*字段值
    :param data: 包含医生信息的字典
    :param db_path: 数据库文件路径
    :return: 成功消息或错误信息
    """
    try:
        # 检查必要字段
        if 'old_employee_id' not in data:
            return "错误: 需要提供old_employee_id字段"

        old_employee_id = data['old_employee_id']

        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查医生是否存在
        cursor.execute("SELECT * FROM doctors WHERE employee_id = ?", (old_employee_id,))
        doctor = cursor.fetchone()

        if not doctor:
            conn.close()
            return f"错误: 未找到工号为 {old_employee_id} 的医生"

        # 获取列名
        cursor.execute("PRAGMA table_info(doctors)")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]

        # 构建更新语句
        update_fields = []
        update_values = []

        # 映射新字段名到数据库字段名
        field_mapping = {
            'new_name': 'name',
            'new_employee_id': 'employee_id',
            'new_department': 'department',
            'new_fee': 'fee',
            'new_work_schedule': 'work_schedule',
            'new_is_available': 'is_available',
            'new_photo_path': 'photo_path'
        }

        # 收集需要更新的字段和值
        for json_key, db_field in field_mapping.items():
            if json_key in data:
                update_fields.append(f"{db_field} = ?")
                update_values.append(data[json_key])

        # 如果没有提供任何新字段，则返回错误
        if not update_fields:
            conn.close()
            return "错误: 未提供任何需要更新的字段"

        # 添加old_employee_id作为WHERE条件的值
        update_values.append(old_employee_id)

        # 构建SQL更新语句
        sql_update = f"UPDATE doctors SET {', '.join(update_fields)} WHERE employee_id = ?"

        # 执行更新
        cursor.execute(sql_update, update_values)
        conn.commit()
        conn.close()

        return f"工号为 {old_employee_id} 的医生信息更新成功"

    except Exception as e:
        # 如果连接已打开，确保回滚并关闭
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return f"错误: {str(e)}"

# 示例用法
if __name__ == "__main__":
    # 首先创建示例表和数据库


    # 示例1: 插入数据的JSON文件
    insert_json = {
        "table_name": "students",
        "name": "张三",
        "age": 20,
        "student_id": 192939821
    }

    with open('insert_data.json', 'w') as f:
        json.dump(insert_json, f)

    # 处理插入JSON
    result = process_json_file('insert_data.json')
    print("插入结果:", result)

    # 示例2: 查询数据的JSON文件
    query_json = {
        "sql_query": "SELECT * FROM students WHERE student_id = 192939821"
    }

    with open('query_data.json', 'w') as f:
        json.dump(query_json, f)

    # 处理查询JSON
    result = process_json_file('query_data.json')
    print("查询结果:", result)
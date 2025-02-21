# from sqlalchemy import inspect
# from sqlalchemy.orm import Session
# from app.database import engine, Base, SessionLocal
# from app.models import MyTable

# def check_table_structure(engine, table_name, expected_columns):
#     inspector = inspect(engine)
#     if table_name in inspector.get_table_names():
#         columns = {col["name"]: col["type"] for col in inspector.get_columns(table_name)}
#         for col_name, col_type in expected_columns.items():
#             if col_name not in columns or not isinstance(columns[col_name], col_type):
#                 return False  # 结构不符合
#         return True  # 结构符合
#     return False  # 表不存在

# def backup_and_create_table(engine, session, table_class):
#     table_name = table_class.__tablename__
#     expected_columns = {"id": int, "name": str}

#     if check_table_structure(engine, table_name, expected_columns):
#         print(f"✅ 表 {table_name} 结构符合要求，无需修改。")
#         return
    
#     if table_name in inspect(engine).get_table_names():
#         backup_table_name = f"{table_name}_backup"
#         counter = 1
#         while backup_table_name in inspect(engine).get_table_names():
#             backup_table_name = f"{table_name}_backup_{counter}"
#             counter += 1

#         session.execute(f"ALTER TABLE {table_name} RENAME TO {backup_table_name}")
#         session.commit()
#         print(f"🔄 旧表 {table_name} 备份为 {backup_table_name}")

#     print(f"🆕 创建新表 {table_name}")
#     Base.metadata.create_all(bind=engine)

# def initialize_database():
#     session = SessionLocal()
#     try:
#         backup_and_create_table(engine, session, MyTable)
#     finally:
#         session.close()

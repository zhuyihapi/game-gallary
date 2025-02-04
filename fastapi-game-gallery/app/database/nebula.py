# # utils/nebula_db.py
# import time
# import networkx as nx
# from typing import Optional, Union
# from nebula3.gclient.net import ConnectionPool
# from nebula3.Config import Config
# from nebula3.data.ResultSet import ResultSet

# from app.config import connect_pool_settings
# from app.log.logger import logger
# from app.utils.string_utils import escape_and_quote_string


# class NebulaDB:
#     def __init__(self, addresses, user, password):
#         self.user = user
#         self.password = password
#         # 初始化连接池配置
#         self.config = Config()
#         self.config.max_connection_pool_size = (
#             connect_pool_settings.MAX_CONNECT_POOL_SIZE
#         )
#         self.pool = ConnectionPool()
#         assert self.pool.init(addresses, self.config)

#     def execute_query(self, query: str, space_name: str, return_format: str):
#         # 执行查询语句 # 获取会话
#         session = self.pool.get_session(self.user, self.password)
#         try:
#             if not session:
#                 raise Exception("Failed to create session")
#             if space_name:
#                 resp = session.execute(f"USE {space_name}")
#                 if not resp.is_succeeded():
#                     session.release()
#                     raise Exception(f"Failed to use space: {resp.error_msg()}")

#             result = session.execute(query)
#             format_map = {
#                 "primitive": result.as_primitive,
#                 "edge_vertex": result.dict_for_vis(),
#                 "dataframe": result.as_data_frame,
#                 "original": result,
#             }
#             if return_format not in format_map:
#                 raise ValueError(f"Unsupported return format: {return_format}")
#             return format_map[return_format]
#         except Exception as e:
#             logger.error(
#                 f"Error executing query: {query}, return_format: {return_format}. Details: {e}"
#             )

#             return None
#         finally:
#             session.release()

#     def create_spaces(self, space_name: str):
#         session = self.pool.get_session(self.user, self.password)
#         resp = session.execute("SHOW SPACES")
#         spaces = [record.values[0].get_sVal().decode("utf-8") for record in resp.rows()]
#         try:
#             if space_name not in spaces:
#                 logger.info(f"Space {space_name} does not exist, creating it now.")
#                 # 创建新的空间
#                 create_space_query = f"CREATE SPACE IF NOT EXISTS {space_name}(partition_num=10, replica_factor=1, vid_type=FIXED_STRING(40));"
#                 resp = session.execute(create_space_query)

#                 # 等待几秒钟让创建的空间生效（根据需要调整）
#                 time.sleep(10)
#                 resp = session.execute(f"USE {space_name}")

#                 # 创建tag
#                 create_tag_query = (
#                     "CREATE TAG IF NOT EXISTS entity("
#                     "datamodel_id string, "
#                     "graph_id string, "
#                     "datamodel_name string, "
#                     "datamodel_description string, "
#                     "datasource_id string, "
#                     "datasource_name string, "
#                     "datasheet_name_zh string COMMENT '数据表中文名', "
#                     "datasheet_name_en string COMMENT '数据表英文名', "
#                     "datasheet_description string, "
#                     "datasheet_type string, "
#                     "datasheet_structure string, "
#                     "service_object_id string, "
#                     "service_object_name string, "
#                     "service_object_description string, "
#                     ") COMMENT='实体';"
#                 )
#                 resp = session.execute(create_tag_query)
#                 # 创建边类型
#                 create_relation_tag_query = (
#                     "CREATE EDGE IF NOT EXISTS relation("
#                     "graph_id string, "
#                     "weight float, "
#                     "relation_name string, "
#                     "description string, "
#                     "src_tgt_field string,"
#                     ") COMMENT='关系';"
#                 )
#                 resp = session.execute(create_relation_tag_query)
#                 # 创建datasheet_id查询tag的index
#                 create_entity_index_query = f"CREATE TAG INDEX IF NOT EXISTS graph_id_index_0 on entity(graph_id(40));"
#                 resp = session.execute(create_entity_index_query)
#                 # 创建datasheet_id查询edge的index
#                 create_edge_index_query = f"CREATE EDGE INDEX IF NOT EXISTS graph_id_index_1 on relation(graph_id(40));"
#                 resp = session.execute(create_edge_index_query)

#                 if not resp.is_succeeded():
#                     raise Exception(f"Failed to create space: {resp.error_msg()}")
#                 time.sleep(10)
#             # 使用指定的空间
#             use_space_query = f"USE {space_name}"
#             resp = session.execute(use_space_query)
#             if not resp.is_succeeded():
#                 raise Exception(f"Failed to use space: {resp.error_msg()}")
#             return True
#         except Exception as e:
#             logger.error(e)
#             return False
#         finally:
#             session.release()

#     def insert_data(self, space_name: str, graph: nx.Graph):
#         session = self.pool.get_session(self.user, self.password)

#         space = space_name

#         try:
#             # Insert nodes (vertices)
#             resp = session.execute(f"USE {space}")
#             if not resp.is_succeeded():
#                 session.release()
#                 raise Exception(f"Failed to use space: {resp.error_msg()}")

#             for node in graph.nodes(data=True):  # 返回图中所有节点及其属性
#                 node_id = str(node[0])
#                 properties = {
#                     key: str(value) for key, value in node[1].items()
#                 }  # node[1] 是节点的属性字典
#                 property_string = ",".join(
#                     [
#                         (
#                             f"{escape_and_quote_string(v)}"
#                             if isinstance(v, str)
#                             else "NULL" if v is None else v
#                         )
#                         for k, v in properties.items()
#                     ]
#                 )
#                 key_list = properties.keys()
#                 insert_node_query = f'INSERT VERTEX entity({",".join(key_list)}) VALUES "{node_id}":({property_string});'
#                 # print(f"Executing node insert SQL: {insert_node_query}")
#                 resp = session.execute(insert_node_query)
#                 if not resp.is_succeeded():
#                     raise Exception(
#                         f"Failed to insert vertex {node_id}: {resp.error_msg()}"
#                     )

#             # Insert edges
#             for edge in graph.edges(data=True):
#                 src_id = str(edge[0])
#                 dst_id = str(edge[1])
#                 properties = {key: value for key, value in edge[2].items()}
#                 # print(f"properties: {properties}")
#                 processed_values = []
#                 for key, value in properties.items():
#                     # 如果 value 是字符串，调用 process_string 对其处理
#                     if isinstance(value, str):
#                         processed_values.append(f"{escape_and_quote_string(value)}")
#                     # 如果 value 是 None，添加字符串 "NULL"
#                     elif value is None:
#                         processed_values.append("NULL")
#                     # 否则，将 value 转换为字符串并添加
#                     else:
#                         processed_values.append(str(value))
#                     # print(f"{value}, {type(value)}")

#                 property_string = ",".join(processed_values)

#                 # print(f"property_string: {property_string}")
#                 insert_edge_query = f'INSERT EDGE relation ({",".join(properties.keys())}) VALUES "{src_id}"->"{dst_id}":({property_string});'
#                 # print(f"Executing edge insert SQL: {insert_edge_query}")
#                 resp = session.execute(insert_edge_query)
#                 if not resp.is_succeeded():
#                     raise Exception(
#                         f"Failed to insert edge from {src_id} to {dst_id}: {str(resp.error_msg())}"
#                     )
#             return True
#         except Exception as e:
#             logger.error(e)
#             return False
#         finally:
#             session.release()

#     def delete_data(self, space_name: str, graph_id: str):
#         session = self.pool.get_session(self.user, self.password)

#         try:
#             resp = session.execute(f"USE {space_name}")
#             if not resp.is_succeeded():
#                 session.release()
#                 raise Exception(f"Failed to use space: {resp.error_msg()}")

#             # Find all edges with the specified edge type and graph_id
#             # relation should be a param
#             find_edges_query = f"""
#             MATCH ()-[e:relation]->()
#             WHERE e.graph_id == \"{graph_id}\"
#             RETURN src(e), dst(e), rank(e)
#             """
#             result_edges: ResultSet = session.execute(find_edges_query)
#             if not result_edges.is_succeeded():
#                 raise Exception(
#                     f"Failed to execute find_edges_query: {result_edges.error_msg()}"
#                 )

#             edge_info = []
#             for i in range(len(result_edges.rows())):
#                 values = result_edges.row_values(i)
#                 src = values[0].as_string()
#                 dst = values[1].as_string()
#                 rank = values[2].as_int()
#                 edge_info.append((src, dst, rank))

#             # Delete each edge
#             for src, dst, rank in edge_info:
#                 delete_edge_query = f'DELETE EDGE relation "{src}" -> "{dst}"'
#                 logger.debug(delete_edge_query)
#                 if rank != 0:  # Include rank if it's not the default
#                     delete_edge_query += f" @{rank}"
#                 result_delete_edge = session.execute(delete_edge_query)
#                 if not result_delete_edge.is_succeeded():
#                     raise Exception(
#                         f"Failed to delete edge {src} -> {dst}: {result_delete_edge.error_msg()}"
#                     )

#             # Find all vertices with the specified tag and graph_id
#             find_vertices_query = f"""
#             MATCH (v:entity)
#             WHERE v.entity.graph_id == \"{graph_id}\"
#             RETURN id(v)
#             """
#             result_vertices: ResultSet = session.execute(find_vertices_query)
#             if not result_vertices.is_succeeded():
#                 raise Exception(
#                     f"Failed to execute query: {result_vertices.error_msg()}"
#                 )

#             vertex_ids = []
#             for i in range(len(result_vertices.rows())):
#                 values = result_vertices.row_values(i)
#                 vertex_ids.append(values[0].as_string())

#             # Delete each vertex
#             for vid in vertex_ids:
#                 delete_vertex_query = f'DELETE VERTEX "{vid}"'
#                 logger.debug(delete_vertex_query)
#                 result_delete_vertex = session.execute(delete_vertex_query)
#                 if not result_delete_vertex.is_succeeded():
#                     raise Exception(
#                         f"Failed to delete vertex {vid}: {result_delete_vertex.error_msg()}"
#                     )

#             logger.info(
#                 f"Successfully deleted all vertices and edges with graph_id '{graph_id}'."
#             )
#             return True
#         except Exception as e:
#             logger.error("Error during delete graph", str(e))
#             return False
#         finally:
#             session.release()

#     def delete_space(self, space_name):
#         # 获取会话
#         session = self.pool.get_session(self.user, self.password)
#         try:
#             resp = session.execute(f"DROP SPACE {space_name}")
#             if not resp.is_succeeded():
#                 session.release()
#                 raise Exception(f"Failed to drop space: {resp.error_msg()}")
#             time.sleep(5)
#             return True
#         except Exception as e:
#             logger.error(e)
#             return False
#         finally:
#             session.release()

#     def clear_space(self, space_name):
#         # 获取会话
#         session = self.pool.get_session(self.user, self.password)
#         try:
#             resp = session.execute(f"CLEAR SPACE {space_name}")
#             if not resp.is_succeeded():
#                 session.release()
#                 raise Exception(f"Failed to drop space: {resp.error_msg()}")
#             time.sleep(5)
#             return True
#         except Exception as e:
#             logger.error(e)
#             return False
#         finally:
#             session.release()

#     def close(self):
#         # 关闭连接池
#         self.pool.close()

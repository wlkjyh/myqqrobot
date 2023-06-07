""" 
    数据库操作门面
"""

import handle.constant as runn
import pymysql
import time
import random


db_conn = pymysql.connect(
    host=runn.DB_HOST,
    port=int(runn.DB_PORT),
    user=runn.DB_USERNAME,
    passwd=runn.DB_PASSWORD,
    db=runn.DB_DATABASE,
    charset='utf8'
)

class DB:

    table_name = None
    wheres = []
    orWheres = []
    orderBys = None
    selects = ['*']
    primaryKey = 'id'
    isDelete = False
    updateData = []
    # pageinates = []
    limit_start = None
    limit_end = None


    

    created_at = True
    updated_at = True

    created_at_field = 'created_at'
    updated_at_field = 'updated_at'

    
    toSqls = None

    completeValue = []

    def __init__(self,primaryKey = 'id',created_at=True,updated_at=True):
        """_summary_

        Args:
            primaryKey (str, optional): 主键
            created_at (bool, optional): 是否开启记录创建时间
            updated_at (bool, optional): 是否开启记录更新时间
        """
        if not runn.DB_OPEN:
            raise Exception('数据库服务未开启')
    

        self.primaryKey = primaryKey
        self.created_at = created_at
        self.updated_at = updated_at
        table_name = None
        self.wheres = []
        self.orWheres = []
        self.orderBys = None
        self.selects = ['*']
        self.isDelete = False
        self.updateData = []
        self.limit_start = None
        self.limit_end = None
        self.created_at_field = 'created_at'
        self.updated_at_field = 'updated_at'
        self.toSqls = None
        self.completeValue = []


    
    def timestamps(self,bool=True):
        """是否开启记录时间

        Args:
            bool (bool, optional): _description_. Defaults to True.
        """
        if bool == False:
            self.created_at = False
            self.updated_at = False
        else:
            self.created_at = True
            self.updated_at = True



    
    def table(self,table_name):
        """选择表

        Args:
            table_name (string): 表名
        """
        self.table_name = table_name
        return self


    def where(self,field,wheretype,where=None):
        """查询条件

        Args:
            field (str): 字段名 
            wheretype (str): 条件或者操作符
            where (str, None): 条件值，当wheretype为操作符时，该值才有效

        Returns:
            _type_: _description_
        """

        # 如果密钥传入where，那么就是=操作
        if where == None:
            where = str(wheretype)
            wheretype = '='

        self.wheres.append({
            'field':field,
            'type':wheretype,
            'where':where
        })

        return self
    
    def orWhere(self,field,wheretype,where=None):
        """or查询条件

        Args:
            field (str): 字段名 
            wheretype (str): 条件或者操作符
            where (str, None): 条件值，当wheretype为操作符时，该值才有效

        Returns:
            _type_: _description_
        """

        if where == None:
            where = str(wheretype)
            wheretype = '='

        self.orWheres.append({
            'field':field,
            'type':wheretype,
            'where':where
        })

        return self
    
    def increment(self,field,value=1):
        """自增

        Args:
            field (str): 字段
            value (int, optional): 增加值. Defaults to 1.
        """


        try:
            query = self.first()
            if query == None or len(query) == 0:
                raise Exception('没有找到该记录')
            
            field_value = self.filedFormatInt(query[field]) + float(value)
            self.completeValue = []
            self.wheres = []
            # 添加主键进去
            self.where(self.primaryKey,query[self.primaryKey])
            
            self.update({
                field:str(field_value)
            })

            return True
        except Exception as e:
            raise e
        

    def decrement(self,field,value=1):
        """自减

        Args:
            field (str): 字段
            value (int, optional): 减少值. Defaults to 1.
        """

        try:
            return self.increment(field,-value)
        except Exception as e:
            raise e
        

    def getPrimaryKey(self):
        """获取主键的值

        Returns:
            _type_: _description_
        """
        query = self.first()
        if query == None or len(query) == 0:
            return None
        
        return query[self.primaryKey]
        

        
    def filedFormatInt(self,value):
        """字段格式化为int
        """
        if value == None or value == '':
            return 0
        
        return float(value)

    
    def orderBy(self,field,order='desc'):
        """排序

        Args:
            field (str): 字段
            order (str, optional): 排序方式. Defaults to 'desc'.

        """
        if order != 'desc' and order != 'asc':
            order = 'desc'
        self.orderBys = [field,order]
        return self
    
    def limit(self,start,end=None):
        """限制查询条数

        Args:
            start (int): 开始条数
            end (int, optional): 结束条数. Defaults to None.
        """
        self.limit_start = start
        self.limit_end = end
        return self
    
    def getRandom(self,number=1):
        """随机查询

        Args:
            number (int, optional): 查询数量. Defaults to 1.
        """
        query = self.get()
        if query == None or len(query) == 0:
            return []
        
        if len(query) <= number:
            return query
        
        return random.sample(query,number)
    
    def select(self,select):
        """选择字段

        Args:
            select (list|str): 字段

            注意：你可以传入一个列表，也可以传入一个字符串，如果传入一个字符串，请使用,隔开

        
        """

        # 当 = 1时，说明查询所有字段，要把它清空
        if len(self.selects) == 1 and self.selects[0] == '*':
            self.selects = []

        if isinstance(select,list):
            select = ','.join(select)
            

        self.selects.append(select)
        return self
    
    def pluck(self,field):
        """获取某个字段的值

        Args:
            field (str|list): 字段
        """
        return self.select(field).get()
    

    def value(self,field):
        """ 获取第一条数据的某个字段的值

        Args:
            field (str): 字段
        """
        try:
            return self.first()[field]
        except Exception as e:
            raise e
    

    def valueMany(self,field):
        """获取某个字段的值

        Args:
            field (list): 字段
        """
        try:
            query = self.first()
            if query == None or len(query) == 0:
                return {}
            
            result = {}
            for k,v in enumerate(field):
                if v in query:
                    result[v] = query[v]


            return result
        
        except Exception as e:
            raise e
        

    def each(self,callback):
        """遍历数据

        Args:
            callback (function): 回调函数，必须包含一个参数，参数为每一条数据
        """
        try:
            query = self.get()
            if query == None or len(query) == 0:
                return None
            
            for i in query:
                callback(i)
            
            return True
        except Exception as e:
            raise e
        
    def map(self,callback):
        """遍历数据，并且支持修改数据

        Args:
            callback (function): 回调函数，必须包含一个参数，参数为每一条数据
        """
        try:
            query = self.get()
            if query == None or len(query) == 0:
                return None
            
            for i in query:
                primaryKeyValue = i[self.primaryKey]
                updateinfo = callback(i)
                if isinstance(updateinfo,dict):
                    try:
                        DB(self.created_at,self.updated_at).table(self.table_name).where(self.primaryKey,primaryKeyValue).update(updateinfo)
                    except:
                        continue
                    
            return True
        except Exception as e:
            raise e
        

    def whereIn(self,field,value):
        """in查询

        Args:
            field (str): 字段
            value (list): 值
        """
        for k in range(len(value)):
            v = value[k]
            if k == 0:
                self.where(field,v)
            else:
                self.orWhere(field,v)


        return self
            

    
    def create(self,dict):
        if self.created_at:
            dict[self.created_at_field] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.updated_at:
            dict[self.updated_at_field] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sql = 'insert into ' + self.table_name + ' (' + ','.join(dict.keys()) + ') values (' + ','.join(['%s' for i in range(len(dict.keys()))]) + ')'
        self.completeValue = list(dict.values())
        return self._query(sql)
    
    def find(self,value):
        """基于主键查询

        Args:
            value (str): 查询值
        """
        self.where(self.primaryKey,'=',value)
        return self.first()
    
    def first(self):
        """获取第一条数据
        """
        # return self.get()[0]
        result = self.get()
        try:
            return result[0]
        except Exception as e:
            return []
    
    def end(self):
        """获取最后一条数据
        """
        return self.get()[-1]
    
    def count(self):
        """获取数据总数
        """
        return len(self.get())
    
    def delete(self):
        """删除数据
        """
        self.isDelete = True
        
        return self.get()
    
    def get(self):
        """查询多条数据
        """
        sql = self._buildSql()
        try:
            return self._query(sql)
        except Exception as e:
            return {'error':e}
        
        
    def findAuto(self,op,value=None):
        """自动处理查询

        Args:
            value (str): 查询值
        """
        try:
            db_conn.ping(reconnect=True)
        except Exception as e:
            pass

        if self.table_name == None:
            raise Exception('未选择表')
        

        # 先反射出表的字段
        sql = 'desc ' + self.table_name
        cursor = db_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        if value == None:
            value = op
            op = '='

        for k in range(len(result)):
            v = result[k]
            if k == 0:
                self.where(v[0],op,value)
            else:
                self.orWhere(v[0],op,value)

        return self.first()
        
    
    def paginate(self,page=1,limit=10):
        """分页查询

        Args:
            page (int, optional): 页码. Defaults to 1.
            limit (int, optional): 每页条数. Defaults to 10.
        """

        # self.pageinates = [page,limit]
        # return self.get()
        if page <= 1:
            self.limit(limit)
        else:
            self.limit((page-1)*limit,limit * page)

        return self.get()


    def execute(self,sql,completeValue=[]):
        """执行sql语句

        Args:
            sql (str): sql语句
            completeValue (list, optional): 预编译值. Defaults to [].
        """
        self.completeValue = completeValue
        return self._query(sql)
    

    def all(self):
        """获取所有数据

        注意：这个方法会清空where条件，如果需要保留where条件，请使用get方法

        """

        self.wheres = []
        self.orWheres = []
        self.limit_end = None
        self.limit_start = None
        self.completeValue = []

        return self.get()
    
    

    
    def _query(self,sql):
        """执行sql语句

        Args:
            sql (str): sql语句

        Returns:
            list: 查询结果
        """

        try:
            db_conn.ping(reconnect=True)
        except:
            pass

        # 这里用到了预编译SQL
        try:
            
            cursor = db_conn.cursor()
            cursor.execute(sql,self.completeValue)
            result = cursor.fetchall()
            fields = [i[0] for i in cursor.description]
            res = [dict(zip(fields, row)) for row in result]
            cursor.close()
            db_conn.commit()
            return res
            
        except Exception as e:
            db_conn.rollback()
            return {'error':e}
    
    def update(self,dict):
        """更新数据

        Args:
            dict (dict): 更新的数据
        """

        if self.updated_at:
            dict[self.updated_at_field] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


        self.updateData = dict

        return self.get()
    
    def toSql(self):
        """获取sql语句
        """
        return self.toSqls
    
    
    def _buildSql(self):
        """构建sql语句
        """

        if self.isDelete:
            sql = 'delete from ' + self.table_name
        elif len(self.updateData) == 0:
            sql = 'select ' + ','.join(self.selects) + ' from ' + self.table_name
        else:
            sql = 'update ' + self.table_name + ' set '
            for key in self.updateData:
                sql += '`' + str(key) + '` = %s,'
                self.completeValue.append(self.updateData[key])
            sql = sql[:-1]

        if len(self.wheres) > 0:
            sql += ' where '
            for where in self.wheres:
                sql += '`' + where['field'] + '` ' + where['type'] + ' %s and '
                self.completeValue.append(where['where'])
            sql = sql[:-4]

        if len(self.orWheres) > 0:
            sql += ' or '
            for where in self.orWheres:
                sql += '`' + where['field'] + '` ' + where['type'] + ' %s or '
                self.completeValue.append(where['where'])
            sql = sql[:-3]

        if self.orderBys != None and not self.isDelete and len(self.updateData) == 0:
            sql += ' order by ' + self.orderBys[0] + ' ' + self.orderBys[1]

        # 限制查询条数
        if self.limit_start != None and not self.isDelete and len(self.updateData) == 0:
            if self.limit_end == None:
                sql += ' limit ' + str(self.limit_start)
            else:
                sql += ' limit ' + str(self.limit_start) + ',' + str(self.limit_end)
    

        self.toSqls = sql
        return sql
""" 
    数据库操作门面
"""

import handle.constant as runn
import pymysql
import time

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
    
    def select(self,select):
        """选择字段

        Args:
            select (list): 字段，用,分割

        
        """
        self.selects = select
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
            return Exception(e)
    
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
            return Exception(e)
    
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

        # # 自动分页
        # if len(self.pageinates) > 0 and not self.isDelete and len(self.updateData) == 0:
        #     # 如果是第一页，就是limit 0,limit
        #     if self.pageinates[0] <= 1:
        #         sql += ' limit ' + str(self.pageinates[1])
        #     else:
        #         sql += ' limit ' + str((self.pageinates[0] - 1) * self.pageinates[1]) + ',' + str(self.pageinates[1] * self.pageinates[0])

        # 限制查询条数
        if self.limit_start != None and not self.isDelete and len(self.updateData) == 0:
            if self.limit_end == None:
                sql += ' limit ' + str(self.limit_start)
            else:
                sql += ' limit ' + str(self.limit_start) + ',' + str(self.limit_end)
    

        self.toSqls = sql
        return sql


        

        



            

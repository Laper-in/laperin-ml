import mysql.connector
import shortuuid

class Database:
    def __init__(self):
        self.my_db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='',
        )
        self.my_cursor = self.my_db.cursor()

    def close_connection(self):
        self.my_cursor.close()
        self.my_db.close()

class DatabaseAccess:
    def __init__(self):
        self.database = Database()

    def read_id(self, table_name, mode='ASC'):
        '''Read recipe ids from database'''
        try:
            sql = 'SELECT idRecipe FROM {} ORDER BY idRecipe {}'.format(table_name, mode)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)
        
    def check_not_exist_id(self, first_table, second_table):
        '''Check recipe ids that not exist in second table'''
        try:
            sql = 'SELECT a.id FROM {} a WHERE a.id NOT IN (SELECT DISTINCT p.idRecipe FROM {} p) ORDER BY id'.format(first_table, second_table)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)

    def read_ingredients(self, table_name, id_column, mode='ASC'):
        '''Read ingredients from database'''
        try:
            sql = 'SELECT ingredient FROM {} ORDER BY {} {}'.format(table_name, id_column, mode)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)
        
    def read_ingredients_by_ids(self, table_name, id_column, recipe_ids):
        '''Read ingredients from database by recipe ids'''
    
        try:
            sql = 'SELECT ingredient FROM {} WHERE {} IN ({})'.format(table_name, id_column, recipe_ids)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)
        
    def insert_many_ingredients(self, list_data, table_name='recipe_details'):
        '''Insert multiple ingredients to database'''
        try:
            sql = 'INSERT INTO {} (id, idRecipe, ingredient) VALUES (%s, %s, %s)'.format(table_name)
            # modified list_data by adding new id column that using random string
            list_data = [(shortuuid.uuid()[:10], item[0], item[1]) for item in list_data]

            self.database.my_cursor.executemany(sql, list_data)
            self.database.my_db.commit()
            return self.database.my_cursor.rowcount
        except mysql.connector.Error as e:
            return str(e)

    def close_connection(self):
        self.database.close_connection()
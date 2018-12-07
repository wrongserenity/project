import psycopg2 as pg
import logging


# TODO: add try:.. except... wrappers
class PostgresConnection:
    def __init__(self, configs):
        try:
            self.__conn = pg.connect(**configs)
        except pg.Error as e:
            logging.critical("%s occurred while connecting PostgreSQL Database" % str(e))
    
    def __cursor(self):
        return self.__conn.__cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__conn.commit()
        except pg.Error as e:
            logging.critical("%s occurred, can\'t save data, changes would be reverted" % str(e))
        self.__conn.close()
        
    # TODO: what outcome datatype is needed?
    def get_data(self, user_id):
        with self.__cursor() as cur:
            cur.execute("FROM users_table SELECT * WHERE user_id = %d", (user_id, ))
            return cur.fetchone()

    def get_uid(self):
        with self.__cursor() as cur:
            cur.execute("SELECT max(user_id) from users_table")
            return int(cur.fetchone()[0])

    def get_many(self, user_id_list):
        with self.__cursor() as cur:
            cur.prepare("FROM users_table SELECT * WHERE user_id = %d")
            for user_id in user_id_list:
                cur.execute(user_id)
                return cur.fetchall()
                
    # TODO: update number of values     
    # TODO: should return dict
    def set_data(self, user_dict):
        with self.__cursor() as cur:
            cur.execute("INSERT INTO users_table VALUES (%s, %s, %s, %s)", (user_dict.values()))
            return self.get_uid()

    def update_data(self, user_dict):
        with self.__cursor() as cur:
            id_ = user_dict.pop("id")
            cur.execute("UPDATE users_table SET name = %s, country = %s, value = %s, gdp = %s WHERE user_id = %s",
                        (*[val for val in user_dict.values()], id_))








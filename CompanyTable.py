import allure
from sqlalchemy import create_engine
from sqlalchemy.sql import text

class CompanyTable:
    __scripts = {
        "select": "select * from company where deleted_at is null",
        "select only active": "select * from company where \"is_active\" = true  and deleted_at is null",
        "delete by id": text("delete from company where id =:id_to_delete"),
        "insert new": text("insert into company(\"name\") values (:new_name)"),
        "get max id": "select MAX(\"id\") from company where deleted_at is null",
        "select by id": text("select * from company where id =:select_id and deleted_at is null")
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string).connect()

    @allure.step("БД. Запросить список организаций")
    def get_companies(self):
        query = self.__db.execute(self.__scripts["select"])
        allure.attach(str(query.context.cursor.query), 'SQL', allure.attachment_type.TEXT)
        return query.fetchall()
    
    @allure.step("БД. Запросить список активных организаций")	
    def get_active_companies(self):
        query = self.__db.execute(self.__scripts["select only active"])
        allure.attach(str(query.context.cursor.query), 'SQL', allure.attachment_type.TEXT)
        return query.fetchall()

    @allure.step("БД. Удалить организацию по {id}")
    def delete(self, id):
        params = {'id_to_delete' : id}
        query = self.__db.execute(self.__scripts["delete by id"], parameters = params)
        allure.attach(str(query.context.cursor.query), 'SQL', allure.attachment_type.TEXT)
           
    @allure.step("БД. Создать организацию с названием {name}")
    def create(self, name):
        params = {'new_name' : name}
        query = self.__db.execute(self.__scripts["insert new"], parameters = params)
        allure.attach(str(query.context.cursor.query), 'SQL', allure.attachment_type.TEXT)

    @allure.step("БД. Получить максимальный id организации")
    def get_max_id(self):
        query = self.__db.execute(self.__scripts["get max id"])
        allure.attach(str(query.context.cursor.query), 'SQL', allure.attachment_type.TEXT)
        return query.fetchall()[0][0]
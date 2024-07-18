import allure 
from time import sleep
from CompanyApi import CompanyApi
from CompanyTable import CompanyTable

@allure.epic("компании") 
@allure.severity("blocker")
class CompanyTest:

    api = CompanyApi("https://x-clients-be.onrender.com")
    db = CompanyTable("postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx")

    @allure.id("SKYPRO-1")
    @allure.story("Получение списка компаний")
    @allure.feature("READ")
    @allure.title("Получение полного списка организаций")
    def test_get_companies(self):
        #Шаг1: получить список компаний через API:
        api_result = self.api.get_company_list()
        with allure.step("Получить список компаний из БД"):
        #Шаг2: получить список компаний из БД:
            db_result = self.db.get_companies()
        with allure.step("Сравнить размеры 2х списков"):
        #Шаг2: проверить, что списки равны
            assert len(api_result) == len(db_result)

    @allure.id("SKYPRO-2")
    @allure.story("Получение списка компаний")
    @allure.feature("READ")
    @allure.title("Получение списка активных организаций")
    @allure.description("Запрос организация с параметром active = true")
    # Проверка получения активных компаний
    def test_get_active_companies(self):
        filtered_list = self.api.get_company_list(params_to_add={"is_active": "true"})
        db_list = self.db.get_active_companies()
        assert len(filtered_list) == len(db_list)

    @allure.id("SKYPRO-3")
    @allure.story("Создание компаний")
    @allure.feature("CREATE")
    @allure.title("Создание организации")
    # Проверка добавления новой компании 
    def test_add_new(self):
            body = self.api.get_company_list()
            len_before = len(body)

            name = "Autotest"
            descr = "Descr"   
            result = self.api.create_company(name, descr)
            new_id = result["id"]

            with allure.step("Проверить поля новой организации. Корректно заполнены"):
                for company in body:
                    if company["id"] == new_id:
                        assert company["name"] == name
                        assert company["description"] == descr
                        assert company["id"] == new_id

            
            body = self.api.get_company_list()
            len_after = len(body)

            with allure.step("Проверить, что список ДО меньше списка ПОСЛЕ на 1"):
                assert len_after - len_before == 1

            self.db.delete(new_id)

    @allure.id("SKYPRO-4")  
    @allure.story("Получение компании по id") 
    @allure.feature("UPDATE")  
    @allure.title("Получение организации по id")   
    def test_get_one_company(self):
        #Подготовка
        name = "SkyPro"
        self.db.create(name)
        max_id = self.db.get_max_id()

        #Получение компании
        new_company = self.api.get_company(max_id)

        #Удаление
        self.db.delete(max_id)

        assert new_company["id"] == max_id
        assert new_company["name"] == name
        assert new_company["isActive"] == True

    # @allure.id("SKYPRO-5")
    # def test_edit(): 
    #     #Добавляем в базу компанию с названием SkyPro:
    #     name = "SkyPro"
    #     db.create(name)
    #     max_id = db.get_max_id()
    #     #Меняем описание компании в поле description:
    #     new_name = "Updated"
    #     new_descr = "_upd_"
    #     edited = api.edit(max_id, new_name, new_descr)
    #     # Удаляем компанию:
    #     db.delete(max_id)
    #     assert edited["id"] == max_id
    #     assert edited["name"] == new_name
    #     assert edited["description"] == new_descr
    #     assert edited["isActive"] == True

    # @allure.id("SKYPRO-6")
    # def test_delete():
    #     #Добавили компанию через базу:
    #     name = "SkyPro"
    #     db.create(name)
    #     max_id = db.get_max_id()

    #     #Удалили компанию:
    #     deleted = api.delete(max_id)
    #     deleted = api.delete(max_id)
    #     assert deleted["id"] == max_id
    #     assert deleted["name"] == name
    #     assert deleted["isActive"] == True

    #     #Проверили по ID, что компании нет в базе:
    #     rows = db.get_company_by_id(max_id)
    #     assert len(rows) == 0

    # @allure.id("SKYPRO-7")
    # def test_deactivate():
    #     name = "SkyPro"
    #     db.create(name)
    #     max_id = db.get_max_id()

    #     body = api.set_active_state(max_id, False)

    #     db.delete(max_id)
    #     assert body["isActive"] == False

    # @allure.id("SKYPRO-8")   
    # def test_deactivate_and_activate_back():
    #     name = "SkyPro"
    #     db.create(name)
    #     max_id = db.get_max_id()

    #     api.set_active_state(max_id, False)
    #     body = api.set_active_state(max_id, True)

    #     assert body["isActive"] == True

from CompanyApi import CompanyApi
from CompanyTable import CompanyTable

api = CompanyApi("https://x-clients-be.onrender.com")
db = CompanyTable("postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx")

def test_get_companies():
    #Шаг1: получить список компаний через API:
    api_result = api.get_company_list()

    #Шаг2: получить список компаний из БД:
    db_result = db.get_companies()

    #Шаг2: проверить, что списки равны
    assert len(api_result) == len(db_result)

# Проверка получения активных компаний
def test_get_active_companies():
    filtered_list = api.get_company_list(params_to_add={"is_active": "true"})
    db_list = db.get_active_companies()
    assert len(filtered_list) == len(db_list)

# Проверка добавления новой компании 
def test_add_new():
    body = api.get_company_list()
    len_before = len(body)

    name = "Autotest"
    descr = "Descr"
    result = api.create_company(name, descr)
    new_id = result["id"]

    body = api.get_company_list()
    len_after = len(body)

    db.delete(new_id)

    assert len_after - len_before == 1
    for company in body:
            if company["id"] == new_id:
                assert company["name"] == name
                assert company["description"] == descr
                assert company["id"] == new_id

def test_get_one_company():
    #Подготовка
    name = "SkyPro"
    db.create(name)
    max_id = db.get_max_id()

    #Получение компании
    new_company = api.get_company(max_id)

    #Удаление
    db.delete(max_id)

    assert new_company["id"] == max_id
    assert new_company["name"] == name
    assert new_company["isActive"] == True

def test_edit(): 
    #Добавляем в базу компанию с названием SkyPro:
    name = "SkyPro"
    db.create(name)
    max_id = db.get_max_id()
    #Меняем описание компании в поле description:
    new_name = "Updated"
    new_descr = "_upd_"
    edited = api.edit(max_id, new_name, new_descr)
    # Удаляем компанию:
    db.delete(max_id)
    assert edited["id"] == max_id
    assert edited["name"] == new_name
    assert edited["description"] == new_descr
    assert edited["isActive"] == True

def test_delete():
    #Добавили компанию через базу:
    name = "SkyPro"
    db.create(name)
    max_id = db.get_max_id()

    #Удалили компанию:
    deleted = api.delete(max_id)
    deleted = api.delete(max_id)
    assert deleted["id"] == max_id
    assert deleted["name"] == name
    assert deleted["isActive"] == True

     #Проверили по ID, что компании нет в базе:
    rows = db.get_company_by_id(max_id)
    assert len(rows) == 0

def test_deactivate():
    name = "SkyPro"
    db.create(name)
    max_id = db.get_max_id()

    body = api.set_active_state(max_id, False)

    db.delete(max_id)
    assert body["isActive"] == False
    
def test_deactivate_and_activate_back():
    name = "SkyPro"
    db.create(name)
    max_id = db.get_max_id()

    api.set_active_state(max_id, False)
    body = api.set_active_state(max_id, True)

    assert body["isActive"] == True

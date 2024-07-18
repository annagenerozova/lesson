import allure
import requests

class CompanyApi:
    # Инициализация 
    def __init__(self, url) -> None:
        self.url = url

    @allure.step("api. Получить список компаний через API")
    # Получить список компаний   
    def get_company_list(self, params_to_add=None):
        resp = requests.get(self.url + '/company', params=params_to_add)
        return resp.json()
    
    @allure.step("api. Получить токен авторизации для пользователя {user}:{password}")
    # Получить токен авторизации
    def get_token(self, user='flora', password='nature-fairy'):
        creds = {
            "username": user,
            "password": password
        } 
        resp = requests.post(self.url + '/auth/login', json=creds)
        return resp.json()["userToken"]
    
    @allure.step("api. Получить компанию по {id}")
    def get_company(self, id):
        resp = requests.get(self.url + '/company/' + str(id))
        return resp.json()
    
    @allure.step("api. Создать компанию {name} ({description})")
    # Добавить компанию:
    def create_company(self, name, description=""):
        company = {
            "name": name,
            "description": description
        }
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.post(self.url + '/company',
                             json=company, headers=my_headers)
        return resp.json()

    @allure.step("api. Редактировать компанию {new_id} {new_name}({new_descr})")
    def edit(self, new_id, new_name, new_descr):
        my_headers = {}
        # Авторизуемся как пользователь
        my_headers["x-client-token"] = self.get_token()
        # Вызываем словарь и кладем в него описание компании
        company = {
            "name": new_name,
            "description": new_descr
        }
        # Метод отправляет запрос по URL, передает заголовки и тело
        resp = requests.patch(self.url + '/company/' + str(new_id), headers=my_headers, json=company)
        # Результат вернется в JSON, мы его прокинем в тест
        return resp.json()   
    
    @allure.step("api. Удалить компанию {id}")
    def delete(self, id):
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.get(self.url + '/company/delete/' + str(id), headers=my_headers)
        return resp.json()
    
    @allure.step("api. (Де)активировать компанию{id}->{isActive}")
    def set_active_state(self, id, isActive):
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.patch(self.url + '/company/status/' + str(id),
                              headers=my_headers, json={"isActive": isActive})
        return resp.json()
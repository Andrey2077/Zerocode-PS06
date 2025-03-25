#Код, написанный с использованием новых селекторов.
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://career.habr.com/vacancies?q=backend&type=all"
driver.get(url)
time.sleep(3)

vacancies = driver.find_elements(By.CSS_SELECTOR, 'div.vacancy-card__info')

parsed_data = []

for vacancy in vacancies:
    try:
        title_element = vacancy.find_element(By.CSS_SELECTOR, 'a.vacancy-card__title-link')
        title = title_element.text
        link = title_element.get_attribute('href')
        company = vacancy.find_element(By.CSS_SELECTOR, 'a.link-comp').text
        required_stacks = vacancy.find_element(By.CSS_SELECTOR, 'div.vacancy-card__skills').find_elements(By.CSS_SELECTOR, 'a.link-comp')
        stack =[]

        for required_stacks in required_stacks:
            try:
                stack.append(required_stacks.text)
            except:
                stack.append("Требуемый стэк не указан")

        if len(stack) == 0:
            stack.append("Требуемый стэк не указан")

        try:
            salary = vacancy.find_element(By.CSS_SELECTOR, 'div.basic-salary').text
        except:
            salary = "Не указана"

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

    parsed_data.append([title, company, salary, link, " • ".join(stack)])

driver.quit()

with open("habr.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', ' Название компании', ' Зарплата', ' Ссылка на вакансию', ' Требуемые навыки'])
    writer.writerows(parsed_data)
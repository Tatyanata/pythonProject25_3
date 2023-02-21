import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from setting import cor_email, cor_password

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('c:/python/chromedriver_win32/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    time.sleep(5)
    yield
    pytest.driver.quit()
def test_show_my_pets():
   # Устанавливаем неявное ожидание
    pytest.driver.implicitly_wait(10)
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(cor_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(cor_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.CSS_SELECTOR, 'h1').text == "PetFriends"


    # Нажимаем на кнопку "Мои питомцы"
    pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()
    # проверяем что на стр присутствуют все питомцы.
    row_count = len(pytest.driver.find_elements(By.TAG_NAME, 'tr'))
    my_pet_amount = pytest.driver.find_element(By.XPATH, '(html/body/div[1]/div[1]/div[1])')
    my_pet_amount = my_pet_amount.get_attribute('innerText')
    assert str((row_count) - 1) in my_pet_amount
    print(my_pet_amount)
    images = pytest.driver.find_elements(By.TAG_NAME, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.TAG_NAME, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.TAG_NAME, '.card-deck .card-text')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(",")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

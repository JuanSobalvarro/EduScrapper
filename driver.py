from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://sive.ulsa.edu.ni")

first_chain = "22-A0401-00"
second_chain = 25
iter_num = 30

wait = WebDriverWait(driver, 20)
for i in range(iter_num):
    try:
        # Localizamos la etiqueta asociada al checkbox usando el atributo for
        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='myCheckbox2']")))
        label.click()
    except Exception as e:
        print("Error al hacer clic en la etiqueta:", e)
    finally:
        button = wait.until(EC.element_to_be_clickable((By.ID, "btn1")))
        button.click()
        
        input_text = wait.until(EC.element_to_be_clickable((By.ID, "documentid")))
        input_text.clear()
        input_text.send_keys(first_chain + str(second_chain + i))

        verificar = wait.until(EC.element_to_be_clickable((By.ID, "btn-verificar")))
        verificar.click()
        
        texto = wait.until(EC.visibility_of_element_located((By.ID, "contenedorResponse"))).text
        if "Advertencia" in texto:
            driver.refresh()
        else:
            time.sleep(3)
            driver.refresh()

driver.quit()


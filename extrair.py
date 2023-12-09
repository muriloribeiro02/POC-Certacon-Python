from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import sqlite3

def ExtrairArquivofuncao():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    url = 'https://www.vriconsulting.com.br/guias/guiasIndex.php?idGuia=22'
    driver.get(url)
    driver.implicitly_wait(10)
    table_xpath = '/html/body/section/section[2]/table[1]'
    table = driver.find_element(by=By.XPATH, value=table_xpath)
    html_content = table.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find('tbody').find_all('tr')
    conn = sqlite3.connect('NF.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            N INTEGER,
            Campo TEXT,
            Descricao TEXT,
            Tipo TEXT,
            Tam TEXT,
            Dec TEXT,
            Entr TEXT,
            Saida TEXT
        )
    ''')

    for row in rows:
        columns = row.find_all('td')
        data = [col.get_text(strip=True) for col in columns]

        cursor.execute('''
            INSERT INTO dados (N, Campo, Descricao, Tipo, Tam, Dec, Entr, Saida)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)

    conn.commit()
    conn.close()
    driver.quit()

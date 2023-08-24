import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import pandas as pd
import tkinter as tk
from tkinter import messagebox

with open("config.json", "r") as file:
    config = json.load(file)

servico = Service(ChromeDriverManager().install())

# define o navegador
navegador = webdriver.Chrome()

# maximiza o chome
navegador.maximize_window()
navegador.implicitly_wait = 5

# acessa o Autodoc
navegador.get("https://plataforma.autodoc.com.br/suite")

def pagina_login():

    navegador.get("https://plataforma.autodoc.com.br/login")
    sleep(2.5)

    # clica no local do email e preenche o Email 
    navegador.find_element(By.ID, "email_input").send_keys(config["email"])
    sleep(1.5)

    #clica no botão para acessar o proximo passo que é a senha 
    navegador.find_element(By.CLASS_NAME, "login_continue_btn").click()
    # navegador.find_element('xpath','//*[@id="single-spa-application:mf-login"]/div[2]/div[1]/div/form/button').click()
    sleep(2)

    #clica no botão para preencher a senha  
    navegador.find_element(By.ID, "password_input").send_keys(config["senha"])
    
    #clica no botão para entrar no autodoc
    navegador.find_element(By.XPATH,'//*[@id="single-spa-application:mf-login"]/div[2]/div[1]/div/form/button').click()

def pagina_empresa(id: int, nome: str):

    navegador.get("https://plataforma.autodoc.com.br/suite")
    sleep(1.5)
    navegador.find_element(By.XPATH, '//*[@id="single-spa-application:mf-suite"]/main/section[1]/div[2]/div[1]').click()
    
    element = Select(navegador.find_element(By.ID, "idEscolhaCliente"))

    element.select_by_visible_text(nome)
    # element.select_by_value(str(id))

    navegador.find_element(By.ID, "btnAcessar").click()

    sleep(10)

    logout()

def logout():

    profile = navegador.find_element(By.CLASS_NAME, 'user-profile')
    profile.click()

    sleep(1)
    
    sair = navegador.find_element(By.XPATH, '//*[@id="pcoded"]/div[2]/nav/div/div[2]/ul[2]/li[3]/ul/li[5]/a')
    sair.click() 

    # O roboot Faz o login se passando pelo usuario
pagina_login()

# Roboot inicia a execução em loop de acordo com as tarefas que foram configuradas no arquivo [config.json]
for tarefa in config["tarefas"]:

    sleep(1.5)

    if tarefa["ativo"] == True:

        pagina_empresa(tarefa["id"], tarefa["nome"])
        sleep(3)

navegador.close()
navegador.quit()
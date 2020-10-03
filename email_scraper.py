
"""
@author: Lucas H S
"""
#
# -*- coding: utf-8 -*-
# E-mail extractor for "Institucionalizacao da FAPDF 2019" project
# 

from googlesearch import search
from socket import timeout
import http
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import URLError, HTTPError
import random
import os
import time
import sqlite3
from sqlite3 import Error
import sys
import re
from fake_useragent import UserAgent
from socket import timeout
from urllib.error import HTTPError, URLError

imageExt = ["jpeg", "exif", "tiff", "gif", "bmp", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat", "bpg", "cgm", "svg"]
ua = UserAgent()

count_email_in_phrase = 0

# Menu Principal
def menu():
    	
	global count_email_in_phrase
	count_email_in_phrase = 0

	try:
		clear()       
		print("|\n              E-mail web scrapper                               \n| ")
		print(" ---------------------------")
		print("1 - Procurar apenas na URL inserida")
		print("2 - Buscar na URL em dois niveis")
		print("3 - Buscar frase relacional no google")
		print("4 - Buscar frase com parametro lista de keywords")
		print("5 - Listar email")
		print("6 - Salvar emails encontrados em arquivo .txt")
		print("7 - Apagar email da Base")
		print("8 - Sair")
		print("")

		opcao = input("Escolha uma opcao: ")
		if (opcao == "1"):
			print("")
			print ("")
			url = str(input("Inserir URL: "))
			extractOnlyUrl(url)
			input("Aperte enter para continuar")
			menu()

		if (opcao == "2"):
			print("")
			print ("")
			url = str(input("Inserir URL: "))
			extractUrl(url)
			input("Aperte enter para continuar")
			menu()

		elif (opcao == "3"):
			print("")
			frase = str(input("Inserir frase para iniciar busca: "))
			print ("***Aviso: A quantidade de resultados escolhidos impacta no tempo de execucao***")
			print ("***")
			cantRes = int(input("Numero de resultados no Google: ")) 
			print ("")
			extractFraseGoogle(frase, cantRes)
			input("Aperte enter para continuar")
			menu()

		elif (opcao == "4"):
			#extractKeywordsList("KeywordsList.txt")
			print("Desenvolvendo...")
			input("Aperte enter para continuar")
			menu()
		
		elif (opcao == "5"):
			print ("")
			print ("1 - Selecione uma frase")
			print ("2 - Insira uma URL")
			print ("3 - Todos os emails")
			opcListar = input("Insira uma opcao: ")
			
			if (opcListar == "1"):
				listarPorFrase("Emails.db")

			elif (opcListar == "2"):
				listarPorUrl("Emails.db")

			elif (opcListar == "3"):
				listarTodo("Emails.db")

			else:
				print("Opcao incorretam retorna ao menu...")
				time.sleep(2)
				menu()

		elif (opcao == "6"):
			print("")
			print("1 - Salvar os email das frases")
			print("2 - Salvar emails da URL")
			print("3 - Salvar todos os emails")
			opcGuardar = input("Inserir uma opcao: ")
			
			if(opcGuardar == "1"):
				frase = str(input("Inserir frase: "))
				guardarFrase("Emails.db", frase)
				
			elif(opcGuardar == "2"):
				print("URL Exemplo: https://www.unb.br/")
				url = str(input("Inserir URL: "))
				guardarUrl("Emails.db", url)
				
			elif(opcGuardar == "3"):
				guardarAll("Emails.db")
				
			else:
				print("Opcao incorreta, retornar ao menu")
				time.sleep(2)
				menu()

		elif (opcao == "7"):
			print("")
			print("1 - Deletar email de uma URL especifica")
			print("2 - Deletar email de uma frase especifica")
			print("3 - Deletar todos os emails")
			op = input("Selecione opcao:  ")

			if(op == "1"):
				print("URL de Exemplo: https://www.unb.br/")
				url = str(input("Insert URL: "))
				deleteUrl("Emails.db", url.strip())
			
			elif(op == "2"):
				phrase = str(input("Insert Phrase: "))
				deletePhrase("Emails.db", phrase.strip())

			elif(op == "3"):
				deleteAll("Emails.db")

			else:
				print("Opcao incorreta, retornar ao menu")
				time.sleep(2)
				menu()
		
		elif (opcao == "8"):
			sys.exit(0)

		else:			
			print("")
			print ("Selecione uma opcao valida - Seleccione un opcao correcta")
			time.sleep(3)
			clear()
			menu()
	
	except KeyboardInterrupt:
		input("Aperte return  para continuar")
		menu()

	except Exception as e:
		print (e)
		input("Aperte enter para continuar")
		menu()

# Inserir endereco, frase e URL na base dados 
def insertEmail(db_file, email, frase, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		c.execute("INSERT INTO emails (phrase, email, url) VALUES (?,?,?)", (frase, email, url))
		conn.commit()
		conn.close()

	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()

	finally:
		conn.close()

# Buscar email na base de dados
def searchEmail(db_file, email, frase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails where email LIKE "%' + str(email) + '%" AND phrase LIKE "%' + str(frase) + '%"'
		result = c.execute(sql).fetchone()
		conn.close()

		return (result[0])

	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()

	finally:
		conn.close()

# Cria tabela principal	
def crearTabla(db_file, delete = False):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		if(delete == True):
			c.execute('drop table if exists emails')			

		sql = '''create table if not exists emails 
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				 phrase varchar(500) NOT NULL,
				 email varchar(200) NOT NULL,
				 url varchar(500) NOT NULL)'''

		c.execute(sql)
		conn.close()

	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()

	finally:
		conn.close()

# Guardar por URL em um arquivo .txt
def guardarUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = "' + url.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("Nao existem emails para apagar")
			input("Aperte enter para continuar")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE url = "' + url.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Aperte enter para continuar")
		menu()
		
	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
	except Exception as o:
		print(o)
		input("Aperte enter para continuar")
		menu()
		
	finally:
		conn.close()

# Guardar por frase em um arquivo .txt
def guardarFrase(db_file, frase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = "' + frase.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("Nao existem emails para apagar")
			input("Aperte enter para continuar")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE phrase = "' + frase.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Aperte enter para continuar")
		menu()
			
	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
	except Exception as o:
		print(o)
		input("Aperte enter para continuar")
		menu()
		
	finally:
		conn.close()

# Guarda todos os emails em um arquivo .txt
def guardarAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("Nao existem emails para apagar")
			input("Aperte enter para continuar")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile + ".txt", "w")
		
			c.execute('SELECT * FROM emails')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		
		input("Aperte enter para continuar")
		menu()
		
	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
	except Exception as o:
		print(o)
		input("Aperte enter para continuar")
		menu()
		
	finally:
		conn.close()

# Apaga todos os emails de uma URL especifica
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = ' + '"' + url + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("Nao existem emails para apagar")
			input("Aperte enter para continuar")
			menu()
			
		else:
			option = str(input("Voce tem certeza que quer deletar " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE url = " + '"' + url + '"')
				conn.commit()

				print("Emails deletados")
				input("Aperte enter para continuar")
				menu()
				
			elif(option == "N" or option == "n"):
				print("Operacao cancelada, retornar ao menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Selecione uma opcao valida")
				time.sleep(2)
				deleteUrl(db_file, url)
				
		conn.close()
		
	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
	finally:
		conn.close()

# Apaga todos os emails de uma frase especifica
def deletePhrase(db_file, phrase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = ' + '"' + phrase + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("Nao existem emails para apagar")
			input("Aperte enter para continuar")
			menu()
			
		else:
			option = str(input("Voce tem certeza que quer deletar " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE phrase = " + '"' + phrase + '"')
				conn.commit()

				print("Emails deletados")
				input("Aperte enter para continuar")
				menu()
				
			elif(option == "N" or option == "n"):
				print("Operacao cancelada, retornar ao menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Selecione uma opcao valida")
				time.sleep(2)
				deleteUrl(db_file, phrase)
				
		conn.close()
				
	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
	finally:
		conn.close()

# Apaga todos os emails 
def deleteAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("Nao existem emails para apagar")
			input("Aperte enter para continuar")
			menu()
		
		
		else:			
			option = str(input("Voce tem certeza que quer deletar " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails")
				conn.commit()
				crearTabla("Emails.db", True)
				print("All emails were deleted")
				input("Aperte enter para continuar")
				menu()

			elif(option == "N" or option == "n"):
				print("Operacao cancelada, retornar ao menu ...")
				time.sleep(2)
				menu()

			else:
				print("Selecione uma opcao valida")
				time.sleep(2)
				deleteAll(db_file)
				
		conn.close()

	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()

	finally:
		conn.close()

# Listar emails por frase
def listarPorFrase(db_file):
	try:
		phrase = str(input("Inserir frase: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("Sem resultados para a URL especificada")
				input("Aperte enter para continuar")
				menu()
				
		else:
			c.execute('SELECT * FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Pressione enter para continuar")
		menu()
		
	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
	
	finally:
		conn.close()

# Lista correos por URL
def listarPorUrl(db_file):
	try:
		print("URL de Exemplo: https://www.unb.br/ ")
		url = str(input("Insert a Url: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails WHERE url LIKE "%' + url.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("Sem resultados para a URL especificada")
				input("Aperte enter para continuar")
				menu()

		else:
			c.execute('SELECT * FROM emails WHERE url LIKE "%' + url.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Pressione enter para continuar")
		menu()

	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
	finally:
		conn.close()

# Lista todos los correos
def listarTodo(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("A base de dados esta vazia")
			input("Aperte enter para continuar")
			menu()

		c.execute("SELECT * FROM emails")

		for i in c:

			print ("")
			print ("Number: " + str(i[0]))
			print ("Phrase: " + str(i[1]))
			print ("Email: " + str(i[2]))
			print ("Url: " + str(i[3]))
			print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Pressione enter para continuar")
		menu()

	except Error as e:
		print(e)
		input("Aperte enter para continuar")
		menu()

	finally:
		conn.close()

# Extrae los correos de una única URL
def extractOnlyUrl(url):
	try:
		print ("Procurando emails...Aguarde")

		count = 0
		listUrl = []

		req = urllib.request.Request(
    			url, 
    			data=None, 
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
    			raise ValueError('Bad Url...')


		html = conn.read().decode('utf-8')

		emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)

		for email in emails:
			if (email not in listUrl and email[-3:] not in imageExt):
				count += 1
				print(str(count) + " - " + email)
				listUrl.append(email)
				if(searchEmail("Emails.db", email, "Especific Search") == 0):
					insertEmail("Emails.db", email, "Especific Search", url)

		print("")
		print("***********************")
		print(str(count) + " emails foram encontrados")
		print("***********************")

	except KeyboardInterrupt:
		input("Aperte return  para continuar")
		menu()

	except Exception as e:
		print (e)
		input("Aperte enter para continuar")
		menu()

# Extrae los correos de una Url - 2 niveles
def extractUrl(url):
	print ("Procurando emails...Aguarde")
	print ("Esta operacao pode demorar varios minutos")
	try:
		count = 0
		listUrl = []
		req = urllib.request.Request(
    			url, 
    			data=None, 
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
    			raise ValueError('Bad Url...')

		html = conn.read().decode('utf-8')
		
		emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)
		print ("Procurando em " + url)
		
		for email in emails:
			if (email not in listUrl and email[-3:] not in imageExt):
					count += 1
					print(str(count) + " - " + email)
					listUrl.append(email)

		soup = BeautifulSoup(html, "lxml")
		links = soup.find_all('a')

		print("Serao analizados " + str(len(links) + 1) + " Urls..." )
		time.sleep(2)

		for tag in links:
			link = tag.get('href', None)
			if link is not None:
				try:
					print ("Procurando em " + link)
					if(link[0:4] == 'http'):
						req = urllib.request.Request(
							link, 
							data=None, 
							headers={
							'User-Agent': ua.random
							})

						try:
							f = urllib.request.urlopen(req, timeout=10)

						except timeout:
							print("Bad Url..")
							time.sleep(2)
							pass

						except (HTTPError, URLError):
							print("Bad Url..")
							time.sleep(2)
							pass

						status = f.getcode()
						contentType = f.info().get_content_type()

						if(status != 200 or contentType == "audio/mpeg"):
							print("Bad Url..")
							time.sleep(2)
							pass
						
						s = f.read().decode('utf-8')

						emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)

						for email in emails:
							if (email not in listUrl and email[-3:] not in imageExt):
								count += 1
								print(str(count) + " - " + email)
								listUrl.append(email)
								if(searchEmail("Emails.db", email, "Especific Search") == 0):
									insertEmail("Emails.db", email, "Especific Search", url)

				# Sigue si existe algun error
				except Exception:
					pass
		
		print("")
		print("***********************")
		print("Finish: " + str(count) + " emails foram encontrados")
		print("***********************")
		input("Aperte return  para continuar")
		menu()

	except KeyboardInterrupt:
		input("Aperte return  para continuar")
		menu()

	except Exception as e:
		print(e)
		input("Aperte enter para continuar")
		menu()

# Extrai os emails de todas as URLs encontradas na busca
# De cada Url extrai os emails - 2 niveis de busca 
def extractFraseGoogle(frase, cantRes):
	print ("Procurando emails...Aguarde")
	print ("Esta operacao pode demorar varios minutos")
	try:
		listUrl = []
		listEmails = []

		for url in search(frase, stop=cantRes):
			listUrl.append(url)

		for i in listUrl:
			try:
				req = urllib.request.Request(
							i, 
							data=None, 
							headers={
							'User-Agent': ua.random
							})
				try:
					conn = urllib.request.urlopen(req)
				except timeout:
					print("Bad Url..")
					time.sleep(2)
					pass
				except(HTTPError, URLError):
					print("Bad Url..")
					time.sleep(2)
					pass

				status = conn.getcode()
				contentType = conn.info().get_content_type()

				if(status != 200 or contentType == "audio/mpeg"):
					print("Bad Url..")
					time.sleep(2)
					pass

				html = conn.read()

				soup = BeautifulSoup(html, "lxml")
				links = soup.find_all('a')

				print("Serao analizados " + str(len(links) + 1) + " Urls..." )
				time.sleep(2)

				for tag in links:
					link = tag.get('href', None)
					if link is not None:
    					# Fix TimeOut
						searchSpecificLink(link, listEmails, frase)
		
			except urllib.error.URLError as e:
				print("Problems with the url:" + i)
				print(e)
				pass
			except (http.client.IncompleteRead) as e:
				print(e)
				pass
			except Exception as e:
				print(e)
				pass
		
		print("")
		print("*******")
		print("Finish")
		print("*******")
		input("Aperte return  para continuar")
		menu()

	except KeyboardInterrupt:
		input("Aperte return  para continuar")
		menu()

	except Exception as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
		
# Extrair lista de palavras chave de .txt 
def extractKeywordsList(txtFile):
	f = open(txtFile, 'r')
	text = f.read()
	keywordList = text.split(sep='\n')
	for key in keywordList:
    		print(key)



# Clear screen na tela conforme o sistema operacional
def clear():
	try:
		if os.name == "posix":
			os.system("clear")
		elif os.name == "ce" or os.name == "nt" or os.name == "dos":
			os.system("cls")
	except Exception as e:
		print(e)
		input("Aperte enter para continuar")
		menu()
   
def searchSpecificLink(link, listEmails, frase):
	try:

		global count_email_in_phrase

		print ("Procurando em " + link)
		if(link[0:4] == 'http'):
			f = urllib.request.urlopen(link, timeout=10)
			s = f.read().decode('utf-8')
			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
			for email in emails:
				if (email not in listEmails):
					count_email_in_phrase += 1
					listEmails.append(email)
					print(str(count_email_in_phrase) + " - " + email)										
					if (searchEmail("Emails.db", email, frase) == 0):
						insertEmail("Emails.db", email, frase, link)
						
	# Segue caso ocorram errros 
	except (HTTPError, URLError) as e:
		print(e)
		pass
	except timeout:
		print('socket timed out - URL %s', link)
		pass
	except (http.client.IncompleteRead) as e:
		print(e)
		pass
	except Exception as e:
		print(e)
		pass

# Inicio do Programa
def Main():
	clear()
	crearTabla("Emails.db", False)	
	menu()

Main()
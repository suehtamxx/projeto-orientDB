import csv
import random
from faker import Faker

fake = Faker('pt_BR')

<<<<<<< HEAD
qtd_pessoas = 10
qtd_empresas = 5
qtd_relacoes = 20
=======
qtd_pessoas = 100000
qtd_empresas = 10000
qtd_relacoes = 1000000 
>>>>>>> origin/Caio-Branch

pessoas_id = []

with open('data/pessoas.csv', 'w', newline='', encoding='utf-8') as f:
	'''Função para gerar o arquivo de pessoas'''
	writer = csv.writer(f)
	writer.writerow(['id','nome','cidade',])
	for i in range(qtd_pessoas):
		id_pessoa = f'p{i}'
		pessoas_id.append(id_pessoa)

		writer.writerow([id_pessoa, fake.name(), fake.city()])

empresas_id = []
with open('data/empresas.csv', 'w', newline='', encoding='utf-8') as f:
	'''Função para gerar o arquivo de empresas'''
	writer = csv.writer(f)
	writer.writerow(['id','nome_empresa'])
	for i in range(qtd_empresas):
		id_empresa = f'e{i}'
		empresas_id.append(id_empresa)
		writer.writerow([id_empresa, fake.company()])

with open('data/relacoes.csv', 'w', newline='', encoding='utf-8') as f:
	'''Função para gerar o arquivo de relacoes'''
	writer = csv.writer(f)
	writer.writerow(['id_pessoa','id_empresa'])
	for i in range(qtd_relacoes):
		id_pessoa = random.choice(pessoas_id)
		id_empresa = random.choice(empresas_id)
		writer.writerow([id_pessoa, id_empresa])

print('Arquivos CSV gerados\n')
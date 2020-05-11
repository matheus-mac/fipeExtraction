import requests, json, time, csv
start_time = time.time()

#Buscando as marcas dos caminhões disponíveis
r = requests.get('http://fipeapi.appspot.com/api/1/caminhoes/marcas.json')
marcasCaminhoes = json.loads(r.text)

#Buscando modelos das marcas encontradas
modelosDaMarca = []

print("Foram encontradas  %s marcas" % len(marcasCaminhoes))
with open("extracaoFipe.csv", 'w', newline='') as file:
	writer = csv.writer(file)
	i = 0
	for marca in marcasCaminhoes:
		print("Marca {0} de {1}".format(marcasCaminhoes.index(marca)+1,len(marcasCaminhoes)))
		requestModelos = requests.get('http://fipeapi.appspot.com/api/1/caminhoes/veiculos/' + str(marca['id']) +'.json')
		try:
			modelosDaMarca = json.loads(requestModelos.text)
		except:
			print("Erro nos modelos")
		print("Foram encontrads {0} modelos da marca {1}".format(len(modelosDaMarca), marca['fipe_name']))
		anoDosModelos = []
		for modelo in modelosDaMarca:
			print("Modelo {0} de {1}".format(modelosDaMarca.index(modelo)+1, len(modelosDaMarca)))
			try:
				requestAnoData = requests.get('http://fipeapi.appspot.com/api/1/caminhoes/veiculo/' + str(marca['id']) +'/'+ str(modelo['id']) +'.json')
			except:
				print("Erro nos anos")
			anoDosModelos = json.loads(requestAnoData.text)
			for anoModelo in anoDosModelos:
				try:
					requestVeiculo = requests.get('http://fipeapi.appspot.com/api/1/caminhoes/veiculo/' + str(marca['id']) +'/'+ str(modelo['id']) + '/'+ str(anoModelo['id']) +'.json')
				except:
					print (requestVeiculo.text)
					
				try:
					#print(requestVeiculo.text)
					try:
						veiculo = json.loads(requestVeiculo.text)
					except:
						print(requestVeiculo.text)
						print('http://fipeapi.appspot.com/api/1/caminhoes/veiculo/' + str(marca['id']) +'/'+ str(modelo['id']) + '/'+ str(anoModelo['id']) +'.json')
						print("Erro no veiculo")
					
					if i==0:
						print("Foram encontrados {0} datas do modelo {1}".format(len(anoDosModelos), anoModelo['veiculo']))
						for key in veiculo.keys():
							file.write(str(key) + ";")
						file.write('\n')
					else:	
						for value in veiculo.values():
							file.write(str(value) + ";")
						file.write('\n')
				except:
					print(requestVeiculo.text + '\n http://fipeapi.appspot.com/api/1/caminhoes/veiculo/' + str(marca['id']) +'/'+ str(modelo['id']) + '/'+ str(anoModelo['id']) +'.json')
				i = i+1
				time.sleep(1)
print("--- %s seconds ---" % (time.time() - start_time))

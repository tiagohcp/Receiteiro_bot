from getAPI import *
ultima = '0'

def converte(item): #Busca a receita solicitada e converte para uma String formatada
    receitas = getRecipe(item)
    
    resultado = []
    resultado.append("Autor: "+receitas['publisher'])
    resultado.append("Receita: "+receitas['title'])
    resultado.append("Avaliação: "+receitas['social_rank'])
    resultado.append("ID: "+receitas['recipe_id'])
    resultado.append("Ingredientes: "+receitas['ingredients']+".")
    resultado.append("Modo de Preparo: "+receitas['source_url'])
        
    #Formatação da mensagem que será exibida no bot
    string = ""
    for i in resultado:
        string += i + "\n"
    return [string, receitas['image_url']]
    
  
def converteLista(item, cont): #Busca o ingrediente informado e Converte para uma String formatada
    global ultima
    receitas = getListOfRecipes(item, cont)

    if receitas == 0:
        return [0, 0, 0]
    else:
    #Seleciona apenas receitas com ID numéricos
        while True:
            try:
                index = int(receitas['recipe_id'])
                #break
            except ValueError as ex:
                receitas = getListOfRecipes(item, cont)

            if ultima == receitas['recipe_id']:
                return [1, 1]
            ultima = 0
            ultima = receitas['recipe_id']
            
            resultado = []
            foto = ""
            qtd = 0
            
            resultado.append("Autor: "+receitas['publisher'])
            resultado.append("Receita: "+receitas['title'])
            resultado.append("Avaliação: "+receitas['social_rank'])
            resultado.append("ID: /id_"+receitas['recipe_id'])
            foto = receitas['image_url']
            qtd = receitas['qtd']
            #Formatação da mensagem que será exibida no bot
            string = ""
            
            for i in resultado:
                string += i + "\n"
            return [string, foto, qtd]






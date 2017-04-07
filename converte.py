from getAPI import *

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
    
  
def converteLista(item): #Busca o ingrediente informado e Converte para uma String formatada
    receitas = getListOfRecipes(item)

    #Seleciona apenas receitas com ID numéricos
    while True:
        try:
            index = int(receitas['recipe_id'])
            break
        except ValueError as ex:
            receitas = getListOfRecipes(item)

    resultado = []
    resultado.append("Autor: "+receitas['publisher'])
    resultado.append("Receita: "+receitas['title'])
    resultado.append("Avaliação: "+receitas['social_rank'])
    resultado.append("ID: /id_"+receitas['recipe_id'])
    foto = getRecipe(receitas['recipe_id'])
    

    #Formatação da mensagem que será exibida no bot
    string = ""
    for i in resultado:
        string += i + "\n"
    return [string, foto['image_url']]



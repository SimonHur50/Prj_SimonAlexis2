
import os
import xmlrpc.client
import base64
import tkinter as tk 
import time
# from PIL  import Image, ImageTk

from Info_connection import ip_v4 ,url ,db ,username ,password , uid
from opcua import Client

from opcua import ua
import CODE_PING


# NOM des variable
Name_ROUGE = "[P_002] Piece Rouge"
Name_BLEU  = "[P_003] Piece Bleue"
Name_VERT  = '[P_004] Piece verte'


#url = "opc.tcp://172.31.10.226:4840"

#VAriable OPC UA
#CODE_COULEUR_OPCUA = 0
#QUANTITE_OPCUA = 0
MOT_DE_VIE_OPCUA = 0
COMPTEUR_OPCUA = 0 




#=======================================================================
### FONCTION ###################
def Connection_SERVEUR_Odoo ():


    # Connection au serveur Odoo
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
   
    # Authentification
    uid = common.authenticate(db, username, password, {})
   
    while not uid :
        # Authentification
        uid = common.authenticate(db, username, password, {})


        # Vérification de la connexion
        
        if uid:
            print("Connexion réussie avec l'utilisateur %s (ID : %d)" % (username, uid))
            print('I m connected')
        else:
            print("Echec de la connexion")
            print (' Je suis plus co blaireau ')


    # RECUPERATION VERSION DE ODOO
    version = common.version()
    print('ODOO Version :',version['server_serie']) 
    
    return uid
        
def Recherhce_Article ():

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # RECHERCHE DE DATA    
    product_template_ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[]])
    print("Nombre d'article :",product_template_ids)


    #Lecture des article 
    Donnee_Article = models.execute_kw(db, uid, password, 'product.template', 'read', [product_template_ids],{'fields': ['name', 'list_price']})
    
    #Affichage des ID/ NOM et Prix pour tout les produits
    for Num_Of_Product in range(len(Donnee_Article)):
        print("List of product:",Donnee_Article[Num_Of_Product])

def Recherche_Ordre_fabrication ():



    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
      # RECHERCHE DE DATA    
    data = models.execute_kw(db, uid, password, 'mrp.production', 'read', [[2]])
    print(data)  
    
    
    #RECHERCHE DES ID    
    fields1 = ['id']
    data1 = models.execute_kw(db, uid, password, 'mrp.production', 'search_read',[],{'fields': fields1} )
    print("Valeur de ID actuelle :" ,data1[0]['id'])
    
    


    # ID de l'ordre de fabrication à lire
    fields = ['name', 'product_qty', 'id', 'product_id']
    order_id = 2 
    order = models.execute_kw(db, uid, password, 'mrp.production', 'read', [[data1[0]['id']]], {'fields': fields})




    # Extraction des informations
    order_name = order[0]['name']
    order_id = order[0]['id']
    order_Article = order[0]['product_id']
    order_Article_NAME = order_Article[1]
    
    # Affichage des informations récupérées
    print("ID de l'ordre de fabrication :", order_id)
    print("Nom de l'ordre de fabrication :", order_name)
    
    print("Type de l'article :", order_Article)
    print("Nom de la Piece :", order_Article_NAME)
    
    
    
    
    
    
    
    # Extraction QUANTITE
    QUANTITE_OPCUA = int(order[0]['product_qty'])

       
    # Choix CODE COULEUR
    if order_Article_NAME == Name_ROUGE  :
        CODE_COULEUR_OPCUA = 1
    elif order_Article_NAME == Name_BLEU :
        CODE_COULEUR_OPCUA = 2
    elif order_Article_NAME ==  Name_VERT :
        CODE_COULEUR_OPCUA = 0
    else :
        CODE_COULEUR_OPCUA = 0
     
         
    print ("Choix code couleur  :" , CODE_COULEUR_OPCUA)
    print("Quantité de l'ordre de fabrication :", QUANTITE_OPCUA)
    
    return CODE_COULEUR_OPCUA, QUANTITE_OPCUA
    
   

    
def LECTURE_OPC_UA (NODE_ID,New_Read_Value):
    
    url = "opc.tcp://10.10.0.100:4840"
    client = Client(url)
    
   
    connected = False

    while not connected:
        try:
            client.connect()
            connected = True
            print("Connexion réussie au serveur OPC UA")
              
                
            ####### LECTURE ########

        
            compteur_node = client.get_node(NODE_ID)
            New_Read_Value = compteur_node.get_value() 
            print(New_Read_Value)
         
            print("Valeurs écrites avec succès.")
         
        
        
        except Exception as e:
            print("Erreur lors de la connexion au serveur OPC UA:", str(e))
        finally:
            # Déconnexion du serveur OPC UA
            print("Deconnexion de l'OPC UA")
            client.disconnect()
            
        
def ECRITURE_OPC_UA (NODE_ID, New_Write_Value):     
        
    url = "opc.tcp://10.10.0.100:4840"
    #url = "opc.tcp://172.31.10.226:4840"
    client = Client(url)

    connected = False

    while not connected:
        try:
            client.connect()
            connected = True
            print("Connexion réussie au serveur OPC UA")


            ####### ECRITURE ######## 
            
            code_couleur_node2 = client.get_node(NODE_ID)
            
            value =code_couleur_node2.get_value()
            print(" holla ",code_couleur_node2)
            print(" holla ",value)
            
            code_couleur_node2.set_attribute(ua.AttributeIds.Value, ua.DataValue(ua.Variant(New_Write_Value, ua.VariantType.UInt16)))
            value =code_couleur_node2.get_value()

            print(" Ecriture fini ",value)
            
            
        except Exception as e:
            print("Erreur lors de la connexion au serveur OPC UA:", str(e))
       # finally:
            # Déconnexion du serveur OPC UA
           # print("Deconnexion de l'OPC UA")
           # client.disconnect()
        
        
    
    
#=======================================================================
### MAIN  #######################
if __name__ == '__main__':

    uid = Connection_SERVEUR_Odoo () 
    Recherhce_Article()
    while True :
        Resultat = Recherche_Ordre_fabrication()
        CODE_COULEUR_OPCUA = Resultat[0]
        QUANTITE_OPCUA = Resultat[1]
        print ("Choix code couleur  :" , CODE_COULEUR_OPCUA)
        print("Quantité de l'ordre de fabrication :", QUANTITE_OPCUA)
        ECRITURE_OPC_UA ("ns=2;s=Local HMI.Tags.CODE_COULEUR_OPCUA", CODE_COULEUR_OPCUA )
        ECRITURE_OPC_UA ("ns=2;s=Local HMI.Tags.QUANTITE_OPCUA", QUANTITE_OPCUA)
        #ECRITURE_OPC_UA ("ns=2;s=Local HMI.Tags.Int 1", CODE_COULEUR_OPCUA)
        #ECRITURE_OPC_UA ("ns=2;s=Local HMI.Tags.Int 1", QUANTITE_OPCUA)

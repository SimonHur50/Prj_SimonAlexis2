
import xmlrpc.client

from Info_connection import ip_v4 ,url ,db ,username ,password
import CODE_PING
import Connection_Odoo
from Connection_Odoo import uid

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# RECUPERATION DE DATA
#Recuperation des Numero de company
model_name = 'res.company'
Num_partners = models.execute_kw(db, uid, password, model_name, 'search', [[]])
print('/n' ,"List of partners:", Num_partners)

# recuperation de toute la data     sur un Numéro de company
domain = [Num_partners [2] ]

partners = models.execute_kw(db, uid, password, model_name, 'read', [domain])
# print("Partner details:", partners)
print(partners[0]['id'])
print(partners[0]['name'])
print(partners[0]['phone'])
print(partners[0]['street'] ,partners[0]['zip'] ,partners[0]['city'] )
print(partners[0]['website'])


# Change = models.execute_kw(db, uid, password, model_name, 'write', [Num_partners [2] ,{'name':'UIMM'}])
'''
# recuperation de l'ID et du NAME    sur un Numéro de company
Name_partner = models.execute_kw(db, uid, password, model_name, 'read', [domain],{'fields':['name']})
print("Partner details:", Name_partner)
'''

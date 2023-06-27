

import xmlrpc.client
from Info_connection import ip_v4 ,url ,db ,username ,password

def Connection_SERVEUR_Odoo ():

    # Connection au serveur Odoo
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

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

if __name__ == '__main__':
    Connection_SERVEUR_Odoo ()

    
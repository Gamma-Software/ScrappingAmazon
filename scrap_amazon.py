from bs4 import BeautifulSoup
import requests
import argparse


def get_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "DNT": "1", "Connection":"close", "Upgrade-Insecure-Requests": "1"}

    # On chope le code source du site
    r = requests.get(url, headers=headers)

    # On le traduit pour mieux recuperer les donnees
    soup = BeautifulSoup(r.content, "html.parser")

    # On cherche l'element qui nous interesse
    element = soup.find('span', attrs={'class': 'prix mr-10 text-black text-bold'})

    # Si on la trouve
    if element is not None:
        # On affiche la valeur du l'element
        print(element.text)

        # On sait que c'est un prix et que c'est une chaine de caractere alors on supprime le signe
        # Euro et on replace la virgule par un point pour transformer la chaine de caract en decimale (float)
        return float(element.text.strip("€").replace(",", "."))

    # Sinon on met un chiffre par defaut nulle
    return 0.


def append_price_to_file(value, file_name):
    # On creer le fichier ou s'il existe on ouvre le fichier et on demande d'ecrire a la suite
    f = open(file_name, "a")
    # On ecrit a la suite
    f.write(str(value) + "\n")
    # On ferme le fichier
    f.close()

# Conversion des parametres du script
parser = argparse.ArgumentParser(description='Scrap amazon prices')
parser.add_argument('-u', '--url', help='Url to scrap', type=str)
parser.add_argument('-f', '--filename', help='Filename to write the price to', type=str)
args = parser.parse_args()

print("Start script")
price = get_data(args.url) # On recupere le prix du livre dans l'url fourni
append_price_to_file(price, args.filename) # On ajoute le prix du livre dans le fichier qu'on souhaite
print("End of script")

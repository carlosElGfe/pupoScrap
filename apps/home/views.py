# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from json import JSONDecodeError
import csv  
from django.template import loader
from django.urls import reverse
import requests
import re
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import producto



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    info = []
    if request.method=='POST':
        if request.POST.get("id_prod"):
            product_id = request.POST.get("product_id")
            html = requests.get(url = 'https://www.lider.cl/supermercado/product/'+product_id).text
            #print(html)
            soup = BeautifulSoup(html, 'html.parser')
            description = soup.select_one('span.product-descript').text.strip()
            context['descripcion'] = description
            price = soup.select('p')
            span = soup.select('span')
            for s in span:
                print(s.text.strip())
                #[t.text for t in soup.select('[id$="_lblCodigo"]')] extraer con ese id
            caracteristicas = soup.select('div.certificate')
            
            # print(soup.select_one('p.section_text').text.strip())
            context['img_src'] = 'https://images.lider.cl/wmtcl?source=url[file:/productos/'+product_id+'a.jpg]&sink'
            context['price'] = price[4].text.strip()
            context['price_gram'] = price[5].text.strip()
        if request.POST.get("search"):
            words = request.POST.get("query")
            words = words.split(" ")
            string2 = "&ost="
            string = "https://www.lider.cl/supermercado/search?Ntt="
            for i in words:
                string+=i
                string+="%20"
                string2+=i
                string2+="%20"
            string = string[:-3]
            string2 = string2[:-3]
            string += string2
            r = requests.post(url = string).text
            soup = BeautifulSoup(r,'html.parser')
            codes = soup.select('span.reference-code')
            context['codes'] = [i.text.strip() for i in codes]
            internal = []
            for link in soup.find_all('a', attrs={'href': re.compile("^/")}):
                if 'product' in str(link.get('href')):
                    internal.append(link.get('href').split("/")[3]+"__Code__:"+link.get('href').split("/")[4])
            internal = list(dict.fromkeys(internal))
            context['internal'] = internal
        if request.POST.get("rappi"):
            producto.objects.all().delete()
            keywords = ['desayuno/cereales',
                        'frutas-y-verduras/frutas',
                        'frutas-y-verduras/ensaladas',
                        'frutas-y-verduras/hierbas-y-aromaticas',
                        'pollos-y-carnes/carnes',
                        'pollos-y-carnes/pollo-y-aves',
                        'pollos-y-carnes/cerdo',
                        'cuidado-personal/higiene',
                        'cuidado-personal/cuidado-oral',
                        'cuidado-personal/cuidado-del-cabello',
                        'cuidado-personal/cuidado-corporal',
                        'cuidado-personal/desodorantes',
                        'cuidado-personal/toallas-protectoras',
                        'cuidado-personal/depilacion-y-afeitado',
                        'cuidado-personal/farmacia',
                        'jamones-y-embutidos/embutidos',
                        'jamones-y-embutidos/jamones',
                        'panaderia-y-pasteleria/masas-dulces',
                        'panaderia-y-pasteleria/panes',
                        'panaderia-y-pasteleria/reposteria',
                        'panaderia-y-pasteleria/tortillas',
                        'desayuno/avena-y-granola',
                        'desayuno/barras-de-cereal',
                        'desayuno/mermelada-manjar-y-mas',
                        'desayuno/cafe',
                        'desayuno/te',
                        'desayuno/mate',
                        'desayuno/modificadores-de-leche',
                        'lacteos/bebidas-vegetales',
                        'lacteos/leches',
                        'lacteos/yogurt-y-bebidas-lacteas',
                        'lacteos/crema-de-leche',
                        'lacteos/quesos',
                        'lacteos/mantequillas',
                        'huevos',
                        'papeleria-y-oficina',
                        'congelados/verduras-congeladas',
                        'congelados/carnes-congeladas',
                        'congelados/listo-para-cocinar',
                        'congelados/platos-preparados',
                        'congelados/helados',
                        'congelados/hielo',
                        'despensa/pastas-y-masas',
                        'despensa/arroz-quinoa-y-cuscus',
                        'despensa/legumbres',
                        'despensa/harina-y-mezclas-para-preparar',
                        'despensa/aceites-y-vinagres',
                        'despensa/azucar-y-endulzantes',
                        'despensa/pescado-enlatado',
                        'despensa/conservas',
                        'despensa/ketchup',
                        'despensa/sal',
                        'despensa/otras-salsas',
                        'snacks-y-confiteria/colaciones',
                        'snacks-y-confiteria/frutos-secos',
                        'snacks-y-confiteria/dulces-y-chicles',
                        'snacks-y-confiteria/snacks-dulces',
                        'snacks-y-confiteria/galletas-dulces',
                        'snacks-y-confiteria/galletas-saladas',
                        'snacks-y-confiteria/chocolates',
                        'snacks-y-confiteria/papas-fritas-y-snacks',
                        'limpieza-del-hogar/detergente-de-ropa',
                        'limpieza-del-hogar/cuidado-de-la-ropa',
                        'limpieza-del-hogar/limpiadores',
                        'limpieza-del-hogar/ambientadores',
                        'limpieza-del-hogar/desinfectantes',
                        'limpieza-del-hogar/esponjas-y-panos',
                        'limpieza-del-hogar/bolsas-de-basura',
                        'limpieza-del-hogar/papel-aluminio',
                        'limpieza-del-hogar/insecticidas',
                        'limpieza-del-hogar/limpiavidrios',
                        'limpieza-del-hogar/lustramuebles',
                        'listo-para-comer/sandwiches-y-wraps',
                        'listo-para-comer/sushi',
                        'listo-para-comer/postres-sin-azucar',
                        'listo-para-comer/postres',
                        'listo-para-comer/bebestibles',
                        'listo-para-cocinar/pizza-y-empanadas',
                        'listo-para-cocinar/postres',
                        'buenos-dias/panaderia-y-dulces',
                        'buenos-dias/quesos-y-fiambres',
                        'emergencias']
            base = 'https://www.rappi.cl/tiendas/900066624-turbo-market-las-condes/'
            
            with open('rappi_turbo_data.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                            'Nombre',
                            'medida',
                            'Precio'
                                    ])
                for i in keywords:
                    base_url = base +i
                    print(base_url)
                    html = requests.get(url = base_url).text
                    soup = BeautifulSoup(html, 'html.parser')
                    results_certificate_elements = [t for t in soup.select('[class$="jIFSBW"]')]
                    for t in results_certificate_elements:
                        try:
                            producto.objects.create(
                                nombre = t.find('h4').text,
                                medida = t.find_all('span')[0].text,
                                precio = t.find_all('span')[1].text
                            )
                            dta = [t.find('h4').text,t.find_all('span')[0].text,t.find_all('span')[1].text]
                            print(dta)
                            writer.writerow(dta)
                            print("producto creado")    
                        except Exception:
                            producto.objects.create(
                                nombre = t.find('h4').text,
                                medida = t.find_all('span')[0].text,
                                precio = t.find_all('span')[0].text
                            )
                            dta = [t.find('h4').text,t.find_all('span')[0].text,t.find_all('span')[0].text]
                            print(dta)
                            writer.writerow(dta)
                            print("producto creado") 
                        #print(t.text.strip())
                    #style__Container-sc-r27pq8-1 dkvZNb
        if request.POST.get("unimarc"):
            with open('unimarc.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='$')
                writer.writerow([
                            'SKU',
                            'ean',
                            'Nombre',
                            'description',
                            'marca',
                            'precio',
                            'precio_unidad'
                             ])
                for t in ['C:349','C:350','C:351','C:352','C:353','C:354','C:355','C:356','C:357','C:358','C:359','C:360','C:361','C:362','C:363','C:364','C:365','C:366','C:367']:
                    for i in range(0,45):
                        if i == 0:
                            url = "https://bff-unimarc-web.unimarc.cl/bff-api/products/?from=0&to=40&fq="+t
                        else:
                            minimo = (i*40)+1
                            maximo = minimo+40
                            url = "https://bff-unimarc-web.unimarc.cl/bff-api/products/?from="+str(minimo)+"&to="+str(maximo)+"&fq="+t
                        payload={}
                        headers = {
                        'authority': 'bff-unimarc-web.unimarc.cl',
                        'accept': 'application/json, text/plain, */*',
                        'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                        'cookie': '_gid=GA1.2.2034699617.1656000090; _hjFirstSeen=1; _hjSession_2255287=eyJpZCI6IjAwYjYwNmFiLTI1N2UtNGYxMy04MzkxLWFiODYxOTdhYWU5ZCIsImNyZWF0ZWQiOjE2NTYwMDAwODk5NzAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gcl_aw=GCL.1656000090.Cj0KCQjwntCVBhDdARIsAMEwACk4TEvYuZVw6DkUz50j6H1tm9BzJOSa9pQd7LknvWDiFiPC7w2BL4kaAnwEEALw_wcB; _gcl_au=1.1.2109869675.1656000090; _tt_enable_cookie=1; _ttp=b19eefbb-62c9-492d-a348-cbb064bb8cdd; _clck=18zrtrv|1|f2k|0; _gac_UA-46206544-6=1.1656000095.Cj0KCQjwntCVBhDdARIsAMEwACk4TEvYuZVw6DkUz50j6H1tm9BzJOSa9pQd7LknvWDiFiPC7w2BL4kaAnwEEALw_wcB; _hjSessionUser_2255287=eyJpZCI6IjM5OGEzZjc2LTAyMWEtNTFhZS05MmZkLTM0NDkyNjE2YzMzNiIsImNyZWF0ZWQiOjE2NTYwMDAwODk5MDcsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.2.1747269101.1656000090; _clsk=y2uray|1656000184864|4|1|n.clarity.ms/collect; _gat_UA-46206544-6=1; _ga_HP7650L1SD=GS1.1.1656000089.1.1.1656000797.60',
                        'origin': 'https://www.unimarc.cl',
                        'referer': 'https://www.unimarc.cl/',
                        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
                        }
                        
                        response = requests.request("GET", url, headers=headers, data=payload)
                        data = response.json()
                        try:
                            for product in data['data']['products']:
                                try:
                                    nombre = product['name'].strip().replace("\n"," ").replace("\r","")
                                except Exception:
                                    nombre = ""
                                try:
                                    sku = product['sku']
                                except Exception:
                                    sku = ""
                                try:
                                    ean = product['ean']
                                except Exception:
                                    ean = ""
                                try:
                                    brand = product['brand'].strip().replace("\n"," ").replace("\r","")
                                except Exception:
                                    brand = ""
                                try:
                                    description = product['description'].strip().replace("\n"," ").replace("\r","")
                                except Exception:
                                    description = ""
                                try:
                                    precio = product['sellers'][0]['price']
                                    print(precio)
                                except Exception:
                                    precio = ""
                                try:
                                    precio_unidad = product['sellers'][0]['ppum']
                                    print(precio_unidad)
                                except Exception:
                                    print("error")
                                    precio_unidad = ""
                                writer.writerow([
                                        sku,
                                        ean,
                                        nombre,
                                        description,
                                        brand,
                                        precio,
                                        precio_unidad
                                        ])
                        except Exception:
                            pass
                         
        if request.POST.get("santa"):
            with open('santa_isabel.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='$')
                writer.writerow([
                            'Nombre',
                            'SKU',
                            'Marca',
                            'Precio'
                             ])
                keywords = ['desayuno-y-dulces/chocolates-y-dulces','desayuno-y-dulces/galletas-y-colaciones','desayuno-y-dulces/te-mate-y-hierbas','desayuno-y-dulces/cafe-y-cafeteras','congelados/verduras-congeladas',
                            'congelados/frutas-congeladas','congelados/hamburguesas','congelados/nuggets-y-apanados',
                            'pescaderia/camarones','pescaderia/pescados','pescaderia/ahumados-y-carpaccios','pescaderia/mariscos','panaderia-y-pasteleria/panaderia-granel','panaderia-y-pasteleria/panaderia-envasada','panaderia-y-pasteleria/pasteleria','panaderia-y-pasteleria/masas-y-tortillas',
                            'mi-bebe/panales-y-toallas-humedas','mi-bebe/colados-picados-y-otros','mi-bebe/leche-y-suplementos-infantiles','mi-bebe/perfumeria-infantil','lacteos/leches/leche-liquida','lacteos/leches/leche-en-polvo','belleza-y-cuidado-personal','vinos-cervezas-y-licores','quesos-y-fiambres','hogar/cocina','hogar/decoracion','hogar/celebraciones','hogar/cama','despensa/aceites-sal-y-condimentos/aceite',
                            'mundo-vegano','comidas-preparadas','lacteos/huevos','mascotas/perros/alimentos-cachorros','mascotas/perros/alimentos-adultos','mascotas/perros/alimentos-senior','mascotas/perros/alimentos-razas-pequenas','mascotas/gatos/alimentos-cachorros','mascotas/gatos/alimentos-adultos','mascotas/gatos/snacks-y-salsas','mascotas/gatos/arenas-higiene-y-accesorios',
                            'lacteos/mantequillas-y-margarinas','/lacteos/postres','despensa/pastas-y-salsas','despensa/arroz-y-legumbres','despensa/aceites-sal-y-condimentos',
                            'despensa/conservas','despensa/coctel','despensa/aderezos-y-salsas','despensa/instantaneos-y-sopas','vinos-cervezas-y-licores/vinos','vinos-cervezas-y-licores/cervezas','vinos-cervezas-y-licores/destilados','vinos-cervezas-y-licores/licores-y-cocteles',
                            'despensa/reposteria','despensa/harina-y-complementos','carniceria/vacuno','carniceria/cerdo','carniceria/pavo','carniceria/pollo','bebidas-aguas-y-jugos/aguas-minerales',
                            'bebidas-aguas-y-jugos/bebidas-gaseosas','bebidas-aguas-y-jugos/jugos','frutas-y-verduras/frutas/fruta','frutas-y-verduras/frutos-secos-y-semillas','frutas-y-verduras/frutas/frutas-organicas','frutas-y-verduras/frutas/frutas-picadas','frutas-y-verduras/verduras/verdura','frutas-y-verduras/verduras/verduras-organicas','frutas-y-verduras/verduras/ensaladas','frutas-y-verduras/verduras/hierbas-y-especias','frutas-y-verduras/frutos-secos-y-semillas/frutos-secos','frutas-y-verduras/frutos-secos-y-semillas/frutas-deshidratadas','frutas-y-verduras/frutos-secos-y-semillas/semillas-y-granos',
                            'limpieza/papeles-hogar','limpieza/pisos-y-muebles','limpieza/papeles-hogar/papel-higienico',
                            'limpieza/papeles-hogar/panuelos','limpieza/papeles-hogar/servilletas','limpieza/papeles-hogar/toallas-de-papel','limpieza/limpieza-de-ropa/detergente-liquido','limpieza/limpieza-de-ropa/detergente-en-polvo',
                            'limpieza/limpieza-de-ropa/suavizantes','limpieza/limpieza-de-ropa/cloro-para-ropa','limpieza/accesorios-de-limpieza/limpiadores-de-calzado','limpieza/aerosoles-y-desinfectantes/cloros','limpieza/aerosoles-y-desinfectantes/desinfectantes','limpieza/aerosoles-y-desinfectantes/desodorantes-ambientales'
                            'limpieza/aerosoles-y-desinfectantes','limpieza/accesorios-de-limpieza',
                            'limpieza/limpieza-de-ropa','limpieza/bano-y-cocina/lavalozas','limpieza/bano-y-cocina/lavavajillas','limpieza/bano-y-cocina/limpiadores-bano-y-cocina','limpieza/bano-y-cocina/limpiavidrios',
                            'limpieza/bano-y-cocina']
                for i in keywords:
                    for t in range(1,40):
                        try:
                            url = "https://apis.santaisabel.cl:8443/catalog/api/v2/pedrofontova/products/"+(i)+"?page="+str(t)+"&sc=1"
                            print(url)
                            payload={}
                            headers = {
                            'authority': 'apis.santaisabel.cl:8443',
                            'accept': 'application/json',
                            'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                            'content-type': 'application/json',
                            'if-none-match': 'W/"14ba7-DxlizjkH6OF1ta3/hbEwrkK5OBg"',
                            'origin': 'https://www.santaisabel.cl',
                            'referer': 'https://www.santaisabel.cl/',
                            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"macOS"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-site',
                            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                            'x-account': 'pedrofontova',
                            'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j',
                            'x-consumer': 'santaisabel'
                            }

                            response = requests.request("GET", url, headers=headers, data=payload)
                            
                            data = response.json()
                            try:
                                for dat in data['products']:
                                    try:
                                        sku = dat["productId"]
                                    except Exception:
                                        sku= ""
                                    try:
                                        nombre = dat['productName'].strip().replace("\n"," ").replace("\r","")
                                    except Exception:
                                        nombre = ""
                                    try:
                                        marca = dat['brand'].strip().replace("\n"," ").replace("\r","")
                                    except Exception:
                                        marca = ""
                                    try:
                                        precio = dat['items'][0]['sellers'][0]['commertialOffer']['Price']
                                    except Exception:
                                        precio = ""
                                    writer.writerow([
                                                sku,
                                                nombre,
                                                marca,
                                                precio
                                                ])     
                            except Exception as e:
                                print("error")
                        except Exception as e:
                                print("error")
        if request.POST.get("lider"):
            f = open("pasillos_2.txt", "r") 
            links_lider =  [x.replace("\n","") for x in f]
            info = []
            with open('lider_data_nueva23.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    'SKU',
                    'Nombre',
                    'EAN',
                    'Precio por unidad',
                    'Precio internet',
                    'Marca'])
                for li in links_lider:
                    print(li)
                    base = '?No='
                    base2 = '&isNavRequest=Yes&Nrpp='
                    base3 = '&page='
                    for i in range(1,25):
                        page = str(40*(i-1))
                        buffer =''
                        page_number = i
                        buffer = base + page + base2 + page + base3 + str(page_number)
                        if i != 1:
                            url = li+buffer
                        else:    
                            url = li
                        url = "https://apps.lider.cl/supermercado/bff/category"
                        payload="""{\"categories\":\""""+li+"""\",\"page\":"""+str(i)+""",\"facets\":[],\"sortBy\":\"\",\"hitsPerPage\":16}"""
                        headers = {
                        'authority': 'apps.lider.cl',
                        'accept': 'application/json, text/plain, */*',
                        'accept-language': 'es-419,es;q=0.9,en;q=0.8',
                        'content-type': 'application/json',
                        'origin': 'https://www.lider.cl',
                        'referer': 'https://www.lider.cl/',
                        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'tenant': 'supermercado',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                        'x-channel': 'SOD',
                        'x-flowid': '2dd37c6d-46fb-42ed-b88d-dca2b7b9554d',
                        'x-sessionid': '61a19a8e-8f85-451c-a451-67701acb1c9d',
                        'Cookie': 'zy_did=CE31A0AE-38CE-D4B5-C482-D51C795D449D; TS018b674b=01538efd7cf2861261d923e618ea12dc0edf73a737162681c9cc4e553f0d3a0283c2aaf94b66522cad5c3f6a4d1aa9c04d6b872201'
                        }

                        response = requests.request("POST", url, headers=headers, data=payload)
                        try:
                            parser_response = response.json()
                            print(parser_response)
                            for line in (parser_response['products']):
                                buffer = []
                                buffer.append(line['sku'])
                                buffer.append(line['displayName'])
                                buffer.append(line['gtin13'])
                                buffer.append(line['price']['BasePricePerUm'])
                                buffer.append(line['price']['BasePriceReference'])
                                buffer.append(line['brand'])
                                print(buffer)
                                writer.writerow(buffer)
                        except JSONDecodeError:
                            print("Erro")
                            break
                        
        if request.POST.get('pedidos_ya'):
            '''url = "https://www.pedidosya.cl/mobile/v3/catalogues/273953/sections?partnerId=254692&max=20&maxProducts=10&offset=0"
            payload={}
            headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Cookie': '_pxhd=xXHgopV3WiMGCoV7OT/A9wArfVYgpQtBlB3svvS6VU1WlEplOKvLv4KFsK5y7PN0BB3oGPCt1AvEbcXm4xLEvA==:FOD89pPnCyVVC0HnEA7c16dzz3gdCyL-y1nLLW5uIEJvS2CsokjYe7pBQfYLP967ZAH2IBtm99yryBVqU3EAboqG-Dcnlodp2yVANWyiQgU=; __cf_bm=69ysaKv9WTrXFP_OTk6g7Pj1QfEb06UAxUEr8oXlTVM-1650924923-0-AQ7OCQ9801Vrt/SDXGOWCveiFgolyOBzSU6hESWBA6tRL/IuqB8nyYOC4ywhI/lrSF+FbVkYn27dUy/FErYCUkU=; dhhPerseusGuestId=1650924958740.465914258195631040.loavcn6xixf; dhhPerseusSessionId=1650924958740.719575921688868200.3iydtiq3o1t; __Secure-peya.sid=s%3Accbfdeb2-dbda-4849-ae2e-9e7c6d511fb1.kUCs6putVDhv0j%2FpJiX1xsk9h0Y0n1sD91grXIE4%2B0o; __Secure-peyas.sid=s%3Af82df708-57b5-4f80-9a95-c1239e4e117e.fyFv%2Fm9q%2FLGpeM1XxEU07geScFyBFC80fkR4rJK92wk; dhhPerseusHitId=1650925259118.284025885506718820.1kjr27m3s22'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)'''
            data = open("pasillos.txt","r")
            data_string = ""
            result = []
            for i in data:
                if len(i.split("/")) == 3 and 'supermercado' not in i:
                    result.append(i.replace("_"," ").replace("\n",""))
            for i in result:
                print(i)
        if request.POST.get("jumbo"):
            keywords = ['desayuno-y-dulces/chocolates-y-dulces','desayuno-y-dulces/galletas-y-colaciones','desayuno-y-dulces/te-mate-y-hierbas','desayuno-y-dulces/cafe-y-cafeteras','congelados/verduras-congeladas',
                        'congelados/frutas-congeladas','congelados/hamburguesas','congelados/nuggets-y-apanados',
                        'pescaderia/camarones','pescaderia/pescados','pescaderia/ahumados-y-carpaccios','pescaderia/mariscos','panaderia-y-pasteleria/panaderia-granel','panaderia-y-pasteleria/panaderia-envasada','panaderia-y-pasteleria/pasteleria','panaderia-y-pasteleria/masas-y-tortillas',
                        'mi-bebe/panales-y-toallas-humedas','mi-bebe/colados-picados-y-otros','mi-bebe/leche-y-suplementos-infantiles','mi-bebe/perfumeria-infantil','lacteos/leches/leche-liquida','lacteos/leches/leche-en-polvo','belleza-y-cuidado-personal','vinos-cervezas-y-licores','quesos-y-fiambres','hogar/cocina','hogar/decoracion','hogar/celebraciones','hogar/cama','despensa/aceites-sal-y-condimentos/aceite',
                        'mundo-vegano','comidas-preparadas','lacteos/huevos','mascotas/perros/alimentos-cachorros','mascotas/perros/alimentos-adultos','mascotas/perros/alimentos-senior','mascotas/perros/alimentos-razas-pequenas','mascotas/gatos/alimentos-cachorros','mascotas/gatos/alimentos-adultos','mascotas/gatos/snacks-y-salsas','mascotas/gatos/arenas-higiene-y-accesorios',
                        'lacteos/mantequillas-y-margarinas','/lacteos/postres','despensa/pastas-y-salsas','despensa/arroz-y-legumbres','despensa/aceites-sal-y-condimentos',
                        'despensa/conservas','despensa/coctel','despensa/aderezos-y-salsas','despensa/instantaneos-y-sopas','vinos-cervezas-y-licores/vinos','vinos-cervezas-y-licores/cervezas','vinos-cervezas-y-licores/destilados','vinos-cervezas-y-licores/licores-y-cocteles',
                        'despensa/reposteria','despensa/harina-y-complementos','carniceria/vacuno','carniceria/cerdo','carniceria/pavo','carniceria/pollo','bebidas-aguas-y-jugos/aguas-minerales',
                        'bebidas-aguas-y-jugos/bebidas-gaseosas','bebidas-aguas-y-jugos/jugos','frutas-y-verduras/frutas/fruta','frutas-y-verduras/frutos-secos-y-semillas','frutas-y-verduras/frutas/frutas-organicas','frutas-y-verduras/frutas/frutas-picadas','frutas-y-verduras/verduras/verdura','frutas-y-verduras/verduras/verduras-organicas','frutas-y-verduras/verduras/ensaladas','frutas-y-verduras/verduras/hierbas-y-especias','frutas-y-verduras/frutos-secos-y-semillas/frutos-secos','frutas-y-verduras/frutos-secos-y-semillas/frutas-deshidratadas','frutas-y-verduras/frutos-secos-y-semillas/semillas-y-granos',
                        'limpieza/papeles-hogar','limpieza/pisos-y-muebles','limpieza/papeles-hogar/papel-higienico',
                        'limpieza/papeles-hogar/panuelos','limpieza/papeles-hogar/servilletas','limpieza/papeles-hogar/toallas-de-papel','limpieza/limpieza-de-ropa/detergente-liquido','limpieza/limpieza-de-ropa/detergente-en-polvo',
                        'limpieza/limpieza-de-ropa/suavizantes','limpieza/limpieza-de-ropa/cloro-para-ropa','limpieza/accesorios-de-limpieza/limpiadores-de-calzado','limpieza/aerosoles-y-desinfectantes/cloros','limpieza/aerosoles-y-desinfectantes/desinfectantes','limpieza/aerosoles-y-desinfectantes/desodorantes-ambientales'
                        'limpieza/aerosoles-y-desinfectantes','limpieza/accesorios-de-limpieza',
                        'limpieza/limpieza-de-ropa','limpieza/bano-y-cocina/lavalozas','limpieza/bano-y-cocina/lavavajillas','limpieza/bano-y-cocina/limpiadores-bano-y-cocina','limpieza/bano-y-cocina/limpiavidrios',
                        'limpieza/bano-y-cocina']
            info_j_l = []
            with open('lider_data.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                            'Nombre',
                            'SKU',
                            'Marca',
                            'description',
                            'ean',
                            'Ingredientes',
                            'Condiciones Alimentarias',
                            'Porción',
                            'Porciones por envase',
                            'Energía (kCal)',
                            'Proteínas (g)',
                            'Grasas Totales (g)',
                            'Azúcares totales (g)',
                            'Hidratos de Carbono disponibles (g)',
                            'Fibra (g)',
                            'Sodio (g)',
                            'Colesterol (mg)',
                            'categoria',
                            'sub categoria',
                            'sub-sub categoria',
                            'Precio online',
                            'Precio Lista',
                            'Precio Sin descuento',
                            'Cantidad disponible',
                            'puntuacion1',
                            'puntuacion2'
                             ])
                for key in keywords:
                    #print(key)
                    for page in range(1,60):
                        try:
                            url = "https://apijumboweb.smdigital.cl/catalog/api/v2/products/"+key+"?o=OrderByTopSaleDESC&page="+str(page)
                            payload={}
                            headers = {
                            'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j'
                            }
                            response = requests.request("GET", url, headers=headers, data=payload)
                            try:
                                response_json = response.json()
                                info_jumbo = response_json['products']
                                score = 0
                                for i in info_jumbo:
                                    score+= 1
                                    info_j = []
                                    info_j.append(i['productName'])
                                    info_j.append(i['productId'])
                                    info_j.append(i['brand'])
                                    url1 = 'https://apijumboweb.smdigital.cl/catalog/api/v1/product/'+i['linkText']+'?sc=11'
                                    headers1 = {
                                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                                    'sec-ch-ua-mobile': '?0',
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'accept': 'application/json',
                                    'Referer': 'https://www.jumbo.cl/',
                                    'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j',
                                    'sec-ch-ua-platform': '"macOS"'
                                    }
                                    payload1 = {}
                                    response_prod = requests.request("GET", url1, headers=headers1, data=payload1)
                                    response_product = response_prod.json()
                                    cont = 0
                                    try:
                                        #foto = response_product[0]['items'][0]['images'][0]['imageUrl']
                                        pass
                                    except Exception:
                                        foto= "no hay dato"
                                    try:
                                        ingredientes = response_product[0]['Ingredientes']
                                    except Exception:
                                        ingredientes = "no hay data"
                                    try:
                                        desct = response_product[0]['description'].strip().replace("\n"," ").replace("\r","")
                                    except Exception:
                                        desct = "no hay data"
                                    try:
                                        product_ean = int(response_product[0]['items'][0]['ean'])
                                        print(product_ean)
                                    except Exception:
                                        product_ean = "no hay data"
                                    try:
                                        product_ingredientes = response_product[0]['Ingredientes']
                                    except Exception:
                                        product_ingredientes = "no hay data"
                                    try:
                                        etiquetas = response_product[0]['Condiciones Alimentarias']
                                    except Exception:
                                        etiquetas = "no hay data"
                                    try:
                                        porcion = response_product[0]['Porción']
                                    except Exception:
                                        porcion = "no hay data"
                                    try:
                                        porciones_envase = response_product[0]['Porciones por envase']
                                    except Exception:
                                        porciones_envase = "no hay data"
                                    try:
                                        energia = response_product[0]['Energía (kCal)']
                                    except Exception:
                                        energia = "no hay data"
                                    try:
                                        proteinas = response_product[0]['Proteínas (g)']
                                    except Exception:
                                        proteinas = "no hay data"
                                    try:
                                        grasas = response_product[0]['Grasas Totales (g)']
                                    except Exception:
                                        grasas = "no hay data"
                                    try:
                                        azucar = response_product[0]['Azúcares totales (g)']
                                    except Exception:
                                        azucar = "no hay data"
                                    try:
                                        hidratos_carbono = response_product[0]['Hidratos de Carbono disponibles (g)']
                                    except Exception:
                                        hidratos_carbono = "no hay data"
                                    try:
                                        fibra = response_product[0]['Fibra (g)']
                                    except Exception:
                                        fibra = "no hay data"
                                    try:
                                        sodio = response_product[0]['Sodio (mg)']
                                    except Exception:
                                        sodio = "no hay data"
                                    try:
                                        colesterol = response_product[0]['Colesterol (mg)']
                                    except Exception:
                                        colesterol = "no hay data"
                                    #info_j.append(foto)
                                    info_j.append(desct)
                                    info_j.append(product_ean)
                                    info_j.append(product_ingredientes)
                                    info_j.append(etiquetas)
                                    info_j.append(porcion)
                                    info_j.append(porciones_envase)
                                    info_j.append(energia)
                                    info_j.append(proteinas)
                                    info_j.append(grasas)
                                    info_j.append(azucar)
                                    info_j.append(hidratos_carbono)
                                    info_j.append(fibra)
                                    info_j.append(sodio)
                                    info_j.append(colesterol)
                                    category = i['categories'][0]
                                    try:
                                        info_j.append(category.split("/")[0])
                                    except Exception:
                                        info_j.append("no hay dato")
                                    try:
                                        info_j.append(category.split("/")[1])
                                    except Exception:
                                        info_j.append("no hay dato")
                                    try:
                                        info_j.append(category.split("/")[2])
                                    except Exception:
                                        info_j.append("no hay dato")
                                    info_j.append(i['items'][0]['sellers'][0]['commertialOffer']['Price'])
                                    info_j.append(i['items'][0]['sellers'][0]['commertialOffer']['ListPrice'])
                                    info_j.append(i['items'][0]['sellers'][0]['commertialOffer']['PriceWithoutDiscount'])
                                    info_j.append(i['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'])
                                    info_j.append(page)
                                    info_j.append(score)
                                    writer.writerow(info_j)
                                    info_j_l.append(info_j)
                                    
                            except JSONDecodeError:
                                print("error")
                        except Exception:
                            pass
                context['info_j'] = info_j_l
    context['info_lider'] = info    
    context['productos_rapi'] = producto.objects.all()                
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
            
        segment, active_menu = get_segment( request )
        
        context['segment']     = segment
        context['active_menu'] = active_menu

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment     = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment     = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboards-'):
            active_menu = 'dashboard'

        if segment.startswith('account-') or segment.startswith('users-') or segment.startswith('profile-') or segment.startswith('projects-'):
            active_menu = 'pages'

        if  segment.startswith('notifications') or segment.startswith('sweet-alerts') or segment.startswith('charts.html') or segment.startswith('widgets') or segment.startswith('pricing'):
            active_menu = 'pages'            

        return segment, active_menu     

    except:
        return 'index', 'dashboard'  

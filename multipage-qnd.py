import requests
import lxml.html
import sys

pagerangestart = 3
pagerangeend = 10

categories = ["refrigerator-dealers","home-furniture","domestic-courier-delivery-services", "international-courier-delivery-services","marble-granite-dealers","production-houses"]

#f = open("scrape-sulekha-" + "page" +str(pagerangestart)+'-'+str(pagerangeend-1)+".csv", 'w')

with open("scrape-sulekha-" + "page" +str(pagerangestart)+'-'+str(pagerangeend-1)+".csv", 'w') as f:
    
    f.write("company_name, contact_number, address, description, url \n")
        
    for category in categories:

        for page in range(pagerangestart,pagerangeend):

            pageURL = "http://yellowpages.sulekha.com/" + category+ "_mumbai_"+str(page)
            print ("Processing URL " + pageURL +" ...")

            page_response = requests.get(pageURL, timeout=30)

            if page_response.status_code != requests.codes.ok:
                print(pageURL + " skipped on error")
                continue
            
            page_html = page_response.content

            page_dom = lxml.html.fromstring(page_html)
               
            entries = page_dom.xpath('//li[@class="list-item "]')
            entrynumber = 0
            
            for entry in entries:

                entrynumber += 1
                print ("Processing listing " + str(entrynumber) +"...")

                company_name = entry.xpath('.//span[@itemprop="name"]/text()')[0].replace(',',';').strip()

                contact_number_element = entry.xpath('.//b[@class="contact-number"]/text()')
                if contact_number_element:
                    contact_number = contact_number_element[0].replace(',',';').strip()
                else:
                    contact_number = ""
                    
                address_element = entry.xpath('.//address[@class="pull-left"]/text()')
                if address_element:
                    address = address_element[0].replace(',',';').strip()
                else:
                    address = ""
                
                entryURL = "http://yellowpages.sulekha.com" + entry.xpath('.//a[@class="YPTRACK GAQ_C_BUSL"]/@href')[0]

                entry_response = requests.get(entryURL, timeout=30)
                print(entryURL + " skipped on error")

                if entry_response.status_code != requests.codes.ok:
                    continue
                
                entry_html = entry_response.content
                entry_dom = lxml.html.fromstring(entry_html)

                description_element = entry_dom.xpath('.//div[@id="showlessabtbuslist"]/p/text()')
                if description_element:
                    description = description_element[0].replace(',',';').strip()
                else:
                    description = ""
                      
                f.write(company_name + "," + contact_number + "," + address + "," + description + "," + entryURL + "\n")

print ('Exported Successfully!')

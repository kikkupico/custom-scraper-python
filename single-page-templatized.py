import requests
import lxml.html
from collections import OrderedDict

fileNamePrefix = 'scrape-iamwire'
pagerangestart = 251
pagerangeend = 501

##PAGE URL: http://www.iamwire.com/page/1
pageURLPrefix = 'http://www.iamwire.com/page/'
pageURLSuffix = ''

rowXpath = '//article'
fieldsAndXpaths = OrderedDict([('site','NON_XPATH'),
                   ('article_title' , './/div[@class="entry-list-right"]/h2/a/@title'),
                   ('author_name' , './/div[@class="entry-list-right"]/div[@class="entry-meta"]/span[@class="author vcard"]/a/text()'),
                   ('author_email' , './/div[@class="entry-list-right"]/div[@class="entry-meta"]/span[@class="author vcard"]/a/text()'),
                   ('article_url' , './/div[@class="entry-list-right"]/h2/a/@href')
                   ])


with open(fileNamePrefix + "-page" +str(pagerangestart)+'-'+str(pagerangeend-1)+".csv", 'w') as f:

    #writing column names
    f.write(','.join(list(fieldsAndXpaths.keys()))+'\n')

    #iterating through the webpages
    for page in range(pagerangestart,pagerangeend):

        pageURL = pageURLPrefix + str(page) + pageURLSuffix
        print ("Processing URL " + pageURL +" ...")

        #if page times out after 30 seconds or returns error response skip page after showing error message
        page_response = requests.get(pageURL, timeout=30)
        if page_response.status_code != requests.codes.ok:
            print(pageURL + " skipped on error")
            continue
        
        page_html = page_response.content
        page_dom = lxml.html.fromstring(page_html)

        #getting all rows       
        rows = page_dom.xpath(rowXpath)


        #iterating through rows
        rownumber = 0
        for row in rows:

            rowdata = []
            rownumber += 1
            print ("Processing row " + str(rownumber) +"...")

            #iterating through fields
            for field,xpath in fieldsAndXpaths.items():
                if xpath == 'NON_XPATH':  #handle non xpath fields here
                    if field =='site':
                        rowdata.append('iamwire.com')

                else:  #handle xpath fields here
                    element = row.xpath(xpath)
                    if element:
                        fieldvalue = element[0].replace(',',';').strip()

                        #do custom formatting if required here
                        if field == 'author_email':
                            space_in_name = fieldvalue.find(' ')
                            
                            if space_in_name != -1:
                                fieldvalue = fieldvalue[:space_in_name].lower() + '@iamwire.com'
                            else:
                                fieldvalue = fieldvalue.lower() + '@iamwire.com'

                        rowdata.append(fieldvalue) #field value is appended to the row
                                        
                    else:
                        rowdata.append("") #null value is appended to the row if xpath returns no element

            #writing a row of data
            f.write(','.join(rowdata).encode('utf-8').decode('ascii','ignore')+'\n')
                
                    
            
            
##        
##    for page in range(pagerangestart,pagerangeend):
##
##        #PAGE URL: http://yourstory.com/ys-stories/page/2/
##        pageURL = "http://yourstory.com/ys-stories/page/" +str(page)
##        print ("Processing URL " + pageURL +" ...")
##
##        page_response = requests.get(pageURL, timeout=30)
##
##        if page_response.status_code != requests.codes.ok:
##            print(pageURL + " skipped on error")
##            continue
##        
##        page_html = page_response.content
##
##        page_dom = lxml.html.fromstring(page_html)
##           
##        entries = page_dom.xpath('//li[@class="grid-full mb-30"]')
##        entrynumber = 0
##        
##        for entry in entries:
##
##            entrynumber += 1
##            print ("Processing listing " + str(entrynumber) +"...")
##
##            article_title = entry.xpath('.//div[@class="title-small bentonCondensed bold color-black-2 truncate-2"]/text()')[0].replace(',',';').strip()
##            author_name = entry.xpath('.//div[@class="postInfo color-ys"]/text()')[0].replace(',',';').strip()
##
##            space_in_name = author_name.find(' ')
##            if space_in_name != -1:
##                author_email = author_name[:space_in_name].lower() + '@yourstory.com'
##            else:
##                author_email = author_name.lower() + '@yourstory.com'
##            
##            article_url = entry.xpath('.//a[@class="block"]/@href')[0].replace(',',';').strip()

##            contact_number_element = entry.xpath('.//div[@class="postInfo color-ys"]/text()')
##            if contact_number_element:
##                contact_number = contact_number_element[0].replace(',',';').strip()
##            else:
##                contact_number = ""
##                
##            address_element = entry.xpath('.//address[@class="pull-left"]/text()')
##            if address_element:
##                address = address_element[0].replace(',',';').strip()
##            else:
##                address = ""
##
##            locality_element = entry.xpath('.//a[@class="YPTRACK GAQ_C_BUSL"]/text()')
##            if locality_element:
##                locality = locality_element[0].replace(',','').strip()
##            else:
##                locality = ""
##            
##            entryURL = "http://yellowpages.sulekha.com" + entry.xpath('.//a[@class="YPTRACK GAQ_C_BUSL"]/@href')[0]

## !!!!!!!!!!!!!!!!!!!DO NOT DELETE THESE COMMENTS!!!!
##                entry_response = requests.get(entryURL, timeout=30)
##                print(entryURL + " skipped on error")
##
##                if entry_response.status_code != requests.codes.ok:
##                    continue
##                
##                entry_html = entry_response.content
##                entry_dom = lxml.html.fromstring(entry_html)

##                description_element = entry_dom.xpath('.//div[@id="showlessabtbuslist"]/p/text()')
##                if description_element:
##                    description = description_element[0].replace(',',';').strip()
##                else:
##                    description = ""
                  
##            f.write("yourstory.com" + "," + article_title.encode('utf-8').decode('ascii','ignore') + "," + author_name.encode('utf-8').decode('ascii','ignore') + ","
##                    + author_email.encode('utf-8').decode('ascii','ignore') + "," + article_url.encode('utf-8').decode('ascii','ignore') + "\n")

print ('Exported Successfully!')

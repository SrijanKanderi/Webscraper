from selenium import webdriver
from re import sub
import json
opts = webdriver.ChromeOptions()
opts.headless = True
driver = webdriver.Chrome(executable_path= r"G:/chromedriver.exe",options =opts)



####SCRAPING IP WEBSITE FOR IP LIST

driver.get('http://www.freeproxylists.net/?c=US&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0')

odd_element = driver.find_elements_by_class_name('Odd')
even_element = driver.find_elements_by_class_name('Even')
next_page = driver.find_element_by_class_name("page")
next_button_IP = next_page.find_elements_by_tag_name("a")[1]


proxylist=[]
flag_IP = True


while flag_IP == True:
    for element in odd_element:
        try:
            IP_odd = element.find_element_by_tag_name('a').text
            Port_odd = element.find_elements_by_tag_name("td")[1].text
            t = [IP_odd+":"+Port_odd]
            proxylist.append(t)
        except:
            pass

    for element in even_element:
        try:
            IP_even = element.find_element_by_tag_name('a').text
            Port_even = element.find_elements_by_tag_name("td")[1].text
            t = [IP_even+":"+Port_even]
            proxylist.append(t)
        except:
            pass

    try:
        next_button_IP.click()
    except:
        flag_IP= False

#### SCRAPING MAIN WEBSITE





driver.get('https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1')
Products = driver.find_elements_by_class_name('product')
statusline = driver.find_elements_by_class_name('pagination')[0]
next_button = statusline.find_element_by_link_text("Next")



driver.implicitly_wait(12)  ##For that pesky popup bar!
popupline = driver.find_element_by_class_name('ltkpopup-close')
popup= popupline.find_element_by_id("x-mark-icon")
popup.click()


n=0
Products_list = list()
switch=True
while switch == True:
    for Product in Products:
        try:
            Title = Product.find_elements_by_class_name("catalog-item-name")[0].text

            try:
                Price = Product.find_elements_by_class_name("price")[0].text
                Price = float(sub(r'[^\d.]', '', Price))
            except:
                Price = "NA"
            try:
                Stock = Product.find_elements_by_class_name("out-of-stock")[0].text
                if Stock == "Out of Stock":
                    Stock = False
                else:
                    Stock= True
            except:
                Stock = "NA"
            try:
                Manufacturer = Product.find_elements_by_class_name("catalog-item-brand")[0].text
            except:
                Manufacturer = "NA"

            dictionary = dict()
            dictionary.update({"price":Price})
            dictionary.update({"title": Title})
            dictionary.update({"stock": Stock})
            dictionary.update({"maftr": Manufacturer})
            Products_list.append(dictionary)

        except:
            pass
    n += 1
    try:
        next_button.click()
        PROXY = proxylist[0][n]
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,

            "proxyType": "MANUAL",

        }
    except:
        switch = False

with open("result.json", "w") as outfile:
    json.dump(Products_list,outfile)






































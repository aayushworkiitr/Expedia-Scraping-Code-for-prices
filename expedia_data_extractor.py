# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
###make sure you install selenium, chromedriver & phantomJs in the server where it is being deployed
import pandas as pd
import random
import string
import itertools
from itertools import compress
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
import warnings
import math
import datetime
import time
import os
import re
import socket

#hostname = socket.gethostname()
#IP = socket.gethostbyname(hostname)

def date_matrix_calculator(date_to_quer,origin,start_day_for_domain_calender):
    import datetime
    import pandas as pd   
    if origin=="today":
        now = datetime.datetime.now()
    else:
        now=pd.to_datetime(origin)
    #now=pd.to_datetime("20/12/2016")
    date_to_quer=pd.to_datetime(date_to_quer)
    current_month=datetime.datetime.now()
    current_month=current_month.month
    if (date_to_quer.year==now.year and date_to_quer.month - now.month<=2):
        no_of_clicks_on_next_button=date_to_quer.month-now.month-1
        if (date_to_quer.month==current_month):
            value_of_div=2
        else:
            value_of_div=3
    elif (date_to_quer.year==now.year and date_to_quer.month - now.month>2):
        no_of_clicks_on_next_button=date_to_quer.month-now.month-1
        value_of_div=3
    elif (date_to_quer.year!=now.year):
        no_of_clicks_on_next_button=((date_to_quer.year-now.year-1)*12)+(date_to_quer.month-(12-now.month)-1)
        value_of_div=3
    elif (date_to_quer.year==now.year and date_to_quer.month-now.month<2 and date_to_quer.month!=current_month):
        no_of_clicks_on_next_button=0
        value_of_div=3
    else:
        no_of_clicks_on_next_button=0
        value_of_div=3
    
    if start_day_for_domain_calender=="sunday":
        offset_val=0
    elif start_day_for_domain_calender=="monday":
        offset_val=1
    elif start_day_for_domain_calender=="tuesday":
        offset_val=2
    elif start_day_for_domain_calender=="wednesday":
        offset_val=3
    elif start_day_for_domain_calender=="thursday":
        offset_val=4
    elif start_day_for_domain_calender=="Friday":
        offset_val=5
    else:
        offset_val=6
    value_of_col=round((date_to_quer.weekday()+offset_val),0)
    ##week starts from Monday
    
    nearest_sunday_date=date_to_quer-datetime.timedelta(days=value_of_col-offset_val)
    farthest_sunday_date=pd.to_datetime(str(date_to_quer.month)+"/"+"01/"+str(date_to_quer.year),format="%m/%d/%Y")
    farthest_sunday_date=farthest_sunday_date+datetime.timedelta(days=(7-farthest_sunday_date.weekday()))
    
    value_of_row= 2 + round(((nearest_sunday_date-farthest_sunday_date).days/7),0)
    return {'no_of_clicks_on_next':no_of_clicks_on_next_button, 'div_value':value_of_div, 'row_value':value_of_row ,'col_value':value_of_col }
#browser.find_element_by_css_selector('#overlayInnerDiv > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td:nth-child(6) > div').click()
#####################################################################################################################################################

def room_selector(browser,no_of_rooms,no_of_adults,no_of_children):
    
    ##change div[#] to change month & change tr[row number]/td[column number] for changing date
    try:
        browser.find_element_by_class_name('rooms-selector').click()
    except:
        browser.find_element_by_xpath('//*[@id="availability-form"]/fieldset/div[3]/div/label/').click()
    browser.find_element_by_xpath('//*[@id="availability-form"]/fieldset/div[3]/div/label/select/option['+str(no_of_rooms)+']').click()
    counter=no_of_adults
    counter_children=no_of_children
    number_of_children_processed=0
    ## change li:nth-child(4) to change the number of rooms
    x=0
    for x in range(0,no_of_rooms):   
        try:
            browser.find_element_by_xpath('//*[@id="rm-adults-'+str(x)+'"]/select"]').click()
        except:
            browser.find_elements_by_class_name('adult-selector')[x].click()
        #### hotel-#-adults selects the room number
        no_of_adults_in_the_room=round(math.ceil(counter/no_of_rooms),0)
        counter=counter-no_of_adults_in_the_room
        no_of_children_in_the_room=round(math.ceil(counter_children/no_of_rooms),0)
        counter_children=counter_children-no_of_children_in_the_room
        browser.find_element_by_xpath('//*[@id="rm-adults-'+str(x)+'"]/select/option['+str(no_of_adults_in_the_room)+']').click() 
        ### minimum value in adults is 1 whereas in children is 0
        browser.find_element_by_xpath('//*[@id="rm-children-'+str(x)+'"]/select').click()
        browser.find_element_by_xpath('//*[@id="rm-children-'+str(x)+'"]/select/option['+str(no_of_children_in_the_room+1)+']').click() ## Value of Option[1]== 0 children
        if no_of_children_in_the_room>=1:
            interim_counter=no_of_children_in_the_room
            child_number=1
            while (child_number<=interim_counter):
                ##child age picker  (Will appear only when # of children is >0)
                try:
                    browser.find_elements_by_class_name('child-age-selector')[number_of_children_processed+1].click()
                except:
                    browser.find_element_by_xpath('//*[@id="childAge'+str(child_number-1)+'Room'+str(x+1)+'"]').click()
                browser.find_element_by_xpath('//*[@id="childAge'+str(child_number-1)+'Room'+str(x+1)+'"]/option['+str(random.randint(1, 15))+']').click() ## first 2 values in this are Age & Under 1 then 1 and 2 onwards
                child_number=child_number+1
                number_of_children_processed=number_of_children_processed+1
                time.sleep(1)
        else:
            print("no Children")
    print("line 122, room selected")

def date_selector_dropdown(browser,checkin_date,checkout_date):
    #if previous_checkin_date!=checkin_date:
    abcd=date_matrix_calculator(checkin_date,"today","monday")
    try:
        try:
            browser.find_element_by_xpath('//*[@id="choose-dates-button"]').click()
            print("Checkin date dropdown selected")
        except:
            browser.find_element_by_xpath('//*[@id="availability-check-in"]').click()
            #print("422")
    except:
        try:
            browser.find_element_by_css_selector('#availability-check-in-label > span.icon.icon-calendar').click()
            #print("Checkin date dropdown selected - Except")
        except:
            browser.implicitly_wait(2)
            time.sleep(2)
            browser.refresh
            try:
                browser.find_element_by_xpath('//*[@id="modalCloseButton"]').click()
                #print("Pop Up closed")
            except:
                pass
                #print("435")                   
            try:
                browser.find_element_by_xpath('//*[@id="availability-check-in"]').click()
            except:
                browser.find_element_by_css_selector('#availability-check-in-label > span.icon.icon-calendar').click()
            if browser.find_element_by_xpath('//*[@id="startDate"]/div/div/button[2]').text=="next month":
                pass
            else:
                try:
                    browser.find_element_by_xpath('//*[@id="availability-check-in"]').click()
                except:
                    browser.find_element_by_css_selector('#availability-check-in-label > span.icon.icon-calendar').click()
    print("Checkin date selected")
    try:
        browser.find_element_by_xpath('//*[@id="availability-check-in-label"]/span[2]').click()
        #print("449")
    except:
        WebDriverWait(browser, 1, poll_frequency=0.1).\
            until(lambda drv: len(browser.find_element_by_xpath('//*[@id="startDate"]/div/div/div[2]/table/caption').text) > 0)
        browser.find_element_by_xpath('//*[@id="availability-check-in-label"]/span[2]').click()
        #print("454")
    if abcd['no_of_clicks_on_next']<=0:
        try:
            browser.find_element_by_xpath('//*[@id="startDate"]/div/div/div['+str(abcd['div_value'])+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
        except NoSuchElementException:
            browser.implicitly_wait(5)
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="startDate"]/div/div/div['+str(abcd['div_value'])+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
        except:
            #browser.implicitly_wait(10)
            #time.sleep(10)
            browser.find_element_by_css_selector('#startDate > div > div > div:nth-child('+str(abcd['div_value']+2)+') > table > tbody > tr:nth-child('+str(abcd['row_value'])+') > td:nth-child('+str(abcd['col_value'])+') > button').click()
        #print("468")
    else:
        while abcd['no_of_clicks_on_next']>0: 
            browser.find_element_by_xpath('//*[@id="startDate"]/div/div/button[2]').click()
            abcd['no_of_clicks_on_next']=abcd['no_of_clicks_on_next']-1
        #print("473")
        try:
            browser.find_element_by_xpath('//*[@id="startDate"]/div/div/div['+str(abcd['div_value'])+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
        except:
            browser.find_element_by_css_selector('#startDate > div > div > div:nth-child('+str(abcd['div_value']+2)+') > table > tbody > tr:nth-child('+str(abcd['row_value'])+') > td:nth-child('+str(abcd['col_value'])+') > button').click()            
	##//*[@id="hotel-checkin-wrapper"]/div/div/div[2]/table/tbody/tr[4]/td[5]/button        	   
    #else:
        #pass                
	##To change month
	##//*[@id="hotel-checkin-wrapper"]/div/div/button[2]
	##change div[#] to change month & change tr[row number]/td[column number] for changing date
    #if previous_checkout_date!=checkout_date:
    if abcd['div_value']==2:
        div_value_exit=2
    else:
        div_value_exit=3
    abcd=date_matrix_calculator(checkout_date,checkin_date,"monday")
    #print("487")
    div_value_exit=abcd['div_value']
    try:
        try:
            browser.find_element_by_xpath('//*[@id="availability-check-out-label"]').click()
            #print("492")
        except:
            browser.find_element_by_xpath('//*[@id="availability-check-out"]').click()
            #print("495")
    except:
        try:
            browser.find_element_by_css_selector('#availability-check-out-label > span.icon.icon-calendar').click()
            #print("499")
        except:
            browser.find_element_by_css_selector('#availability-check-out').click()
            #print("502")
    if abcd['no_of_clicks_on_next']<=0:
        try:
            browser.find_element_by_xpath('//*[@id="endDate"]/div/div/div['+str(div_value_exit)+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
        except:
            browser.implicitly_wait(2)
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="endDate"]/div/div/div['+str(div_value_exit)+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()                    
        #print("line 498, choosing dates")
    else:
        while abcd['no_of_clicks_on_next']>0: 
            browser.find_element_by_xpath('//*[@id="hotel-checkout-wrapper"]/div/div/button[2]').click()
            abcd['no_of_clicks_on_next']=abcd['no_of_clicks_on_next']-1
    print("line 512, selecting end date")
    
    try:
        browser.find_element_by_xpath('//*[@id="endDate"]/div/div/div['+str(div_value_exit)+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
    except:
        try:
            browser.find_element_by_css_selector('#availability-check-out-label > span.icon.icon-calendar').click()
            #print("521")
        except:
            browser.find_element_by_css_selector('#availability-check-out').click()
            #print("524")
        try:     
            browser.implicitly_wait(2)
            #time.sleep(3)                        
            browser.find_element_by_xpath('//*[@id="endDate"]/div/div/div['+str(div_value_exit)+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
        except:
            browser.implicitly_wait(5)
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="endDate"]/div/div/div['+str(div_value_exit)+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()
            except:
                time.sleep(3)
                browser.find_element_by_css_selector('#availability-check-out-label > span.icon.icon-calendar').click()                            
                browser.find_element_by_xpath('//*[@id="endDate"]/div/div/div['+str(div_value_exit)+']/table/tbody/tr['+str(abcd['row_value'])+']/td['+str(abcd['col_value'])+']').click()                            

#if availability error or sold out error then nothing, all prices Null. else trigger the function
def hotel_data_extractor(webdriver_path,hotel_url,no_of_rooms,no_of_adults,no_of_children,checkin_date,checkout_date):
    warnings.simplefilter(action = "ignore", category = RuntimeWarning)
    if bool(re.search("phantomjs",webdriver_path)):
        browser = webdriver.PhantomJS(executable_path=webdriver_path, service_log_path=os.path.devnull)
        browser.set_window_size(1400, 1000)
    else:
        browser = webdriver.Chrome(webdriver_path)
    hotel_url=hotel_url.split("?chkin")[0]
    browser.get(hotel_url)
    try:
        browser.find_element_by_xpath('//*[@id="modalCloseButton"]').click()
        #print("612")
    except:
        pass
        #print("614")
    	#choosing dates
    #abcd=date_matrix_calculator(checkin_date,"today","monday")
    try:
        browser.find_element_by_xpath('//*[@id="modalCloseButton"]').click()
        #print("618")
    except:
        pass                
    try:
        location_element=browser.find_element_by_xpath('//*[@id="availability-check-in"]')            
        browser.execute_script("window.scrollTo(0,"+str((location_element.location['y']-100))+");")                
        #print("623")
        try:            
            date_selector_dropdown(browser,checkin_date,checkout_date)
        except:
            browser_current_url=browser.current_url
    except:
        browser_current_url=browser.current_url
        if bool(re.search("travelads",browser_current_url)):
            browser.get(hotel_url)
            try:
                browser.find_element_by_xpath('//*[@id="modalCloseButton"]').click()
            except:
                pass
            try:
                date_selector_dropdown(browser,checkin_date,checkout_date)
                #print("618")
            except:
                browser.find_element_by_xpath('//*[@id="modalCloseButton"]').click()
                location_element=browser.find_element_by_xpath('//*[@id="availability-check-in"]')            
                browser.execute_script("window.scrollTo(0,"+str((location_element.location['y']-100))+");")                
                date_selector_dropdown(browser,checkin_date,checkout_date)
                #print("623")                    
        else:
            browser.implicitly_wait(3)
        		#time.sleep(5)
            date_selector_dropdown(browser,checkin_date,checkout_date)
    room_selector(browser,no_of_rooms,no_of_adults,no_of_children)
    try:
        browser.find_element_by_xpath('//*[@id="update-availability-button"]').click()
    except:
        browser.implicitly_wait(3)
        browser.find_element_by_xpath('//*[@id="update-availability-button"]').click()
    try:
        error_msg=browser.find_element_by_xpath('//*[@id="availability-errors"]/p').text
    except:
        error_msg="rooms_available"
    if bool(re.search("no rooms available",error_msg)) or bool(re.search("exceed",error_msg)) or bool(re.search("longer",error_msg)):
        booking_datetime=str(datetime.date.today())
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        domain="expedia.com"
        sold_out_flag=int(bool(re.search("no rooms available",error_msg)))
        exceeds_allowed_guests_flag=int(bool(re.search("exceed",error_msg)))
        interim_data=pd.DataFrame([[None,None,no_of_rooms,no_of_adults,no_of_children,booking_datetime,checkin_date,checkout_date,None,ip_address,domain,"NA",sold_out_flag,exceeds_allowed_guests_flag,None,None,None,None,None,None,None,None]],
        columns=['room_name','room_id','no_of_rooms','no_of_adults','no_of_children','booking_datetime','checkin_date','checkout_date','breakfast','ip_address','domain','perc_rooms_booked','sold_out_flag','exceeds_guests_flag','rooms_available','reserve_now_pay_later_flag','free_cancellation_flag','non_refundable_flag','refundable_flag','no_expedia_booking_fee_flag','price_type','price_shown'])
        browser.close
    else:
        hotel_name=browser.find_element_by_id('hotel-name').text
        interim_data=pd.DataFrame()
        hotel_room_interim_data=pd.DataFrame()
        print("line 133, scraping for hotel="+str(hotel_name))
        try:
            price_type=browser.find_element_by_class_name('nights-over-lead-price').text
        except:
            price_type=None
        try:
            displayed_price=str(browser.find_element_by_xpath('//*[@id="lead-price-container"]/div/div[1]/a').text.replace("more",""))
            displayed_price_1=displayed_price.split("\n")
            bool_price=[bool(re.search("Rs|INR", i)) for i in displayed_price_1]
            if sum(bool_price)>=1:
                currency="INR"
            else:
                currency="Other"
            displayed_price_1=displayed_price[displayed_price.find("Rs"):]
            displayed_price=re.sub("[^0-9]","",displayed_price_1)
        except:
            displayed_price=None
        try:
            perc_rooms_booked=browser.find_element_by_xpath('//*[@id="hotelCompressionAlert"]/div[1]/div[1]').text
        except:
            perc_rooms_booked=None        
        number_of_room_types=len(browser.find_elements_by_xpath('//*[@id="rooms-and-rates"]/div/article/table/tbody'))
        ##y=2
        room_names=browser.find_elements_by_class_name('room-name')
        room_prices=browser.find_elements_by_class_name('room-price')
        print("line 215, hotel level info scraped")
        roomratefeatures=browser.find_elements_by_class_name('rate-features')
        counter=0
        for y in range(1,number_of_room_types+1):
            number_of_prices_per_room_type=len(browser.find_elements_by_xpath('//*[@id="rooms-and-rates"]/div/article/table/tbody['+str(y)+']/tr'))
            #z=1
            #print("line 219, scraping for room number "+str(y))
            for z in range(1,(number_of_prices_per_room_type+1)):
                try:
                    room_info=list(map(lambda x:x.lower(),browser.find_element_by_xpath('//*[@id="rooms-and-rates"]/div/article/table/tbody['+str(y)+']/tr['+str(z)+']').text.split("\n")))
                except:
                    room_info=[]
                try:
                    room_info1=list(map(lambda x:x.lower(),browser.find_element_by_xpath('//*[@id="rooms-and-rates"]/div/article/table/tbody['+str(y)+']/tr['+str(z)+']/td[2]').text.split("\n")))
                except:
                    room_info1=[]
                try:
                    room_info2=list(map(lambda x:x.lower(),browser.find_element_by_xpath('//*[@id="rooms-and-rates"]/div/article/table/tbody['+str(y)+']/tr['+str(z)+']/td[1]').text.split("\n")))                        
                except:
                    room_info2=[]
                room_info=room_info+room_info1+room_info2
                room_info=list(set(room_info))   
                try:
                    room_name=room_names[y-1].text
                except:
                    room_name=room_names[y-2].text
                #print("line 232, room level information to be scraped")
                room_id=str(hotel_name)+"_"+str(room_name)[:3]+"_"+str(room_name[-3:])
                interim_rate_features=roomratefeatures[y+z-2].text
                try:
                    no_expedia_booking_fee=bool(re.search("No Expedia booking fees", interim_rate_features))*1
                except:
                    no_expedia_booking_fee=None
                try:
                    sold_out_flag=len(list(compress(room_info,[bool(re.search("sold out", i)) for i in room_info])))  
                except:
                    sold_out_flag=0
                #print("line 263")
                try:
                    exceeds_allowed_guests_flag=len(list(compress(room_info,[bool(re.search("exceeds max guests", i)) for i in room_info])))
                except:
                    exceeds_allowed_guests_flag=0
                #try:
                    #rooms_available=list(compress(room_info,[bool(re.search("rooms left", i)) for i in room_info]))[0].replace("we have ","").replace(" rooms left","")
                #except:
                    #rooms_available=None
                try:
                    breakfast=len(list(compress(room_info,[bool(re.search("breakfast", i)) for i in room_info])))
                except:
                    breakfast=0
                try:
                    price_shown=room_prices[counter].text              
                except:
                    if sold_out_flag!=0:
                        price_shown="Sold Out"
                    elif exceeds_allowed_guests_flag!=0:
                        price_shown="Exceeds maximum possible guests"
                    else:
                        price_shown=None
                #print("line 291")
                try:
                    rate_type=set(list(compress(room_info,[bool(re.search("rate|per night", i)) for i in room_info])))
                    noise=set(list(compress(room_info,[bool(re.search("information", i)) for i in room_info])))
                    rate_type=rate_type ^ noise
                    rate_type=str(list(rate_type)[0])
                except:
                    rate_type=None
                try:
                    non_refundable_flag=len(list(compress(room_info,[bool(re.search("non-refundable", i)) for i in room_info])))
                    refundable_flag=len(list(compress(room_info,[bool(re.search("refundable", i)) for i in room_info])))
                    if refundable_flag<=non_refundable_flag:
                        refundable_flag=0
                    else:
                        refundable_flag=1
                except:
                    non_refundable_flag=None
                try:
                    free_cancellation_flag=bool(re.search("Free Cancellation", interim_rate_features))*1
                except:
                    free_cancellation_flag=0
                try:
                    reserve_now_pay_later_flag=bool(re.search("Reserve now, pay later", interim_rate_features))*1
                except:
                    reserve_now_pay_later_flag=0
                #print("line 316")
                booking_datetime=str(datetime.date.today())
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                domain="expedia.com"
                #print("line 403")            
                interim_data=pd.DataFrame([[room_name,room_id,no_of_rooms,no_of_adults,no_of_children,booking_datetime,checkin_date,checkout_date,breakfast,ip_address,domain,perc_rooms_booked,sold_out_flag,exceeds_allowed_guests_flag,reserve_now_pay_later_flag,free_cancellation_flag,non_refundable_flag,refundable_flag,no_expedia_booking_fee,price_type,price_shown]],
                                          columns=['room_name','room_id','no_of_rooms','no_of_adults','no_of_children','booking_datetime','checkin_date','checkout_date','breakfast','ip_address','domain','perc_rooms_booked','sold_out_flag','exceeds_guests_flag','reserve_now_pay_later_flag','free_cancellation_flag','non_refundable_flag','refundable_flag','no_expedia_booking_fee_flag','price_type','price_shown'])
                #final_data.to_csv("C:/Users/test/Desktop/Scraping/Tripadvisor/List_of_cities/price_info.txt",sep="|")
                #hotel_room_interim_data=pd.DataFrame([[hotel_name,hotel_id,hotel_url,domain,ip_address,tripadvisor_reviews,tripadvisor_rating,recommend_percentage,expedia_reviews,expedia_user_rating,hotel_rating,room_name,room_id,booking_datetime,extra_bed,double_bed_size,single_bed_size,num_guest_allowed,num_adult_allowed,num_child_allowed,room_size,room_with_view,rate_type,free_internet,tv_available,balcony_view,massage,bottled_water,bedding_type,bathroom_type,bathtub_flag,newspaper_flag,desk_flag,phone_flag,Non_Smoking_flag,airconditioning_type,fitness_center,restaurant,bar_lounge,steam_room,rooftop_terrace,parking,soundproof_rooms,swimming_pool]]
                #,columns=['hotel_name','hotel_id','hotel_url','domain','ip_address','tripadvisor_reviews','tripadvisor_rating','recommend_percentage','expedia_reviews','expedia_user_rating','hotel_rating','room_name','room_id','booking_datetime','extra_bed','double_bed_size','single_bed_size','num_guest_allowed','num_adult_allowed','num_child_allowed','room_size','room_with_view','rate_type','free_internet','tv_available','balcony_view','massage','bottled_water','bedding_type','bathroom_type','bathtub_flag','newspaper_flag','desk_flag','phone_flag','Non_Smoking_flag','airconditioning_type','fitness_center','restaurant','bar_lounge','steam_room','rooftop_terrace','parking','soundproof_rooms','swimming_pool'])
                #hotel_room_data.to_csv("C:/Users/test/Desktop/Scraping/Tripadvisor/List_of_cities/hotel_room_info.txt",sep="|")
                counter=counter+1
                print("price extracted for room"+str(counter))
                if price_shown==None:
                    pass
                else:
                    hotel_room_interim_data=hotel_room_interim_data.append(interim_data)
        browser.quit()
        return hotel_room_interim_data
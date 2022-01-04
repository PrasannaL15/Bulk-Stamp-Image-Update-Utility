import urllib.request
from numpy import isnan, product
# importing openpyxl module
import pandas as pd
import warnings
import os

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
 


def getFile(url,publisher_name,product_name):

    
    publisher_name = publisher_name.replace(' ','_')
    url = str(url)
    url = url.rstrip() 
    url = url.lstrip()
    if(url == ""):
        print("Empty stamp image for "+product_name)
        return(False,'junk')
    
  
    if(url.startswith('/dotcom/')):
        url = 'https://learning.tcsionhub.in'+url.replace('/','//')
        if not os.path.exists('Stamp_Image_Update'):
            os.makedirs('Stamp_Image_Update')
        if not os.path.exists('Stamp_Image_Update/'+publisher_name):
            os.makedirs('Stamp_Image_Update/'+publisher_name)
        try:
            product_name = product_name.replace(' ','_')
            product_name = ''.join(e for e in product_name if e.isalnum() or e=='_')
            if(url.endswith(".jpg") or url.endswith(".JPG") ):
                output_path = 'Stamp_Image_Update/'+publisher_name+'/'+product_name+'_Stamp.jpg'
                urllib.request.urlretrieve(url=url,filename=output_path)
            elif(url.endswith(".png")):
                output_path = 'Stamp_Image_Update/'+publisher_name+'/'+product_name+'_Stamp.png'
                urllib.request.urlretrieve(url,output_path)
            elif(url.endswith(".jpeg") or url.endswith(".JPEG")):
                output_path = 'Stamp_Image_Update/'+publisher_name+'/'+product_name+'_Stamp.jpeg'
                urllib.request.urlretrieve(url,output_path)
            print("got file "+product_name)
            
            return (True,output_path)
        except Exception as e:
            print(url)
            print(e)
    elif(url.startswith('https://cdn4.tcsion.com/')):
        #url = 'https://learning.tcsionhub.in'+url.replace('https://cdn4.tcsion.com/','/')
        if not os.path.exists('Stamp_Image_Update'):
            os.makedirs('Stamp_Image_Update')
        if not os.path.exists('Stamp_Image_Update/'+publisher_name):
            os.makedirs('Stamp_Image_Update/'+publisher_name)
        try:
            product_name = product_name.replace(' ','_')
            product_name = ''.join(e for e in product_name if e.isalnum() or e=='_')
            if(url.endswith(".jpg") or url.endswith(".JPG") ):
                output_path = 'Stamp_Image_Update/'+publisher_name+'/'+product_name+'_Stamp.jpg'
                urllib.request.urlretrieve(url=url,filename=output_path)
            elif(url.endswith(".png")):
                output_path = 'Stamp_Image_Update/'+publisher_name+'/'+product_name+'_Stamp.png'
                urllib.request.urlretrieve(url,output_path)
            elif(url.endswith(".jpeg") or url.endswith(".JPEG")):
                output_path = 'Stamp_Image_Update/'+publisher_name+'/'+product_name+'_Stamp.jpeg'
                urllib.request.urlretrieve(url,output_path)
            print("got file "+product_name)
            
            return (True,output_path)
        except Exception as e:
            print(url)
            print(e)
    else:
        print("already in base"+product_name)
        return(False,'junk')
       
def readexcel():
    #Required for ignoring warning messages
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        #path of the input file
        path = "input.xlsx"
        
        #Loading excel sheet as dataframe object
        df_out = pd.read_excel(path)
        
        #Selecting concerned columns in dataframe
        df = df_out[['Product Name','Thumbnail Image Path','Publisher Name','Product Status']].dropna()
        
        #selecting products with Status Active
        df = df.loc[df['Product Status'] == 'Active']
        df = df.head(200)  #selecting only top 200 for testing purpose

        #for each product extracting values
        for url, publisher_name,product_name in zip(df['Thumbnail Image Path'], df['Publisher Name'],df['Product Name']):
            #current product which is send for processing
            print(url, publisher_name,product_name)

            #Function call for saving file in respective publisher's folder and getting new URL path
            flag_path = getFile(url, publisher_name,product_name) 
            if(flag_path[0] == True):
                df_out.loc[ df_out['Product Name']==product_name, ['Thumbnail Image Path']] = '/per/g01/pub/1016/iDH/instance/4/template/83/temp/template/'+flag_path[1]
    df_out.to_excel("output.xlsx", index=False)
readexcel()

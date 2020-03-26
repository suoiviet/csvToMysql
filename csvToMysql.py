import json
import mysql.connector
from mysql.connector import errorcode
import csv
from datetime import datetime

#get configuration settings from config.json
with open('config.json') as json_data_file:
  data = json.load(json_data_file)
#print(data)
#print("host:"+data["mysql"]["host"])

host = data["mysql"]["host"]
user = data["mysql"]["user"]
passwd = data["mysql"]["passwd"]
db = data["mysql"]["db"]
table = data["table"]
filecsv = data["csv"]

try:
  #establish connection
  connection = mysql.connector.connect(host=host, user=user, password=passwd, database=db)

  #create a cursor
  mycursor = connection.cursor()

  #build sql string******
  sql = ""
  strInsertFld = ""
  strInsertPlaceHld = ""
  listInsertVal = list()
  listFieldFormat = list()
  listFieldAsDate = list()
  i = 0
  for x in data["fields"]:
    #going thru getting fields info from config (to see if there are any format consideration)
    strField = x["name"]

    #getting optional fields
    strFormat = ""
    strFieldAsDate = ""
    ##strFieldAsDate is used to store value from "fieldasdate" attribute coming from config.json
    ##"fieldasdate" indicates the field will be converted to a date field (instead of text) when inserted into MySql
    ##If the MySQL's field that's storing the csv's field is a date field, then need convert the csv to a date (otherwise if MySQL field is text/char don't need to do anything)... 
    ##do this by identifying the date format that the csv field is using
    ##"fieldasdate" in config.json is the date format the csv field represents, see file "strptimeDateFormatCodes.txt" for proper Date Format codes for "fieldasdate"
    ##example 1, if the value of the "findate" field in "annual-bs.csv" is something like "12/31/2008"...
    ##and the user wants to import this into a MYSQL date field, then config.json needs to have: 
    ##{"name":"findate", "fieldasdate":"%m/%d/%Y"}
    if "format" in x:
      strFormat = x["format"]
    if "fieldasdate" in x:
      strFieldAsDate = x["fieldasdate"]
    listFieldFormat.append(strFormat)
    listFieldAsDate.append(strFieldAsDate)


    #print("field:" + strField + " format:" + strFormat)
    if strInsertFld == "":
      strInsertFld = strField
      strInsertPlaceHld = "%s"
    else:
      strInsertFld += ", " + strField
      strInsertPlaceHld += ", " + "%s"

  #INSERT statement header & placeholder
  strInsertFld = "(" + strInsertFld + ")"
  strInsertPlaceHld = "(" + strInsertPlaceHld + ")"
  #test
  #strInsertPlaceHld = "(%s, %s, %s, %s, %s, %s, %s, %s)"

  sql = "INSERT IGNORE INTO " + table + " " + strInsertFld + " VALUES " + strInsertPlaceHld + " "

  #loop csv file and build list of values (listInsertVal) for all fields in each row
  #placeholders (%s) used for parameters will ensure sql injection is taken care of
  #although with this script, there's not alot of worries for injections b/c there are no user inputs to worry
  with open(filecsv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #skip first line
            line_count += 1
        else:
            #loop thru each field from each record, build values to insert into db
            i = 0
            end = len(row)
            while i < end:
                val = row[i]

                #for handling custom format of the fields, add code here**
                #if listFieldFormat[i] != "":
              


                #for storing the field as a date field (MySql Date field will store any date as YYYY-MM-DD)
                #here specify the date format the csv field is using (strptime 2nd parameter) if the MySQL field storing this value is a date field
                #see file "strptimeDateFormatCodes.txt" for proper Date Format codes
                if listFieldAsDate[i] != "":
                    val = datetime.strptime(val, listFieldAsDate[i])
                    
                #add to list of values (Python list) to be included in INSERT statement
                listInsertVal.append(val)
                i += 1

            #execute the INSERT statement
            mycursor.execute(sql, listInsertVal)
            listInsertVal.clear() #clear items from list, to prepare for next iteration of values

            line_count += 1
    
  #ends csv loop


  #commit inserts to DB
  connection.commit()
  print(str(line_count) + " records inserted.")
  
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
  
  #quit script
  exit()
else:
  #run after try completed w/o errors
  connection.close()


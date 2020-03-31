# CSV To MySQL
This python script extracts data from a csv file and import them into a MySQL table.

## Executing the script
1. Make sure you have this installed:
	- Python
2. Create the MySQL table that will hold the data for your csv file. Make sure the table have all the fields specified in the csv file.
2. Provide your MySQL credentials in config.json, under "mysql" key. Under "table" & "fields", provide the MySQL table name & fields receiving the import; "name" is required and need to match the field name coming from the table. The "csv" key will need a filename of the source csv.
3. Open Terminal and change the directory to the location of csvToMysql.py. Run csvToMysql.py (there exists different syntaxes for executing Python scripts, depending on the Python version and OS you're running on)
4. When the script finished, the data from the source csv will be imported to the MySQL table specifed in config.json

## Samples

There's a sample "annual-bs.csv" and "annual-bs.sql" in the root directory. "annual-bs.sql" can be used and imported into MySQL to create the "annual" table to hold the data for "annual-bs.csv". 

Additional samples can be found in the "examples" folder.

If the user wants a field imported as a MySQL date field (instead of varchar, char, text field), he/she can use the optional "fieldasdate" attribute belonging to the "field" key in config.json. The "fieldasdate" attribute would need to represent the Date Format of the csv's field that's to be imported as a date field. For reference, there is a file called strptimeDateFormatCodes.txt" in the root directory that contains the Date Format codes which can be used to construct the "fieldasdate". These Date Format codes are also the codes used in Python's strptime function (from the datetime module).

For example: 

The value of the "findate" field in "annual-bs.csv" is "12/31/2008" and if the user wants to import this into a MYSQL date field, then config.json needs to have: {"name":"findate", "fieldasdate":"%m/%d/%Y"}

See additional "fieldasdate" examples in the sample config files found in "examples" sub folder.
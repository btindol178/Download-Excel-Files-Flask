from flask import Flask ,render_template,request,redirect,url_for,send_file,abort
#from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import pyodbc          
import pandas as pd
import os
from datetime import datetime   
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import time
from datetime import timedelta
import sqlite3
from sqlite3 import Error
import io
from io import BytesIO

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'sdflksjslksajfsda' # NOT KOSSURE BUT FOR NOW

# Run app through sql alchemy and marshmallow 
db = SQLAlchemy(app)

# Create tables at first
@app.before_first_request
def create_tables():
    db.create_all() 


conn_str = ('DRIVER={SQL Server};'
    'SERVER=<server name>;'
    'DATABASE=<database name>;'
    'Trusted_Connection=yes;')

cnxn = pyodbc.connect(conn_str)

@app.route("/home",methods =['GET','POST'])
def home():
    df = "select top 10 dv.DIVISION, p.BUSINESS_UNIT, st.CUSTNAME, p.PRODUCT_GROUP_NAME, o.QTY, o.EXTENDED_AMT from hcs_discover.dw.factorders o left join HCS_DISCOVER.dw.DimProducts p on p.id = o.PRODUCT_ID left join HCS_DISCOVER.dw.DimShipTo st on st.id = o.SHIP_TO_ID left join HCS_DISCOVER.DW.DimDivision dv on dv.ID = o.DIV_ID where p.BUSINESS_UNIT IN('{}') and p.PRODUCT_GROUP_NAME IN('{}')".format('Orthopaedic Instruments','LB Cut Access')
    predata = pd.read_sql(df, cnxn)
    print(predata)
    tables = predata.to_html(classes='table table-striped', header="true", index=False)
    if request.method == "POST":
   
        df = "select top 10 dv.DIVISION, p.BUSINESS_UNIT, st.CUSTNAME, p.PRODUCT_GROUP_NAME, o.QTY, o.EXTENDED_AMT from hcs_discover.dw.factorders o left join HCS_DISCOVER.dw.DimProducts p on p.id = o.PRODUCT_ID left join HCS_DISCOVER.dw.DimShipTo st on st.id = o.SHIP_TO_ID left join HCS_DISCOVER.DW.DimDivision dv on dv.ID = o.DIV_ID where p.BUSINESS_UNIT IN('{}') and p.PRODUCT_GROUP_NAME IN('{}')".format('Orthopaedic Instruments','LB Cut Access')
        predata = pd.read_sql(df, cnxn)
        print(predata)
        tables = predata.to_html(classes='table table-striped', header="true", index=False)

        output = BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            predata.to_excel(writer, sheet_name="Sheet1")

        output.seek(0)

        return send_file(output, attachment_filename="df.xlsx", as_attachment=True) 
    return render_template("index.html",tables=tables)


@app.route("/",methods =['GET','POST'])
@app.route("/download_file",methods =['GET','POST'])
def download_file():
    if request.method == 'POST':
        
        return redirect(url_for('home'))
    return render_template("download.html")


if __name__ == "__main__":
    app.run(debug=True)
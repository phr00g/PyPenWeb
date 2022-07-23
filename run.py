
from flask import Flask, render_template, request
import os
import socket
import requests
import nmap 

scanner = nmap.PortScanner()





# initializes Flask
app = Flask(__name__)

#creates necessary socket object for network activity
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#returns array with strings of found subdirectories
def dirb(fixed_name):
    check_list = ["/robots.txt" , "/sitemap.xml" , "/admin" , "/wp-admin" , "/cpanel" ]
    temp = []
    for directory in check_list:
        more_fixed = fixed_name + directory
        respy = requests.get(more_fixed)
        head = get_head(respy)
        if(head==200):
            temp.append(fixed_name + directory)
    return temp




# returns HTTP response code from given response
def get_head(respo):
    temp = str(respo)
    g = int(temp[11:14])
    return g



#just adds https:// at beginning of given hostname
def fixed_name(given):
    fixer = "https://" + given
    return fixer



#site landing page with name
@app.route('/')
def index():
    return render_template('index.html')



#has form for user to input DNS name for scanning
@app.route('/pypen')
def test():
    return render_template('pypen.html')



#result page with scan insights
@app.route('/ppresult' , methods=['POST' , 'GET'])
def scan():
    if request.method == 'POST':
        
        k = request.form
        dns = k['dnsName']
        ip = socket.gethostbyname(dns)
        fixed = fixed_name(dns)

        found = dirb(fixed)



        #pypen.html form creates Json object/dictionary
        return render_template('result.html' , ip=ip , dns=dns , fixed=fixed , found=found)






if __name__ == "__main__":
    app.run(debug=True)
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
from django.core.files.storage import FileSystemStorage
import pickle
from hashlib import sha256
import pyaes, pbkdf2, binascii, secrets
import base64
import timeit

global usersList, educationList

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'MyEduContract.json' #Smart Contract to manage education data details
    deployed_contract_address = 'Your_Contract_Address' #contract address' 
     
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUsersList():
    global usersList, contract
    usersList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        user = contract.functions.getUsername(i).call()
        password = contract.functions.getPassword(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        address = contract.functions.getAddress(i).call()
        utype = contract.functions.getUserType(i).call()
        usersList.append([user, password, phone, email, address, utype])

def getEducationList():
    global educationList, contract
    educationList = []
    count = contract.functions.getEducationCount().call()
    for i in range(0, count):
        address = contract.functions.getLMSAddress(i).call()
        desc = contract.functions.getLMSDesc(i).call()
        course = contract.functions.getCourse(i).call()
        data_type = contract.functions.getType(i).call()
        data_desc = contract.functions.getDescription(i).call()
        certificate = contract.functions.getCertificate(i).call()
        dd = contract.functions.getDate(i).call()
        educationList.append([address, desc, course, data_type, data_desc, dd, certificate])
getUsersList()
getEducationList()

def getKey(): #generating AES key based on Diffie common secret shared key
    password = "s3cr3t*c0d3"
    passwordSalt = str("0986543")#get AES key using diffie
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key

def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def DownloadFileDataRequest(request):
    if request.method == 'GET':
        global fileList
        filename = request.GET.get('hash', False)
        with open("EducationApp/static/certificates/"+filename, "rb") as file:
            data = file.read()
        file.close()
        decrypted = decrypt(data)
        response = HttpResponse(decrypted,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response

def AccessData(request):
    if request.method == 'GET':
       return render(request, 'AccessData.html', {})

def AccessDataAction(request):
    if request.method == 'POST':
        global username, contract, educationList
        address = request.POST.get('username')
        strdata = '''
        <div class="overflow-x-auto">
        <table class="table-auto w-full border border-gray-600 text-white text-sm">
          <thead>
            <tr>
              <th class="border px-4 py-2">Address</th>
              <th class="border px-4 py-2">LMS Description</th>
              <th class="border px-4 py-2">Course Name</th>
              <th class="border px-4 py-2">Data Type</th>
              <th class="border px-4 py-2">Data Description</th>
              <th class="border px-4 py-2">Upload Date</th>
              <th class="border px-4 py-2">Certificate Name</th>
              <th class="border px-4 py-2">Download Certificate</th>
            </tr>
          </thead>
          <tbody>
        '''
        for flist in educationList:
            if address == flist[0]:
                strdata += f'''
                <tr>
                  <td class="border px-4 py-2">{flist[0]}</td>
                  <td class="border px-4 py-2">{flist[1]}</td>
                  <td class="border px-4 py-2">{flist[2]}</td>
                  <td class="border px-4 py-2">{flist[3]}</td>
                  <td class="border px-4 py-2">{flist[4]}</td>
                  <td class="border px-4 py-2">{flist[5]}</td>
                  <td class="border px-4 py-2">{flist[6]}</td>
                  <td class="border px-4 py-2 whitespace-nowrap">
                    <a href="DownloadFileDataRequest?hash={flist[6]}" class="text-blue-400 hover:underline inline-block">Download File</a>
                  </td>
                </tr>
                '''
        strdata += '</tbody></table></div>'
        context = {'data': strdata}
        return render(request, 'ViewAccessData.html', context)

  

def ViewData(request):
    if request.method == 'GET':
        global  username, educationList
        address = sha256(username.encode()).hexdigest()
        strdata = '<table border=1 align=center width=100%><tr><th><font size="" color="white">Address</th>'
        strdata+='<th><font size="" color="white">LMS Description</th><th><font size="" color="white">Course Name</th>'
        strdata+='<th><font size="" color="white">Data Type</th><th><font size="" color="white">Data Description</th>'
        strdata+='<th><font size="" color="white">Upload Date</th><th><font size="" color="white">Certificate Name</th>'
        strdata+='<th><font size="" color="white">Download Certificate</th></tr>'
        address = sha256(username.encode()).hexdigest()
        for i in range(len(educationList)):
            flist = educationList[i]            
            if address == flist[0]:
                strdata+='<tr><td><font size="" color="white">'+str(flist[0])+'</td><td><font size="" color="white">'+flist[1]+'</td><td><font size="" color="white">'+str(flist[2])+'</td>'
                strdata+='<td><font size="" color="white">'+str(flist[3])+'</td>'
                strdata+='<td><font size="" color="white">'+str(flist[4])+'</td>'
                strdata+='<td><font size="" color="white">'+str(flist[5])+'</td>'
                strdata+='<td><font size="" color="white">'+str(flist[6])+'</td>'
                strdata+='<td><a href=\'DownloadFileDataRequest?hash='+flist[6]+'\'><font size=3 color=white>Download File</font></a></td></tr>'                
        context= {'data':strdata}
        return render(request, 'ViewStudentData.html', context)       

def ShareDataAction(request):
    if request.method == 'POST':
        global username, contract, educationList
        lms_desc = request.POST.get('t1')
        course = request.POST.get('t2')
        data_type = request.POST.get('t3')
        data_desc = request.POST.get('t4')
        filename = request.FILES['t5'].name
        myfile = request.FILES['t5'].read()
        address = sha256(username.encode()).hexdigest()
        aes_encrypt = encrypt(myfile)
        with open("EducationApp/static/certificates/"+filename, "wb") as file:
            file.write(aes_encrypt)
        file.close()
        msg = contract.functions.createeducation(address, lms_desc, course, data_type, data_desc, str(date.today()), filename).transact({
           'from': web3.eth.defaultAccount})
        educationList.append([address, lms_desc, course, data_type, data_desc, str(date.today()), filename])
        tx_receipt = web3.eth.wait_for_transaction_receipt(msg)
        context= {'data':'Your Data Successfully Shared with Blockchain<br/>Education Data Address : '+address+'<br/>'+str(tx_receipt)}
        return render(request, 'ShareData.html', context) 

    

def ShareData(request):
    if request.method == 'GET':
       return render(request, 'ShareData.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def StudentLogin(request):
    if request.method == 'GET':
       return render(request, 'StudentLogin.html', {})

def EducationLogin(request):
    if request.method == 'GET':
       return render(request, 'EducationLogin.html', {})    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        global usersList, contract
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        utype = request.POST.get('t6', False)
        count = contract.functions.getUserCount().call()
        status = "none"
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            if username == user1:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.createUser(username, password, contact, email, address, utype).transact({
                 'from': web3.eth.defaultAccount})
            tx_receipt = web3.eth.wait_for_transaction_receipt(msg)
            usersList.append([username, password, contact, email, address, utype])
            context= {'data':'New user signup details completed<br/>'+str(tx_receipt)}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)

def StudentLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList, usertype
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = "StudentLogin.html"
        output = 'Invalid login details'
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            if user1 == username and pass1 == password and ulist[5] == 'Student':
                output = 'Welcome '+username
                status = 'StudentScreen.html'                
                break            
        context= {'data':output}
        return render(request, status, context)


def EducationLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList, usertype
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = "EducationLogin.html"
        output = 'Invalid login details'
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            if user1 == username and pass1 == password and ulist[5] == 'Education Department':
                output = 'Welcome '+username
                status = 'EducationScreen.html'                
                break            
        context= {'data':output}
        return render(request, status, context)







        



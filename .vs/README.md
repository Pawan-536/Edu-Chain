# 🏛 PublicEduChain

*A Framework for Sharing Student-Owned Educational Data on Blockchain*

PublicEduChain is a decentralized application that allows students to control and share their educational data securely through the Ethereum blockchain using smart contracts. This framework aims to overcome the limitations of centralized educational data systems, such as data tampering, single-point failures, and lack of interoperability.



## 🚀 Key Features

-  *Student-Controlled Data Access*  
  Students store and manage their own academic records via smart contracts.

-  *Tamper-Proof Blockchain Storage*  
  Education data is stored as immutable blocks on Ethereum, ensuring transparency and security.

- *Smart Contract Integration*  
  Designed using Solidity, deployed on Ethereum, and interacted with via Python (Web3).

-  *AES Encryption*  
  Certificate data is encrypted with AES for additional security and can be decrypted only by authorized educational departments.

-  *Decentralized Certificate Management*  
  Both text and image-based student certificates are stored and accessible securely.



## 🛠 Tech Stack

- *Backend:* Django 2.1.7 (Python)
- *Frontend:* Tailwind CSS, HTML
- *Blockchain:* Ethereum (Solidity smart contracts)
- *Encryption:* AES
- *Libraries:* Web3.py, pyaes, pbkdf2

---

## 🧱 Modules Overview

-  *New User Profile Generation*  
  Both students and education departments can register themselves. Their identities are stored on the blockchain.

-  *Student Login*  
  Students can log in, add educational data, upload certificates, and view their blockchain-stored information.

- *Education Department Login*  
  Authorized departments can log in and access any student's shared data via their blockchain address.





## 📦 Installation & Setup

### 🧰 Requirements

Install dependencies using the provided requirements.txt:


pip install -r requirements.txt

🧪 Run the Blockchain Server
Navigate to:

hello-eth/node-modules/bin
Double-click runBlockchain.bat to start the Ethereum test node.

In the console that opens, type: migrate


This command will deploy the smart contract and generate a contract address.
Copy the contract address from the output and paste it into the views.py file in your Django project to enable interaction with the smart contract.

▶ Run the Django Server
Double-click the runServer.bat file to launch the Django backend.

OR run it manually:

python manage.py runserver

Open your browser and go to:

http://127.0.0.1:8000/index.html  to start using the application.
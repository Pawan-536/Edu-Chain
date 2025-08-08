pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//MyEduContract solidity code
contract MyEduContract {

    uint public educationCount = 0; 
    mapping(uint => education) public educationList; 
     struct education
     {
       string LMSAddress;
       string LMSDescription;
       string course;
       string datatype;
       string datadescription;
       string data_date;      
       string certificate_filename;
     }
 
   // events 
   event educationCreated(uint indexed _fileId);

  
   //function  to save education details
   function createeducation(string memory add, string memory desc, string memory course_, string memory datatype_, string memory datadescription_, string memory data_date_, string memory certificate_filename_) public {
      educationList[educationCount] = education(add, desc, course_, datatype_, datadescription_, data_date_, certificate_filename_);
      emit educationCreated(educationCount);
      educationCount++;
    }

     //get education count
    function getEducationCount()  public view returns (uint) {
          return  educationCount;
    }

    function getLMSAddress(uint i) public view returns (string memory) {
        education memory chq = educationList[i];
	return chq.LMSAddress;
    }

    function getLMSDesc(uint i) public view returns (string memory) {
        education memory chq = educationList[i];
	return chq.LMSDescription;
    }

    function getCourse(uint i) public view returns (string memory) {
        education memory chq = educationList[i];
	return chq.course;
    }

    function getType(uint i) public view returns (string memory) {
        education memory chq = educationList[i];
	return chq.datatype;
    }

     function getDescription(uint i) public view returns (string memory) {
        education memory chq = educationList[i];
	return chq.datadescription;
    }

    function getDate(uint i) public view returns (string memory) {
        education memory chq =educationList[i];
	return chq.data_date;
    }

    function getCertificate(uint i) public view returns (string memory) {
        education memory chq = educationList[i];
	return chq.certificate_filename;
    }

         
       
    uint public userCount = 0; 
    mapping(uint => user) public usersList; 
     struct user
     {
       string username;
       string password;
       string phone;
       string email;
       string user_address;
       string usertype;
     }
 
   // events
 
   event userCreated(uint indexed _userId);
 
  function createUser(string memory _username, string memory _password, string memory _phone, string memory _email, string memory _address, string memory ut) public {
      usersList[userCount] = user(_username, _password, _phone, _email, _address, ut);
      emit userCreated(userCount);
      userCount++;
    }

    
     //get user count
    function getUserCount()  public view returns (uint) {
          return  userCount;
    }

    function getUsername(uint i) public view returns (string memory) {
        user memory usr = usersList[i];
	return usr.username;
    }

    function getPassword(uint i) public view returns (string memory) {
        user memory usr = usersList[i];
	return usr.password;
    }

    function getAddress(uint i) public view returns (string memory) {
        user memory usr = usersList[i];
	return usr.user_address;
    }

    function getEmail(uint i) public view returns (string memory) {
        user memory usr = usersList[i];
	return usr.email;
    }

    function getPhone(uint i) public view returns (string memory) {
        user memory usr = usersList[i];
	return usr.phone;
    }

    function getUserType(uint i) public view returns (string memory) {
        user memory usr = usersList[i];
	return usr.usertype;
    }
}
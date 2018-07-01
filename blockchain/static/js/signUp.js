function register() {
	if(!checkname()){
		return false;	
	}
	if (!checkpass()) {
		return false;
	} 
	if (!checkrpass()) {
		return false;
	} 
	if(!checkemail()){
		return false;
	} 
	//if(!checkbirthday()){
		//return false;
	//}
	return true;
}

function modify(){
	if(!checkname()){
			return false;	
		}
	if (!checkpass()) {
			return false;
		} 
		
	if(!checkemail()){
			return false;
		} 
		
	return true;


}


function checkname()    
{
    var name = $("#uname").val();  
    var ts = document.getElementById("nametext");
    if(name == "")    
    {   
        ts.innerHTML ="input name!";
        ts.style.color="red";
        return false;
    } 
   
    ts.innerHTML ="ok";
    ts.style.color="green";

    return true;
}

function checkpass(){
	var userPass = $("#upass").val();
	
	var pts = document.getElementById("pswtext");
	
	if(userPass == "")
	{
		pts.innerHTML ="input password!";
		pts.style.color="red";
	    return false;
	}else if(userPass.length<6)	
	{	
		pts.innerHTML ="password short!";
		pts.style.color="red";
	    return false;
	}else{
    	pts.innerHTML ="ok";
    	pts.style.color="green";
		return true;
	}
}
function checkrpass(){
	var userPass = $("#upass").val();
	var userRPass = $("#urpass").val();
	var prts =  document.getElementById("rpswtext");
	if (userPass != userRPass) {
		prts.innerHTML="different inputs!";
		prts.style.color="red";
		return false;
	}
    prts.innerHTML ="ok";
    prts.style.color="green";
	return true;
}
function checkemail(){
	var userEmail = $("#uemail").val();
	var ets = document.getElementById("emailtext");
	if(!isEmail(userEmail)){
		ets.innerHTML ="format incorrect!";
		ets.style.color="red";
		return false;
	} 
    ets.innerHTML ="ok";
    ets.style.color="green";
	return true;
}
function isEmail(str){
    var reg = /[a-z0-9-]{1,30}@[a-z0-9-]{1,65}.[a-z]{3}/;
    return reg.test(str);
}

function checkbirthday(){
	var userBirth = $("#ubirthday").val();
	var ets = document.getElementById("birthdaytext");
	if(userBirth  == "")
		return true;
	else if(!isBirthday(userBirth)){
		ets.innerHTML ="format incorrect!";
		ets.style.color="red";
		return false;
	}else{ 
    	ets.innerHTML ="ok";
    	ets.style.color="green";
		return true;
	}
}
function isBirthday(str){
    var reg = /[0-9-]{4}-[0-9-]{2}-[0-9-]{2}/;
    return reg.test(str);
}


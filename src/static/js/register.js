var check_confirm = function() {
  if (document.getElementById('password').value ==
    document.getElementById('confirm_password').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'matching';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'not matching';
  }
}

var check_password = function () {
    var str = document.getElementById('password').value;
    var re = /^[\w\~\!\@\#\$\%\^\&\*\(\)\_\+\,\.\;\']+$/;
    if(str.length <6){
        document.getElementById('message_password').innerHTML = 'Too short, current length: ' + str.length;
        document.getElementById('message_password').style.color = 'red';
    }
    else if(str.length >16){
        document.getElementById('message_password').innerHTML = 'Too long, at most 16';
        document.getElementById('message_password').style.color = 'red';
    }
    else if(!re.exec(str)){
        document.getElementById('message_password').innerHTML = 'Invalid character!';
        document.getElementById('message_password').style.color = 'red';
    }
    else{
        document.getElementById('message_password').innerHTML = '';
        document.getElementById('message_password').style.color = 'green';
    }
}

var check_username = function () {
    var str = document.getElementById('user_name').value;
    var re = /^\w+$/;
    if(!re.exec(str)){
        document.getElementById('message_username').innerHTML = 'Only characters, digits and underscore';
        document.getElementById('message_username').style.color = 'red';
    }
    else{
        document.getElementById('message_username').innerHTML = '';
    }
}
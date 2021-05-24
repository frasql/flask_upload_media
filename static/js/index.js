/* Bulma css open modals */

// modal signup
const signUpButton = document.querySelector('#register_modal');

if(signUpButton) {
    
    const modal_signup = document.querySelector('#modal_register');
    const closeSignupBtn = document.querySelector('#close_register');
      
      
    signUpButton.addEventListener('click', () => {
        modal_signup.classList.add('is-active');
    });
      
    closeSignupBtn.addEventListener('click', () => {
        modal_signup.classList.remove('is-active');
    })

}


// modal signin
const signInButton = document.querySelector('#login_modal');

if(signInButton) {
    const modal_signin = document.querySelector('#modal_login');
    const closeSigninBtn = document.querySelector('#close_login');


    signInButton.addEventListener('click', () => {
        modal_signin.classList.add('is-active');
    });


    closeSigninBtn.addEventListener('click', () => {
        modal_signin.classList.remove('is-active');
    })

}

/* Register and Login functions */

function RegisterUser() {
    const firstname = document.querySelector("#firstname");
    const lastname = document.querySelector("#lastname");
    const username = document.querySelector("#username");
    const email = document.querySelector("#email");
    const password = document.querySelector("#password");


    const data = {
        "firstname": firstname.value,
        "lastname": lastname.value,
        "username": username.value,
        "email": email.value,
        "password": password.value

    }
    
    console.log(data);
    let data_json = JSON.stringify(data);
    console.log(data_json);
    let h = new Headers();
    h.append("Content-Type", "application/json");
    h.append("Accept", "application/json");

    let options = {
        method: 'POST',
        mode: 'no-cors',
        header: h,
        body: JSON.stringify(data)        
    }
    
    const url = 'http://localhost:5000/register/';
    
    const req = new Request(url, options);
    
    fetch(req)
    .then((response) => {
        if(response.ok) {
            return response.json();
        } else {
            throw new Error(response.statusText);
        }
    })
    .then((data) => {
        console.log(data);
    })
    .catch((err) => {
        console.log("Error:", err);
    })
}


function CleanForm() {
    document.querySelector("#firstname").value = "";
    document.querySelector("#lastname").value = "";
    document.querySelector("#username").value = "";
    document.querySelector("#password").value = "";

    return false

}

// set cookies
function createCookie(cookieName,cookieValue)
{
  // var date = new Date();
  //date.setTime(date.getTime()+(daysToExpire*24*60*60*1000));
  document.cookie = cookieName + "=" + cookieValue; // + "; expires=" + date.toGMTString()
}

// read cookies
function accessCookie(cookieName)
{
  var name = cookieName + "=";
  var allCookieArray = document.cookie.split(';');
  for(var i=0; i<allCookieArray.length; i++)
  {
    var temp = allCookieArray[i].trim();
    if (temp.indexOf(name)==0)
    return temp.substring(name.length,temp.length);
     }
    return "";
}
// log a user
function LoginUser() {
    const login_username = document.querySelector("#login_username");
    const login_password = document.querySelector("#login_password");

    let data = {
        "username": login_username.value,
        "password": login_password.value
    }
    
    let h = new Headers();
    h.append("Content-Type", "application/json");
    h.append("Accept", "application/json");    
    let options = {
        method: 'POST',
        mode: 'no-cors',
        header: h,
        body: JSON.stringify(data)
            
    }
    
    const url = 'http://localhost:5000/login/';
    
    let req = new Request(url, options);
    
    fetch(req)
    .then((response) => {
        if(response.ok) {
            return response.json();
        } else {
            throw new Error(response.statusText);
        }
    })
    .then((data) => {
        //let data_json = JSON.parse(data);
        // get access and refresh token for login endpoint
        const access_token = data['access_token'];
        const refresh_token = data['refresh_token'];
        // set access and refresh token in session storage 
        createCookie("access_token", access_token);
    })
    .catch((err) => {
        console.log("Error:", err);
    })
}


function GetUserProfile() {
    let access_token = accessCookie("access_token");
    
    let options = {
        method: 'GET',
        credentials: "include",
        mode: 'cors',
        headers: {
            "Content-Type": "aplication/json",
            "Authorization": "Bearer "+ access_token
        }
    }
    
    let url = 'http://localhost:5000/profile/';
    
    let req = new Request(url, options);
    console.log(req);
    
    fetch(req)
    .then((response) => {
        if(response.ok) {
            return response;
        } else {
            throw new Error(response.statusText);
        }
    })
    .then((data) => {
        console.log(data);
    })
    .catch((err) => {
        console.log("Error:", err);
    })
}



/* Main Program */

// execute login_user

const btn_login_user = document.querySelector("#login_user");
if(btn_login_user) {
    btn_login_user.addEventListener('click', LoginUser);
}


// execute register_user
const btn_register_user = document.querySelector("#register_user");
if(btn_register_user) {
    btn_register_user.addEventListener('click', RegisterUser);
}

// execute register_user
const btn_profile_user = document.querySelector("#profile");
if(btn_profile_user) {
    console.log(btn_profile_user);
    btn_profile_user.addEventListener('click', GetUserProfile);
}



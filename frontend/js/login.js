window.onload = function(){
    localStorage.removeItem('token');
    //localStorage.removeItem('username');
    localStorage.removeItem('id');
}
function login_user(){
    //document.getElementById("mensaje").innerHTML="";
    const username = document.getElementById('in-username').value;
    const password = document.getElementById('in-password').value;
    const requestOptions={
        method:'POST',
        headers:{
            'Content-Type' : 'application/json',
            'authorization' : 'Basic ' + btoa(username + ':' + password)
        }
    }
    fetch('http://127.0.0.1:5000/login', requestOptions)
    .then(
        res=>{return res.json()}
        )
    .then(
        resp=>{
            console.log(resp)
            if (resp.token){
                localStorage.setItem('token', resp.token);
                localStorage.setItem('username', resp.nombre_completo);
                localStorage.setItem('id', resp.id);
                //document.getElementById("mensaje").innerHTML = 'Bienvenido ' + resp.nombre_completo;
                window.location.href = "./dashboard.html";
            }
            else{
                document.getElementById("mensaje").innerHTML= resp.message;
            }
        
        }
        )
}
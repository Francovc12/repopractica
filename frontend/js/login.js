window.onload = function(){
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('id');
}

function login_usuario(){
    const nombre_usuario = document.getElementById('in-nombre_usuario').value;
    const contraseña = document.getElementById('in-contraseña').value;

    if (nombre_usuario == "" || contraseña == "")
    {
        Swal.fire({
            title: 'Error!',
            text: 'Ingrese el usuario y la contraseña',
            icon: 'error',
            confirmButtonText: 'Cool'
        })
    }
    else {
        const requestOptions={
            method:'POST',
            headers:{
                'Content-Type' : 'application/json',
                'authorization' : 'Basic ' + btoa(nombre_usuario + ':' + contraseña)
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
                    window.location.href = "./dashboard.html";
                }
                else{
                    document.getElementById("mensaje").innerHTML= resp.message;
                }
            
            }
        )
    }

}

function registrar_usuario(){
}
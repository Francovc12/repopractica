const iduser = localStorage.getItem('id')
const token = localStorage.getItem("token")
const name = localStorage.getItem('username')
window.onload = function(){
    document.getElementById("bienvenida").innerHTML = 'Bienvenido ' + name;
}
function clientes(){
    document.getElementById("recurso").innerHTML="<h2>hola mundo</h2>";
    const requestOptions={
        method:'GET',
        headers:{
            'token-acceso' : token,
            'id-usuario' : iduser
        }
    }
    fetch(`http://127.0.0.1:5000/usuarios/${iduser}/clientes`, requestOptions)
    .then(
        res =>{return res.json()}
    )
    .then(
        resp=>{
            console.log(resp)
            console.log("hola mundo")
            document.getElementById("recurso").innerHTML = "<table id=tablacliente> </table>"
            var clientes = "<tr><th>ID</th><th>Nombre</th><th>Apellido</th><th>Dni</th><th>Email</th></tr>"
            for(let i = 0; i < resp.length; i++){
                let id = resp[i].id_cliente
                let name = resp[i].nombre
                let surname = resp[i].apellido
                let dni = resp[i].dni
                let email = resp[i].email
                //console.log(email)
                let cliente=`<tr><td>${id}</td><td>${name}</td><td>${surname}</td><td>${dni}</td><td>${email}</td></tr>`
                clientes = clientes.concat(cliente)
            }
            document.getElementById("tablacliente").innerHTML=clientes
        }
    )
    .catch(error => console.error(error));
    
}
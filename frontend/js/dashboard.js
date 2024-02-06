const iduser = localStorage.getItem('id')
const token = localStorage.getItem("token")
const name = localStorage.getItem('username')
window.onload = function(){
    document.getElementById("bienvenida").innerHTML = 'Bienvenido ' + name;
}
function clientes(){

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
            //console.log(resp)
            //console.log("hola mundo")
            document.getElementById('botonesrec').innerHTML='<button onclick="agregarcliente()">Agregar cliente</button>'
            document.getElementById("recurso").innerHTML = "<table id=tablacliente> </table>"
            var clientes = "<thead><tr><th>ID</th><th>Nombre</th><th>Apellido</th><th>Dni</th><th>Email</th><th>accion</th></tr></thead>"
            if (resp.length == 0){
                clientes = clientes.concat('<tr><td>No posee registros de clientes</td></tr>')
            }

            for(let i = 0; i < resp.length; i++){
                let id = resp[i].id_cliente
                let name = resp[i].nombre
                let surname = resp[i].apellido
                let dni = resp[i].dni
                let email = resp[i].email
                //console.log(email)
                let cliente=`<tr><td>${id}</td><td>${name}</td><td>${surname}</td><td>${dni}</td><td>${email}</td><td><button>Eliminar</button><button>Modificar</button></td></tr>`


                clientes = clientes.concat(cliente)
            }
            document.getElementById("tablacliente").innerHTML=clientes
        }
    )
    .catch(error => console.error(error));
}
function agregarcliente(){
    document.getElementById("form").innerHTML='<form><input type="text" placeholder="Ingrese nombre"></input><button type="submit">Enviar</button></form><button id="cerrarModal">Cerrar</button>'
    document.getElementById('form').showModal()
    /*const requestOptions={
        method:'POST',
        headers:{
            'token-acceso' : token,
            'id-usuario' : iduser
        }
    }
    fetch(`http://127.0.0.1:5000/usuarios/${iduser}/clientes`, requestOptions)*/
}
document.addEventListener("DOMContentLoaded", search);
const URL_API = "http://localhost:3000/api/";
var customers = []

function openForm() {
  var modalElement = document.getElementById("modal");
  modalElement.classList.add("opened");
}

function closeModale() {
  var modalElement = document.getElementById("modal");
  modalElement.classList.remove("opened");
}

function add() {
  clean()
  openForm()
}

function clean() {
  document.getElementById('txtID').value = ''
  document.getElementById('txtFirstName').value = ''
  document.getElementById('txtSurName').value = ''
  document.getElementById('txtPhone').value = ''
  document.getElementById('txtAdress').value = ''
  document.getElementById('txtEmail').value = ''
}
function init() {
  search();
}

async function search() {
  var url = URL_API + 'customers';
  var response = await fetch(url, {
    "method": 'GET',  
    "headers": {
      "ContentType": 'application/json',
    },
  })
  customers = await response.json();

  var html = ''
  for(n of customers){
    var row = `      
    <tr>
      <td>${n.firstname}</td>
      <td>${n.surname}</td>
      <td>${n.email}</td>
      <td>${n.phone}</td>
      <td>
        <a href="#" onclick="edit(${n.id})" class="myButton edBtn">Edit</a>
        <a href="#" onclick="remove(${n.id})" class="myButton delBtn">Delete</a>
      </td>
    </tr>`
    html = html + row
  };
  
  document.querySelector("#customers > tbody").outerHTML = html;
}

async function remove(id){
  respuesta = confirm('Are you sure you want to delete this client?')
  if(respuesta){
    var url = URL_API + 'customers/' + id;
    await fetch(url, {
      "method": 'DELETE',
      "headers": {
      "ContentType": 'application/json',
    },
  })
    window.location.reload();
  }
}


async function save(){
  var data = {
    "adress": document.getElementById('txtAdress').value,
    "email": document.getElementById('txtEmail').value,
    "firstname": document.getElementById('txtFirstName').value,
    "phone": document.getElementById('txtPhone').value,
    "surname": document.getElementById('txtSurName').value
  }
  var id = document.getElementById('txtID').value
  if(id != ''){
    console.log("ID VALUE adentro del if:"+id)
    data.id = id
  }

  var url = URL_API + 'customers'
  await fetch(url, {
    'method': 'PUT',
    'body': JSON.stringify(data),
    'headers': {
      'Content-Type': 'application/json',
      },
  })
    window.location.reload();
  }

  function edit(id){
    openForm()
    var customer = customers.find(x => x.id == id)
    document.getElementById('txtID').value = customer.id
    document.getElementById('txtAdress').value = customer.adress
    document.getElementById('txtEmail').value = customer.email
    document.getElementById('txtFirstName').value = customer.firstname
    document.getElementById('txtPhone').value = customer.phone
    document.getElementById('txtSurName').value = customer.surname
    }

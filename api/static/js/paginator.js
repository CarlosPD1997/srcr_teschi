// pagination.js

document.addEventListener('DOMContentLoaded', function() {
  var utensiliosList = document.getElementById('utensilios-list');
  var pagination = document.getElementById('pagination');
  var itemsPerPage = 5;
  var currentPage = 1;

  // Función para mostrar los utensilios en la tabla según la página actual
  function displayUtensilios(items, page) {
    var start = (page - 1) * itemsPerPage;
    var end = start + itemsPerPage;
    var paginatedItems = items.slice(start, end);

    utensiliosList.innerHTML = '';

    paginatedItems.forEach(function(utensilio) {
      var tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${utensilio.id}</td>
        <td>${utensilio.nombre}</td>
        <td>${utensilio.cantidad}</td>
        <td>${utensilio.descripcion}</td>
        <td>${utensilio.tamaño}</td>
        <td><button type="button" class="btn btn-success mb-3 add-item">Agregar</button></td>
      `;
      utensiliosList.appendChild(tr);
    });
  }

  // Mostrar los utensilios en la página inicial
  displayUtensilios(utensilios, currentPage);

  // Función para generar los ítems de la paginación
  function setupPagination(items, wrapper, rows_per_page) {
    wrapper.innerHTML = '';

    var page_count = Math.ceil(items.length / rows_per_page);
    for (var i = 1; i <= page_count; i++) {
      var btn = document.createElement('button');
      btn.classList.add('btn', 'btn-sm', 'btn-outline-secondary');
      btn.innerText = i;

      btn.addEventListener('click', function() {
        currentPage = parseInt(this.innerText);
        displayUtensilios(items, currentPage);
      });

      wrapper.appendChild(btn);
    }
  }

  // Configurar la paginación
  setupPagination(utensilios, pagination, itemsPerPage);
});

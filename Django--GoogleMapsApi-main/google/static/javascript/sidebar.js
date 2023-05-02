function openSidebar(nombre) {
  var sidebar = document.getElementById("nuevo-sidebar");
  var sidebarContent = document.getElementById("sidebar-content");
  var personal = "Personal";

  fetch(nombre)
    .then((response) => response.text())
    .then((html) => {
      sidebarContent.innerHTML = "<h3>" + personal + "</h3>";
      sidebarContent.innerHTML = html;
    });

  sidebar.style.width = "460px";
  sidebar.style.height = "70%";
  sidebar.style.position = "fixed";
  sidebar.style.top = "15%";
  sidebar.style.right = "20%";
  sidebar.style.backgroundColor = "#f1f1f1";
  sidebar.style.padding = "20px";
  sidebar.style.display = "block";
  sidebar.style.zIndex = "9999";
  sidebar.style.overflowY = "scroll";

  // Verificar el ancho de la ventana y modificar los estilos del sidebar en consecuencia
  if (window.innerWidth <= 600) {
    sidebar.style.width = "100%";
    sidebar.style.height = "100%";
    sidebar.style.top = "0";
    sidebar.style.right = "0";
  }
}

function openSidebarCrearEmp(nombre) {
  var sidebar = document.getElementById("nuevo-sidebar");
  var sidebarContent = document.getElementById("sidebar-content");

  fetch(nombre)
    .then((response) => response.text())
    .then((html) => {
      // agregar el contenido al sidebar
      sidebarContent.innerHTML = html;
    });

  // configurar estilos para el sidebar
  sidebar.style.width = "250px";
  sidebar.style.position = "fixed";
  sidebar.style.top = "0";
  sidebar.style.right = "0";
  sidebar.style.width = "100%";
  sidebar.style.height = "100%";
  sidebar.style.backgroundColor = "#f1f1f1";
  sidebar.style.padding = "20px";
  sidebar.style.display = "block";
  sidebar.style.zIndex = "9999";
  sidebar.style.overflowY = "scroll";
}
function closeSidebar() {
  var sidebar = document.getElementById("nuevo-sidebar");
  sidebar.style.display = "none";
}
var closeButton = document.getElementById("sidebar-close");
if (closeButton) {
  closeButton.addEventListener("click", closeSidebar);
}

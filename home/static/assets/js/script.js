let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e) => {
    let arrowParent = e.target.parentElement.parentElement;//selecting main parent of arrow
    arrowParent.classList.toggle("showMenu");
  });
}
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");
console.log(sidebarBtn);
sidebarBtn.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});




var addRow = document.getElementById("addRow");
addRow.addEventListener("click", handle_addRow)

function handle_addRow() {
  var myTable = document.getElementById("myTable");
  var row = myTable.insertRow();
  var rowCell = row.insertCell(0)
  rowCell.innerHTML = "Hello";
  row.inertCell(-1).innerHTML = "<i class='bx bx-trash'></i>"
  // row.inertCell(-1).innerHTML = "<i class='bx bx-trash'></i>"
}




// ------------ Date Range Selection 
$(function() {
        
  $('input[name="datefilter"]').daterangepicker({
      autoUpdateInput: false,
      locale: {
          cancelLabel: 'Clear'
      }
  });
  
  $('input[name="datefilter"]').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
  });
  
  $('input[name="datefilter"]').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
  
  });

// -- J Querry  For search Dropdown
$(document).ready(function() {
  $('.js-example-basic-single').select2();
});





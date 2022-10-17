
function deleteNote(id, url, url_redirect) {
  var action = confirm("Вы уверены, что хотите удалить заметку?");
  if (action !== false) {
    $.ajax({
        url: url,
        data: {
            'id': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data.deleted) {
              $("#table_id #note_" + id).remove();
            }
            if (url_redirect) {
                window.location.href = url_redirect
            }
        }
    });
   }}


function chosenOneNote(id, url) {
    $.ajax({
        url: url,
        data: {
            'id': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data.is_chosen_one) {
                document.getElementById("i_id_" + id).className = 'btn btn-warning';
                document.getElementById("i_id_" + id).textContent = 'Убрать '
            } else {
                document.getElementById("i_id_" + id).className = 'btn btn-outline-dark';
                document.getElementById("i_id_" + id).textContent = 'Поставить'
            }
         }
    });
   }

   function sortedResults(sorted_item, url) {
      $.ajax({
        url: url,
        data: {
            'sorted_item': sorted_item,
        },
        dataType: 'json',
        success: function (data) {

            $('#result_list').html(data.html);
         }
    });
   }

   function applyFilters(url) {
       const formData = new FormData(document.getElementById("filters-form"));
       var title = formData.get('title');
       var category = formData.get('category');
       var date_from = formData.get('date_from');
       var date_by = formData.get('date_by');
       var is_chosen_one = formData.get('is_chosen_one');
      $.ajax({
        url: url,
        data: {
            'title': title,
            'category': category,
            'date_from': date_from,
            'date_by': date_by,
            'is_chosen_one': is_chosen_one,
            'use_filter': true,
        },
        dataType: 'json',
        success: function (data) {

            $('#result_list').html(data.html);
         }
    });
   }

    function showFilters() {
        var filters_form_hidden = document.getElementById('filters-form').hidden;
        if (filters_form_hidden === false) {
            document.getElementById('filters-form').hidden = true;
            document.getElementById('filters').textContent = 'Показать фильтры'
        } else {
            document.getElementById('filters-form').hidden = false;
            document.getElementById('filters').textContent = 'Скрыть фильтры'
                }
            }

    function setColor(thisObj, color)
 {
    thisObj.style.backgroundColor = color;
 }


 function showNote(id, url) {
  $.ajax({
        url: url,
        data: {
            'id': id,
        },
        dataType: 'json',
        success: function (data) {

            $('#my_result').html(data.html);
         }
    });
}
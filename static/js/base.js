function deleteNote(id, url, from_detail_page_flag, from_link_flag, url_redirect) {
  var action = confirm("Вы уверены, что хотите удалить заметку?");
  if (action !== false) {
    $.ajax({
        url: url,
        data: {
            'id': id,
            'from_detail_page_flag': from_detail_page_flag,
            'from_link_flag': from_link_flag
        },
        dataType: 'json',
        success: function (data) {
            if (data.deleted) {
              $("#table_id #note_" + id).remove();
              if (data.table_remote) {
                  document.getElementById("filters").hidden = true
                  document.getElementById("table_id").hidden = true
                  document.getElementById("message-no-notes").hidden = false
              }
            } else {
                if (data.from_link_flag) {
                    window.location.href = url_redirect
                } else {
                    $('#my_result').html(data.html);
                }
            }
        }
    });
  }
}

function showFormCreateNote(url) {
  $.ajax({
      url: url,
      dataType: 'json',
      success: function (data) {
          $('#my_result').html(data.html);
        }
    });
  }

function createNote(url) {
    const formData = new FormData(document.getElementById("create-form"));
    var title = formData.get('title');
    var category = formData.get('category');
    var text = CKEDITOR.instances.editor.getData();
  $.ajax({
      url: url,
      data: {
            'title': title,
            'category': category,
            'text': text,
            'time_create': true,
        },
      dataType: 'json',
      success: function (data) {
          $('#my_result').html(data.html);
        }
    });
   }

function updateNote(id, url, save_flag, from_link_flag, url_redirect) {
    if (save_flag) {
        var title = document.getElementById("title-update").value
        var category = document.getElementById("category-update").value
        var text = CKEDITOR.instances.editor.getData();
        var i_data = {'id': id, 'save_flag': save_flag, 'title': title,
            'category': category, 'text': text, 'from_link_flag': from_link_flag}
    } else {
        var i_data = {'id': id, 'from_link_flag': from_link_flag}
    }
    $.ajax({
      url: url,
      data: i_data,
      dataType: 'json',
      success: function (data) {
          if (data.from_link_flag) {
              window.location.href = url_redirect
          } else {
              $('#note-detail').html(data.html);
          }
        }
    });
    }

function publishNote(id, url) {
    $.ajax({
      url: url,
      data: {
          'id': id
      },
      dataType: 'json',
      success: function (data) {
          document.getElementById('link-place').hidden = false;
          document.getElementById('link-place').value = data.note_link
        }
    });
   }


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

function setColor(thisObj, color) {
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
}
);}
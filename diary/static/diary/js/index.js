// Collecting form inputs
function collectInputs() {
    let map = {}
    $(".modal-body > .form-control > input").each(function() {
        map[$(this).attr("id")] = $(this).val();
    })
    return map
}

// if view return if_valid = True
function appendToHtml(data) {
    $('.modal-backdrop').remove()
    $("body").html(data.html)
    $('.dropdown-toggle').dropdown()
    $('body').removeClass('modal-open')
}

function appendToBtnGroup(item) {
    $('.buttons').append(item)
    $('form#create-form').trigger('reset')
    $('#create').modal('hide')
//    if ($("#exist-check")) {
//        alert('exist-check')
//    }

}

function deleteItem(slug) {
    $('#delete-form').submit(function (e) {
        e.preventDefault()
        // Pass view url through item attribute "data-url"
        let url = $('#delete-dropdown' + slug).attr('data-url')
        console.log(url)
        let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
        if (slug) {
            $.ajax({
                url: url,
                data: {'slug': slug, csrfmiddlewaretoken: csrf_token},
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.deleted) {
                        $('#item-' + slug).remove()
                        $('#delete').modal('hide')
                    }
                }
            })
        }
    })

}

// Create Django Ajax Call
$("#create-form").on('submit', function(e) {
    e.preventDefault()
    let inputTitle = $('input#input-title').val()
    let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
    url = $('#add').attr('data-url')
    $.ajax({
        url: url,
        // data: form.serialize(),
        data: {title: inputTitle, csrfmiddlewaretoken: csrf_token},
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                appendToBtnGroup(data.html)
            }
            else {
                alert("All fields must have a valid value.")
            }
        }
    })
})

// Set create Django Ajax Call
$("form#set-create-form").on('submit', function(e) {
    e.preventDefault()
    let inputWeight = $('input#input-weight').val()
    let inputReps = $('input#input-reps').val()
    let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
    url = $('#add').attr('data-url')
    alert( inputWeight + ' x ' + inputReps)
    $.ajax({
        url: url,
        // data: form.serialize(),
        data: {
            weight: inputWeight,
            reps: inputReps,
            csrfmiddlewaretoken: csrf_token
            },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                appendToHtml(data)
            }
            else {
                alert("All fields must have a valid value.")
            }
        }
    })
    // $("#workout-create-form").trigger("reset")
})

// Update Django Ajax Call
function updateItem(slug) {
    if (slug) {
        // Passing initial form fields data
        let itemId = '#title' + slug
        let title = $(itemId).text()
        $('input#update-title').val(title)
        $('#slug').val(slug)

        // forming ajax request
        $("form#update-form").submit(function(s) {
            s.preventDefault()
            let itemTitle = $('#update-title').val()
            let url = $('#edit-dropdown' + slug).attr('data-url')
            console.log('url:', url)
            let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
            $.ajax({
                url: url,
                data: {
                    slug: slug,
                    title: itemTitle,
                    csrfmiddlewaretoken: csrf_token
                },
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        $('#item-' + slug).replaceWith(data.html)
                        $('form#update-form').trigger('reset')
                        $('#edit').modal('hide')

                    }
                    else {
                        alert("All fields must have a valid value.")

                    }
                }
            });
        })
    }
}

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
//    $('.dropdown-toggle').dropdown()
    $('body').removeClass('modal-open')
}

function appendToBtnGroup(item) {
    $('.buttons').append(item)
    $('div#exist-check').remove()
    $('form#create-form').trigger('reset')
    $('#create').modal('hide')
}

function setAppendToBtnGroup(item) {
    $('.set-box').append(item)
    $('form#set-create-form').trigger('reset')
    $('#create').modal('hide')
}

function deleteItem(slug) {
    $('#delete-form').submit(function (e) {
        e.preventDefault()
        // Pass view url through item attribute "data-url"
        let url = $('#delete-dropdown' + slug).attr('data-url')
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

// Workout & exercise create Django Ajax Call
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

// Workout & exercise update Django Ajax Call
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

// Set create Django Ajax Call
$("form#set-create-form").on('submit', function(e) {
    e.preventDefault()
    let inputWeight = $('input#input-weight').val()
    let inputReps = $('input#input-reps').val()
    let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
    url = $('#add').attr('data-url')
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


// Set update Django Ajax Call
function updateSet(pk) {
    if (pk) {
        // Passing initial form fields data
        let setWeightId = '#set-weight' + pk
        let setRepsId = '#set-reps' + pk
        let setRestId = '#set-rest-time' + pk
        // Current fields values
        let weight = $(setWeightId).text().trim()
        let reps = $(setRepsId).text().trim()
        let rest = $(setRestId).text().trim()
        $('input#update-weight').val(weight)
        $('input#update-reps').val(reps)
        $('input#update-rest-time').val(rest)
        $('#pk').val(pk)

        // forming ajax request
        $("form#update-form").submit(function(s) {
            s.preventDefault()
            let itemWeight = $('#update-weight').val()
            let itemReps = $('#update-reps').val()
            let itemRestTime = $('#update-rest-time').val()
            let url = $('#edit' + pk).attr('data-url')
            let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
            $.ajax({
                url: url,
                data: {
                    pk: pk,
                    weight: itemWeight,
                    reps: itemReps,
                    rest_time: itemRestTime,
                    csrfmiddlewaretoken: csrf_token
                },
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        appendToHtml(data)

                    }
                    else {
                        alert("All fields must have a valid value.")

                    }
                }
            });
        })
    }
}


function restTime(pk) {
    if (pk) {
        // Passing initial form fields data
        let setWeightId = '#set-weight' + pk
        let setRepsId = '#set-reps' + pk
        // Current fields values
        let weight = $(setWeightId).text().trim()
        let reps = $(setRepsId).text().trim()
        $('input#update-weight').val(weight)
        $('input#update-reps').val(reps)
        $('#pk').val(pk)
        // forming ajax request
        $("form#update-form").submit(function(s) {
            s.preventDefault()
            let itemWeight = $('#update-weight').val()
            let itemReps = $('#update-reps').val()
            let itemRestTime
            stop()
            if (result === '00:00:00') {
                itemRestTime = $('.stopwatch').text().trim().slice(0, 5)
            } else {
                itemRestTime = result.slice(0, 5)
            }
            let url = $('#edit' + pk).attr('data-url')
            let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
            $.ajax({
                url: url,
                data: {
                    pk: pk,
                    weight: itemWeight,
                    reps: itemReps,
                    rest_time: itemRestTime,
                    csrfmiddlewaretoken: csrf_token
                },
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        appendToHtml(data)

                    }
                    else {
                        alert("All fields must have a valid value.")

                    }
                }
            });
        })
    }
}



// Set delete Django Ajax Call
function setDelete(pk) {
    $('#delete-form').submit(function (e) {
        e.preventDefault()
        // Pass view url through item attribute "data-url"
        let url = $('#delete-dropdown' + pk).attr('data-url')
        let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
        if (pk) {
            $.ajax({
                url: url,
                data: {'pk': pk, csrfmiddlewaretoken: csrf_token},
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.deleted) {
                        appendToHtml(data)
                    }
                }
            })
        }
    })

}

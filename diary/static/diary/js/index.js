// if view return if_valid = True
function appendToHtml(data) {
    $('.modal-backdrop').remove();
    let html2 = document.querySelector('html')
    $("body").html(data.html);
    $('.dropdown-toggle').dropdown();
    $('body').removeClass('modal-open');
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
                        $("body").html(data.html)
                        // $('#title' + slug).parent().remove()
                        $('.dropdown-toggle').dropdown()
                        $('body').removeClass('modal-open')
                    }
                }
            })
        }
    })

}

// Create Django Ajax Call
$("#create-form").on('submit', function(e) {
    e.preventDefault();
    let inputTitle = $('input#input-title').val()
    let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
    $.ajax({
        url: '/',
        // data: form.serialize(),
        data: {title: inputTitle, csrfmiddlewaretoken: csrf_token},
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
        let workoutId = '#title' + slug
        let title = $(workoutId).text()
        $('#update-title').val(title)
        $('#slug').val(slug)

        // forming ajax request
        $("form#update-form").submit(function(s) {
            s.preventDefault()
            let workoutTitle = $('#update-title').val()
            let type = $(this).attr('type')
            let url = $('#edit-dropdown' + slug).attr('data-url')
            let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()

            $.ajax({
                url: url,
                data: {
                    slug: slug,
                    title: workoutTitle,
                    csrfmiddlewaretoken: csrf_token
                },
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        $('.modal-backdrop').remove()
                        let html2 = document.querySelector('html')
                        $("body").html(data.html)
                        $('.dropdown-toggle').dropdown()
                        $('body').removeClass('modal-open')

                    }
                    else {
                        alert("All fields must have a valid value.")

                    }
                }
            });
        })
    }
}
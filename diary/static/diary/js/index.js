// if view return if_valid = True
function appendToHtml(data) {
    $('.modal-backdrop').remove();
    let html2 = document.querySelector('html')
    $("body").html(data.html);
    $('.dropdown-toggle').dropdown();
    $('body').removeClass('modal-open');
}

function updateWorkout(slug) {
    if (slug) {
        let workoutId = '#title' + slug
        let title = $(workoutId).text()
        $('#workout-update-title').val(title)
        $('#workout-slug').val(slug)
    }
}

function deleteWorkout(slug) {
    $('#delete-workout').submit(function (e) {
        e.preventDefault()
        let url = 'workout/' + slug + '/workout_delete'
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

// Update Django Ajax Call
$("form#workout-update-form").submit(function(s) {
    s.preventDefault()
    let url = $(this).attr('action')
    let workoutTitle = $('#workout-update-title').val()
    let workoutSlug = $('#workout-slug').val()
    let type = $(this).attr('type')
    let url2 = 'workout/' + workoutSlug + '/update/'
    let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()

    console.log('after:', workoutTitle)
    console.log('url:', url2)
    console.log('this:', this)
    console.log('slug:', workoutSlug)
    $.ajax({
        url: url2,
        data: {
            slug: workoutSlug,
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
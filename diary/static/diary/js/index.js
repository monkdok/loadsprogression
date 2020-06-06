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
    }
}

// Update Django Ajax Call
$("form#workout-update-form").submit(function(s) {
    s.preventDefault()
    let url = $(this).attr('action')
    let workoutTitle = $('#workout-update-title').val()
    let type = $(this).attr('type')

    console.log('after:', workoutTitle)
    console.log('url:', url)
    console.log('this:', this)
    // $.ajax({
    //     url: url,
    //     data: {title: workoutTitle, csrfmiddlewaretoken: '{{ csrf_token }}'},
    //     type: type,
    //     dataType: 'json',
    //     success: function (data) {
    //         alert('Success')
    //         if (data.form_is_valid) {
    //             // $('.modal-backdrop').hide();
    //             // $(document.body).removeClass("modal-open");
    //             // $('#workout_create').modal('hide')
    //             // $('.modal').remove();
    //             $('.modal-backdrop').remove();
    //             // $('#workout_create').modal('handleUpdate')
    //             // $('body').removeClass('modal-open');
    //             // document.documentElement.innerHTML = data.html; // 3 dots don't load
    //             let html2 = document.querySelector('html')
    //             // html2.innerHTML = data.html
    //             $("body").html(data.html);
    //             $('.dropdown-toggle').dropdown();
    //             $('body').removeClass('modal-open');
    //
    //         }
    //         else {
    //             // $("#workout_create .modal-body").html(data.workouts_create_form);
    //             console.log('Nope')
    //
    //         }
    //     }
    // });
})
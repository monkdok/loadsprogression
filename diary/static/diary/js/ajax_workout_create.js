$(document).ready(function(){
    $("#form").on('submit', function(e) {
        e.preventDefault();
        let workoutTitle = $('#workout-title').val();
        $.ajax({
            url: "{% url 'workout_list_url' %}",
            // data: form.serialize(),
            data: {title: workoutTitle, csrfmiddlewaretoken: '{{ csrf_token }}'},
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    // $('.modal-backdrop').hide();
                    // $(document.body).removeClass("modal-open");
                    // $('#workout_create').modal('hide')
                    // $('.modal').remove();
                    // $('body').removeClass('modal-open');
                    // $('.modal').remove();
                    // $(document.body).removeClass("modal-open");
                    // $('#workout_create').modal('handleUpdate')
                    // $('body').removeClass('modal-open');
                    // document.documentElement.innerHTML = data.html; // 3 dots don't load
                    $("#ajax-response-here").html(data.html);
                    $('.modal-backdrop').remove();
                    $('.dropdown-toggle').dropdown();

                }
                else {
                    // $("#workout_create .modal-body").html(data.workouts_create_form);
                    console.log('Nope')

                }
            }
        });
    });
});
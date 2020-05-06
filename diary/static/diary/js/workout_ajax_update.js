$document.ready(function() {
  $("#workout_edit").on('click', modal)
  function modal() {
    var title = $("#workout_title").val();
    $.ajax({
      url: "{ url 'workout_update_view' }",
      data: {
      'title': title
      },
      dataType: "json",
      success: function( data ) {
      console.log(data);
      }
    })
  }
});

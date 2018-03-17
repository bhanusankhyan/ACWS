

$(function(){
  $('a#process_input').bind('click', function(){
  $.getJSON('/background_process', {
    model: $('input[name="carModels"]').val(),
  }, function(data) {
    $("#result").text(data.result);
  });
  return false;
  });

});

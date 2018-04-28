$('document').ready(function() {

  //$('#img').addEventListener('click',function(){
    //var img = $('#img').val()
    //$.ajax({
      //data : JSON.stringify({"name" : img}),
      //dataType : 'json',
      //type : 'POST',
      //url : '/_modal_processing'
    //}).done(function(data){

    //})
  //});
  $('#process_input').on('click',function(event){
    var model = $('#carModels').val();
    //var workshop = $('#workshop').val();
  ///  var automodel1 = [Alto 800:"Alto 800",
    //Alto K10:"Alto K10",
  //  Omni:"Omni",
  //  Gypsy:"Gypsy",
  //  WagonR:"WagonR",
  //  Eeco : "Eeco",
  ///  Celerio:"Celerio",
  //  Ritz:"Ritz",
  //  Swift:"Swift",
  //  Swift Dzire:"Swift Dzire",
//    Ertiga:"Ertiga",
  //  SX4 :"SX4",
  //  Ciaz:"Ciaz"
//  ];

   //$('#img').on('click',function(){
    ///var company = $('#img').alt;
    // if (company == "Maruti Suzuki"){
      // alert("YES");

     //}

   //});
  // $( "#carModels").autocomplete({ source: automodel1 });
   //$('#myModal').modal('show');
   //$('#carModels').autocomplete("option","appendto", "#modform");
   //$.ajax({
    //   data : JSON.stringify({"workshop" :workshop}),
    //   dataType : 'json',
    //   type: 'POST',
    //   url : '/select_workshop'
   //}).done(function(data){
    // $('#result1').text("Booking Done!")

   //});


    $.ajax({
      data :JSON.stringify({"model" : model}),
      dataType : 'json',
      type : 'POST',
      url: '/background_process'
  }).done(function(data) {
    $('#result').text(data.model);
    $('#basic').text("Rs."+data.basic);
    $('#standard').text("Rs."+data.standard);
    $('#comprehensive').text("Rs."+data.comprehensive);
  });
  event.preventDefault();
  });



  // for every slide in carousel, copy the next slide's item in the slide.
  // Do the same for the next, next item.
  var carousel = $("#carousel").waterwheelCarousel({
      flankingItems: 3,
      movingToCenter: function ($item) {
        $('#callback-output').prepend('movingToCenter: ' + $item.attr('id') + '<br/>');
      },
      movedToCenter: function ($item) {
        $('#callback-output').prepend('movedToCenter: ' + $item.attr('id') + '<br/>');
      },
      movingFromCenter: function ($item) {
        $('#callback-output').prepend('movingFromCenter: ' + $item.attr('id') + '<br/>');
      },
      movedFromCenter: function ($item) {
        $('#callback-output').prepend('movedFromCenter: ' + $item.attr('id') + '<br/>');
      },
      clickedCenter: function ($item) {
        $('#callback-output').prepend('clickedCenter: ' + $item.attr('id') + '<br/>');
      }
    });
    //var currentImg = $('.active');
    //var nextImg = currentImg.next();
    $('#prev').bind('click', function () {
      carousel.prev();
      return false
    });
    $('#next').bind('click', function () {
      carousel.next();
      return false;
    });



  });

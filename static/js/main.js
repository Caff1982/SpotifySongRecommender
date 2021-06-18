
$(document).ready(function(){
	// Open modal popup
    $(".modal-button").click(function(){
	  	let modal_id = $(this).attr('id');
	  	$('#modal-popup' + modal_id).show();
  	});
  	// Close modal popup
  	$('.close-btn').click(function() {
        $('.modal').hide();
    });


});
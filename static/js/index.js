$(document).ready(function()    {

	var selectedFrame = ""

  	var selectedFrame = $( "#selectedFrame" ).text();

  	if (selectedFrame != "0") {
  		$("#sel1").val(selectedFrame);
  	}
  	else {
  		$("#sel1").val("Customised");
  	}
	
	$( "select" ).change(function () {
    	var str = "";
    	$( "select option:selected" ).each(function() {
      		str += $( this ).text() + " ";
    	});
    	
		if ($.trim(str) != "Customised") {
			$( "#number" ).slideDown( "fast" );
			$( "#site" ).slideUp( "fast" );
			$( "#report" ).slideUp( "fast" );
			$("#client").prop('disabled', true);
			$("#editor").prop('disabled', true);
			var selectedOption = $("select.form-control").val();
			$.ajax({
				type: 'POST',
				url: '/ajax',
				processData: false,
				data: selectedOption,
				contentType: 'application/octet-stream; charset=utf-8',
				dataType: 'json',
				success: function(result) {
				// Handle or verify the server response if necessary.
					if (result) {

						$("#firstNameC").val(result.frame.client_firstname);
						$("#lastNameC").val(result.frame.client_lastname);
						$("#fulladdressFieldC").val(result.frame.client_full_adress);
						$("#phoneNumberC").val(result.frame.client_phone);
						$("#emailC").val(result.frame.client_mail);
						$("#firstNameE").val(result.frame.editor_firstname);
						$("#lastNameE").val(result.frame.editor_lastname);
						$("#fulladdressFieldE").val(result.frame.editor_full_adress);
						$("#phoneNumberE").val(result.frame.editor_phone);
						$("#emailE").val(result.frame.editor_mail);

					} else {
							
						$('#result').html('Failed to make a server-side call. Check your configuration and console.');
							
					}
				}

		  	}); 
		}
		else {
			$( "#number" ).slideUp( "fast" );
			$( "#site" ).slideDown( "fast" );
			$( "#report" ).slideDown( "fast" );
			$("#client").prop('disabled', false);
			$("#editor").prop('disabled', false);
			$(".form-control:not(#sel1):not(#visitDate):not(#redactionDate)").val("");
		}
  	}).change();

    // $('#sel1 option[value="+selectedFrame+"]').prop('selected', true);
	
    $("#slider-range-min").slider({
      range: "min",
      value: 1,
      min: 1,
      max: 100,
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
      }
    });
    $( "#amount" ).val( $( "#slider-range-min" ).slider( "value" ));
    
});
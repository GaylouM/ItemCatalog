$(document).ready(function () {  
    
    var placeSearch, autocomplete;
    var componentForm = {
      street_number: 'short_name',
      route: 'long_name',
      locality: 'long_name',
      administrative_area_level_1: 'short_name',
      country: 'long_name',
      postal_code: 'short_name'
    };
  
    $.fn.googleMapAutocompleteAddressC = function(opt) {  
        var options = $.extend({}, {  
        }, opt);  
        // each : si le plugin est énumérer tous les éléments du selector     
        return this.each(function(i, e){  
            //l’élément a qui s’applique le plugin ne peut etre qu un champs input  
            if(! $(this).is("input"))return ;  
            var autocomplete = new google.maps.places.Autocomplete($(this).get(0));  
            //Définir le champs comme autocomplete  
            //Attacher un évènement chaque fois que l’adresse saisie change     
            google.maps.event.addListener(autocomplete, 'place_changed', function() {  
                //Récupérer les lieux correspondants a l adresse saisie
                var place = '';
                var place = autocomplete.getPlace(); 

                for (var component in componentForm) {
                    document.getElementById(component).value = '';
                    document.getElementById(component).disabled = false;
                }

                for (var i = 0; i < place.address_components.length; i++) {
                    var addressType = '';
                    var addressType = place.address_components[i].types[0];
                    if (componentForm[addressType]) {
                        var val = place.address_components[i][componentForm[addressType]];
                        document.getElementById(addressType+"C").value = val;
                    }
                } 
          
            });//end addListener   
        });//end each    
   };//end googleMapAuocompleteAddress

   $.fn.googleMapAutocompleteAddressE = function(opt) {  
        var options = $.extend({}, {  
        }, opt);  
        // each : si le plugin est énumérer tous les éléments du selector     
        return this.each(function(i, e){  
            //l’élément a qui s’applique le plugin ne peut etre qu un champs input  
            if(! $(this).is("input"))return ;  
            var autocomplete = new google.maps.places.Autocomplete($(this).get(0));  
            //Définir le champs comme autocomplete  
            //Attacher un évènement chaque fois que l’adresse saisie change     
            google.maps.event.addListener(autocomplete, 'place_changed', function() {  
                //Récupérer les lieux correspondants a l adresse saisie
                var place = '';
                var place = autocomplete.getPlace(); 

                for (var component in componentForm) {
                    document.getElementById(component).value = '';
                    document.getElementById(component).disabled = false;
                }

                for (var i = 0; i < place.address_components.length; i++) {
                    var addressType = '';
                    var addressType = place.address_components[i].types[0];
                    if (componentForm[addressType]) {
                        var val = place.address_components[i][componentForm[addressType]];
                        document.getElementById(addressType+"E").value = val;
                    }
                } 
          
            });//end addListener   
        });//end each    
   };//end googleMapAuocompleteAddress

   $.fn.googleMapAutocompleteAddressS = function(opt) {  
        var options = $.extend({}, {  
        }, opt);  
        // each : si le plugin est énumérer tous les éléments du selector     
        return this.each(function(i, e){  
            //l’élément a qui s’applique le plugin ne peut etre qu un champs input  
            if(! $(this).is("input"))return ;  
            var autocomplete = new google.maps.places.Autocomplete($(this).get(0));  
            //Définir le champs comme autocomplete  
            //Attacher un évènement chaque fois que l’adresse saisie change     
            google.maps.event.addListener(autocomplete, 'place_changed', function() {  
                //Récupérer les lieux correspondants a l adresse saisie
                var place = '';
                var place = autocomplete.getPlace(); 

                for (var component in componentForm) {
                    document.getElementById(component).value = '';
                    document.getElementById(component).disabled = false;
                }

                for (var i = 0; i < place.address_components.length; i++) {
                    var addressType = '';
                    var addressType = place.address_components[i].types[0];
                    if (componentForm[addressType]) {
                        var val = place.address_components[i][componentForm[addressType]];
                        document.getElementById(addressType+"S").value = val;
                    }
                } 
          
            });//end addListener   
        });//end each    
   };//end googleMapAuocompleteAddress

});  
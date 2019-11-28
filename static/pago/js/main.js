function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

(function($) {    
    jQuery.validator.addMethod("validate_email", function(value, element) {

        if (/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(value)) {
            return true;
        } else {
            return false;
        }
    }, "Por favor digite un email válido.");   

    var form = $("#signup-form");
    form.validate({
        errorPlacement: function errorPlacement(error, element) {
             element.before(error); 
        },
        rules: {           
            'form1-nombre' : {
                required: true,
                minlength: 2,
            },
            'form1-schema_name' : {
                required: true,
                remote:
            {
                  url: "/validate/",
                  type: "get",                 
                  data:                  
                  {                                  
                    'form1-schema_name': function()
                      {
                          return $('#signup-form :input[name="form1-schema_name"]').val();
                      }
                  }
                },
                nowhitespace: true,
                minlength: 2,
            },
            'form3-first_name' : {
                required: true,
                lettersonly:true,
                minlength: 2,
            },

            'form3-last_name' : {
                required: true,
                lettersonly:true,
                minlength: 2,
            },
            'form2-cc' : {
                required: true,
                number:true,
                rangelength: [8, 20],
            },
            'form2-telefono' : {
                required: true,
                number:true,
                rangelength: [10, 12],
            },
           'form3-email' : {
                required: true,
                validate_email: true,
                remote:
                {
                      url: "/validate_email/",
                      type: "get",                 
                      data:                  
                      {                                  
                        'form3-email': function()
                          {
                              return $('#signup-form :input[name="form3-email"]').val();
                          }
                      }
                    },
            },

            'form2-pais' : {
                required: true,
                lettersonly:true,
            }, 

            'form3-username' : {
                required: true,
                alphanumeric: true,
                minlength: 3,
            },

            'form3-password1' : {
                required: true,
                minlength: 8,
            },
            
            'form3-password2' : {
                required: true,
                minlength: 8,  
                equalTo: "#id_form3-password1",                                             
            },

            'form2-nombre_banco' : {
                required: true,  
                lettersonly:true,                
                                                             
            },

            'form2-fecha_vencimiento' : {
                required: true,  
                date:true,                
                                                             
            },

            'form2-numero_tarjeta' : {
                required: true,  
                rangelength: [15, 16],
                number:true,                
                                                             
            },

            'form2-tipo_tarjeta' : {
                required: true,  
                lettersonly:true, 
                                                             
            },

            'form2-cvv' : {
                required: true,  
                rangelength: [3,4], 
                number:true,
                                                             
            },
            
         },
         
        messages: {
            'form1-nombre' : {
                required : "Por favor digite el nombre de la franquicia",
                minlength: "El nombre de la franquicia debe contener al menos dos caracteres",  
            },   
            'form1-schema_name' : {
                required : "Por favor digite el subdominio",
                remote: jQuery.validator.format("El subdomio {0} ya está siendo usado"),
                nowhitespace:"No se permite espacios en el subdominio",
                minlength: "El nombre del subdominio debe contener al menos dos caracteres",
            }, 
            'form3-first_name' : {
                required : "Por favor digite su nombre",
                lettersonly: "Solo se permiten caracteres alfabéticos",
                minlength: "El nombre debe contener al menos dos caracteres" ,
                
            }, 
            'form3-last_name' : {
                required : "Por favor digite su apellido",
                lettersonly: "Solo se permiten caracteres alfabéticos",
                minlength: "El apellido debe contener al menos dos caracteres" ,
            }, 
            'form2-cc' : {
                required : "Por favor digite su identificación",
                number: "Solo se permiten caracter númericos",
                rangelength:$.validator.format( "El número de identificación debe contener entre {0} y {1} caracteres." ),
            }, 
            'form2-telefono' : {
                required : "Por favor digite su número telefónico",
                number: "Solo se permiten caracter númericos",
                rangelength:$.validator.format( "El telefóno debe contener entre {0} y {1} caractéres." ),
            },
            'form3-email' : {
                required : "Por favor digite un email válido",
                remote: jQuery.validator.format("El email {0} ya está siendo usado"),
                email: "Por favor digite un email válido!"
            },

            'form2-pais' : {
                required : "Por favor elija su país",
                lettersonly: "Solo se permiten caracteres alfabéticos",
            }, 

            'form3-username' : {
                required : "Por favor digite su usuario",
                alphanumeric: "Solo se permiten caracteres alfanuméricos",
                minlength: $.validator.format( "El usuario debe contener al menos {0} caracteres." ),
            }, 
            'form3-password1' : {
                required : "Por favor digite su contraseña", 
                minlength: "La contraseña debe contener al menos 8 dígitos"
            }, 
            'form3-password2' : {
                required : "Por favor confirme su contraseña", 
                minlength: "La contraseña debe contener al menos 8 dígitos", 
                equalTo: "Las contraseñas deben coincidir"                                      
            },   
            
            'form2-nombre_banco'  : {
                required : "Por favor digite el nombre de su banco",   
                lettersonly: "Solo se permiten caracteres alfabéticos",                                                   
            }, 

            'form2-fecha_vencimiento' : {
                required: "Por favor digite la fecha de vencimiento de su tarjeta",  
                date:"Por favor digite una fecha válida",                
                                                             
            },

            'form2-numero_tarjeta' : {
                required: "Por favor digite el número de su tarjeta",  
                rangelength: "digite un número de tarjeta válido",   
                number:"digite un número de tarjeta válido",             
                                                             
            },

            'form2-tipo_tarjeta' : {
                required: "Por favor digite el tipo de su tarjeta",  
                lettersonly: "digite un tipo de tarjeta válido",               
                                                             
            },

            'form2-cvv' : {
                required: "Por favor digite el código cvv de su tarjeta",  
                rangelength:" digite un código CVV/CVC válido", 
                number: " digite un código CVV/CVC válido",
                                                             
            },
            
        }, 

        onfocusout: function(element) {
            $(element).valid();
        },
        highlight : function(element, errorClass, validClass) {
            $(element.form).find('.actions').addClass('form-error');
            $(element).removeClass('valid');
            $(element).addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element.form).find('.actions').removeClass('form-error');
            $(element).removeClass('error');
            $(element).addClass('valid');
        }
    });
    form.steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        labels: {
            previous : 'Anterior',
            next : 'Siguiente',
            finish : 'Terminar',
            current : ''
        },
        titleTemplate : '<span class="title">#title#</span>',
        onStepChanging: function (event, currentIndex, newIndex)
        {   
            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },

        onStepChanged: function (event, currentIndex, priorIndex)        
        {
            
         
        },
        onFinishing: function (event, currentIndex)
        {   
            form.validate().settings.ignore = ":disabled";
            return form.valid();
        },
        onFinished: function (event, currentIndex)        
        {  
           form.submit();
        },
        // onInit : function (event, currentIndex) {
        //     event.append('demo');
        // }
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });

   
   
        
})(jQuery);
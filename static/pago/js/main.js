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
            },
            'form1-schema_name' : {
                required: true,
            },
            'form3-first_name' : {
                required: true,
            },

            'form3-last_name' : {
                required: true,
            },
            'form2-cc' : {
                required: true,
            },
            'form2-telefono' : {
                required: true,
            },
           'form3-email' : {
                required: true,
                validate_email: true,
            },

            'form2-pais' : {
                required: true,
            }, 

            'form3-username' : {
                required: true,
            },

            'form3-password1' : {
                required: true,
                minlength: 8,
            },
            
            'form3-password2' : {
                required: true,
                minlength: 8,                
            },
         },
         
        messages: {
            'form1-nombre' : {
                required : "Por favor digite el nombre de la franquicia"
            },   
            'form1-schema_name' : {
                required : "Por favor digite el subdominio"
            }, 
            'form3-first_name' : {
                required : "Por favor digite su nombre"
            }, 
            'form3-last_name' : {
                required : "Por favor digite su apellido"
            }, 
            'form2-cc' : {
                required : "Por favor digite su identificación"
            }, 
            'form2-telefono' : {
                required : "Por favor digite su número telefónico"
            },
            'form3-email' : {
                required : "Por favor digite un email válido",
                email: "Por favor digite un email válido!"
            },

            'form2-pais' : {
                required : "Por favor elija su país"
            }, 

            'form3-username' : {
                required : "Por favor digite su usuario"
            }, 
            'form3-password1' : {
                required : "Por favor digite su contraseña", 
                minlength: "La contraseña debe contener al menos 8 dígitos"
            }, 
            'form3-password2' : {
                required : "Por favor confirme su contraseña", 
                minlength: "La contraseña debe contener al menos 8 dígitos"
                
            }
                                
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
            finish : 'Finish',
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
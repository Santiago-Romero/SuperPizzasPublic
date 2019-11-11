$(document).ready(function(){

//Evento cuando hay un cambio en el range de letra
$("#myRange-letra").change(function(){
    $("#tamanioLetraNum").text($("#myRange-letra").val()+"%");
    
});

//Evento cuando se seleciona un logo con input file
$("#inputFileLogoConfig").on('change',function(e){
 // Obtenemos la ruta temporal mediante el evento
 var TmpPath = URL.createObjectURL(e.target.files[0]);
 // Mostramos la ruta temporal
 $('#imagenLogoConfig').attr('src', TmpPath);
  
});

})
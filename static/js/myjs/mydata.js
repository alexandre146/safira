///**
// * Created by allan on 13/02/15.
// */
//
//
//$(document).ready(function(){
//    $('input').blur(function(){
//
//        validar_data()
//    });
//
//    $('#enviar').click(function(){
//       validar_data();
//   });
//
//    //$('form').submit(function(){
//    //    return validar_data()
//    //})
//
//});
//
//function atualizaData(){
//
//    elemento=document.getElementById("id_fase_Inicio");
//    submete=document.getElementById("id_fase_submeter");
//    comenta=document.getElementById("id_fase_comentar");
//    replica=document.getElementById("id_fase_replica");
//    treplica=document.getElementById("id_fase_treplica");
//    nota=document.getElementById("id_fase_nota");
//    fim=document.getElementById("id_fase_finalizada");
//
//    var formato='DD/MM/YYYY hh:mm:ss';
//
//    var data=moment(elemento.value,formato);
//    submete.value=data.add(1,'days').format(formato);
//
//    comenta.value=data.add(1,'days').format(formato);
//
//    replica.value=data.add(1,'days').format(formato);
//
//    treplica.value=data.add(1,'days').format(formato);
//
//    nota.value=data.add(1,'days').format(formato);
//
//    fim.value=data.add(1,'days').format(formato);
//    validar_data()
//
//}
//
//
//function validar_data(){
//    var formato='DD-MM-YYYY hh:mm:ss';
//    var elemento=moment($("#id_fase_Inicio").val(),formato);
//    var submete=moment($("#id_fase_submeter").val(),formato);
//    var comenta=moment($("#id_fase_comentar").val(),formato);
//    var replica=moment($("#id_fase_replica").val(),formato);
//    var treplica=moment($("#id_fase_treplica").val(),formato);
//    var nota=moment($("#id_fase_nota").val(),formato);
//    var fim=moment($("#id_fase_finalizada").val(),formato);
//
//
//    console.log(elemento.isBefore(submete));
//    $('input').parent().removeClass('has-error').addClass('has-success').children('input[type=datetime]').siblings('span').remove()
//
//    retorno=true;
//    if (!elemento.isBefore(submete)){
//        $('#id_fase_Inicio').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');;
//        retorno=false
//    }
//    if (!submete.isBefore(comenta)){
//        $('#id_fase_submeter').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');;
//        retorno=false
//    }
//    if (!comenta.isBefore(replica)){
//        $('#id_fase_comentar').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');;
//        retorno=false
//    }
//    if (!replica.isBefore(treplica)){
//        $('#id_fase_replica').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');;
//        retorno=false
//    }
//    if (!treplica.isBefore(nota)){
//        $('#id_fase_treplica').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');;
//        retorno=false
//    }
//    if (!nota.isBefore(fim)){
//        $('#id_fase_nota').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');
//        $('#id_fase_finalizada').parent().addClass('has-error').append('<span class="help-block">Verifique a data inserida, o correto são as fases seguirem uma ordem cronológica.</span>');
//        retorno=false
//    }
//
//
//
//    console.log(retorno)
//    return retorno
//
//
//
//}
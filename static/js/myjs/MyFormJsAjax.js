/*jslint browser: true*/
/*global $, jQuery, alert*/


function formTwoStep(id_form) {
    "use strict";
    var $divBtnStep, $btnStep, $divBtnBack, $btnBack, $colSpan, $row, $spanAviso;


    $divBtnStep = $('<div>').addClass('col-md-2').attr('id', 'divBtnStep');
    $btnStep = $('<a>').addClass('btn btn-info').append($('<i>').addClass('glyphicon glyphicon-arrow-right')).append(' Next').attr('id', 'next');


    $divBtnBack = $('<div>').addClass('col-md-1').attr('id', 'divBtnBack');
    $btnBack = $('<a>').addClass('btn btn-danger').append($('<i>').addClass('glyphicon glyphicon-arrow-left')).append(' Back').attr('id','back');


    $colSpan = $('<div>').addClass('col-md-7 alert alert-warning');
    $row = $('<div>').addClass('row');
    $spanAviso = $('<span>').addClass('glyphicon glyphicon-exclamation-sign').text('  Por Favor verifique os dados digitados antes de confirmar.').attr('id','spanAviso');


    $divBtnBack.append($btnBack);
    $divBtnStep.append($btnStep);
    $row.append($divBtnBack).append($divBtnStep);
    $(id_form).append($row);
    $colSpan.append($spanAviso);

    $btnStep.click(function () {
        var $btnSend;
        $btnSend = $('<button>').addClass('btn btn-success').append($('<i>').addClass('glyphicon glyphicon-ok')).append(' Confirmar').attr('id','confirma');

            $(id_form + ' input').prop('disabled',true);
            $(id_form + ' select').hide(0);

            $(this).parent().append($btnSend).parent().append($colSpan);
            $(this).hide(250);
            $btnSend.click(function () {

                $(id_form+' input').prop('disabled', false);
                var dados = $(id_form).serialize();

			    var $request=$.ajax({
				    method: "POST",
				    url: "",
				    data: dados,
                    mimeType:"JSON"

			});
                    $request.success(function (msg) {

                        $('#spanAviso').text(msg);

                        $(id_form).html(msg);

                        });

                $request.fail(function( jqXHR, textStatus ) {
                alert( "Request failed: " + textStatus );
        });
                //$(id_form).submit();


            return false;

            });


        });

        $btnBack.click(function(){
            location.reload();
        });

        }


function formToAjax(seletor){
    "use strict";

        $(seletor).submit(function(e){
            e.preventDefault();
            $.ajax({
                        url: $(this).attr('action'),
                        method:$(this).attr('method'),
                        data:$(this).serialize(),
                        success:function(msg){
                            generate('success','salvo com sucesso');
                        },
                        error:function(a,b){
                            generate('warning','algum erro aconteceu');
                        }
                    }
            );

        });

    }
/**
 * Created by allan on 22/06/15.
 */


function sendDeletationModal(class_elemento,titulo,mensagem,token){
    $('#modalTitulo').text(titulo);
    $('#modalMsg').text(mensagem);

    var $btnRow;


    $(class_elemento).click(function(){

        $btnRow=$(this);
        });

    $('#btnSimModal').click(function(){
        var $request=$.ajax({
            method: "POST",
            url: $btnRow.data('url'),
            data:{csrfmiddlewaretoken:token},
            mimeType:"JSON"

			});
            $request.success(function (msg) {


            generate('success',msg);
            $btnRow.parents('tr').remove();
                    });

                $request.fail(function( jqXHR, textStatus ) {
                generate('warning','Atualize a página');
        });

        });
    }

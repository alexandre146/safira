/**
 * Created by allan on 22/06/15.
 */
function generate(type,text) {
        var n = noty({
            text        : text,
            type        : type,
            dismissQueue: true,
            timeout     : 2000,
            closeWith   : ['click'],
            layout      : 'topRight',
            theme       : 'defaultTheme',
            maxVisible  : 10
        });

    }
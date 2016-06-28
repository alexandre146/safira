$ (function(){
    $('td').on('click', function() {
        displayForm($(this));
    });
});

function displayForm( cell ) {
    var column = cell.attr('class'),
        id = cell.closest('tr').attr('id'),
        cellWidth = cell.css('width'),
        prevContent = cell.text(),
        form = '<form action="javascript: this.preventDefault"><input type="text" name="newValue" size="4" value="'+prevContent+'"/><input type="hidden" name="id" value="'+id+' />' + '<input type="hidden" name="column" value="'+column+'"/></form>';
    
    cell.html(form).find('input[type=text]').focus().css('width',cellWidth);
    
    cell.on('click', function(){
       return false; 
    });
}


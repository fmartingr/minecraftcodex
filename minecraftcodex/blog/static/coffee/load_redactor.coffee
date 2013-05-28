window.onload = ->
    items = document.querySelectorAll '.redactor-editor'
    for item in items
        $(item).redactor()

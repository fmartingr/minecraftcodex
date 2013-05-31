window.onload = ->
    # Studio
    if window.Studio
        window.Studio.init '.studio-canvas', 320, 240
        window.modalManager.studio = window.Studio

    # Textures
    $('.texture-list .item').hover ->
        $('.texture-name').html $(@).attr('data-name')

    $('div.texture-list').on 'onmouseout', ->
        $('.texture.name').html 'Mouseover a texture'

    $('input.texture-search').on 'keyup', (event) ->
        # [enter] -> do search
        if event.which == 13 || event.keyCode == 13
            value = $(@).val()
            if value == ''
                $('.texture-list .item').removeClass 'hide'
            else
                $('.texture-list .item').addClass 'hide'
                $('.texture-list [data-name*="' + value + '"]').removeClass 'hide'

        # [esc] -> cancel search
        if event.which == 27 || event.keyCode == 27
            $(@).val ''
            $('.texture-list .item').removeClass 'hide'

    # input:select
    $('select.flatui').selectpicker
        style: 'btn-primary'
        menuStyle: 'dropdown-inverse'

    # Camera controls
    $(':radio[name="cameraType"]').on 'toggle', ->
        camera = $(@).val()
        window.Studio.onCameraChange camera

    $(':radio[name="cameraType"]:first').click()

    # Toggles
    $('[data-action="toggle"]').click ->
        target = $(this).attr 'data-target'
        $(target).toggle 'fast'

    # TESTS
    $('[data-studio="change-texture"]').click ->
        texture = $(this).attr('data-texture')
        window.Studio.changeTexture texture
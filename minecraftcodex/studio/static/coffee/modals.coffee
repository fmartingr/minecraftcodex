modalManager = 
    studio: null
    modals: null

    modal: (modalType) ->
        if modalType of @modals
            modal = @modals[modalType]
            context = modal.context
            source = $("##{modal.template}").html()
            template = Handlebars.compile source
            if source
                html = template context
                $('body').append html
                dom = $("##{context['modalId']}")

                if 'onClose' of modal
                    dom.on 'hidden', =>
                        modal.onClose(dom)

                if 'onInit' of modal
                    modal.onInit(dom)

                if 'onSubmit' of modal
                    dom.find('.btn-submit').click =>
                        modal.onSubmit(dom)

                dom.modal 'show'



modals =
    changeCanvas:
        type: 'confirm'
        template: 'modal-template-confirm'
        context:
            modalId: 'modal-changeCanvas'
            header: 'Change canvas'
            content: """
                    <form class="form-horizontal">
                        <div class="control-group">
                            <label class="control-label">Width</label>
                            <div class="controls">
                                <input type="text" id="canvasWidth" value="">
                            </div>
                        </div>
                        <div class="control-group">
                            <label class="control-label">Height</label>
                            <div class="controls">
                                <input type="text" id="canvasHeight" value="">
                            </div>
                        </div>
                    </form>
            """
        onInit: (domElement) ->
            domElement.find('input#canvasWidth').val modalManager.studio.width
            domElement.find('input#canvasHeight').val modalManager.studio.height

        onSubmit: (domElement) ->
            width = domElement.find('input#canvasWidth').val()
            height = domElement.find('input#canvasHeight').val()
            modalManager.studio.setSize width, height
            domElement.modal 'hide'

        onClose: (domElement) ->
            domElement.remove()


window.modalManager = modalManager
window.modalManager.modals = modals


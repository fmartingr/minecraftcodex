Studio =
    domElement: null
    _dom: null

    renderer: null
    width: 600
    height: 600

    scene: null

    camera: null
    _cameraType: null

    animating: false

    lights: []
    _lights: {}
    
    objects: []
    _objects: {}
    
    # OBJECT MANAGER
    objectManager:
        add: (object) ->
            if object of window.StudioObjects
                obj = new window.StudioObjects[object]
                obj.init
                    x: 16
                    y: 16
                    z: 16
                obj._id = @studio.objects.length + 1
                @studio.objects.push 
                    type: object
                    id: obj._id

                @studio._objects[obj._id] = obj
                @studio.scene.add @studio._objects[obj._id]._object

                context =
                    object_id: obj._id
                    name: obj.name

                template = Handlebars.compile $('#entity-template-simple').html()
                html = template(context)
                $('.entities-list').append(html)
                @setHandlers $(".entities-list .entity-#{obj._id}")


        list: ->
            return @studio._objects

        setHandlers: (dom) ->
            _this = @
            dom.find('.btn-edit').click ->
                console.log 'edit'

            dom.find('.btn-remove').click ->
                _this.remove $(@).parents('[data-objectid]').attr('data-objectid')

            dom.find('.check-visible').change ->
                console.log 'toggle!'

        remove: (object_id) ->
            if object_id of @studio._objects
                obj = @studio._objects[object_id]
                @studio.scene.remove obj._object
                delete @studio._objects[object_id]
                $(".entities-list .entity-#{object_id}").remove()



    # Methods
    checkWebGLsupport: ->
        return !!window.WebGLRenderingContext;

    # Callbacks
    onCameraChange: (cameraType) ->
        if "#{cameraType}Camera" of window.StudioCameras
            @_cameraType = cameraType
            @camera = new window.StudioCameras["#{cameraType}Camera"]
            @camera.init @width, @height
            @_camera = @camera._self
            if not @animating
                @animate()

    # Animation
    animate: ->
        if @scene and @camera
            if not @animating
                @animating = true
            @renderer.render @scene, @_camera

            @_animationFrame = requestAnimationFrame =>
                @animate()

    # Scene helpers
    setSize: (width, height) ->
        @width = parseInt width
        @height = parseInt height

        @renderer.setSize @width, @height
        @domElement.style.width = "#{@width}px"
        @domElement.style.height = "#{@height}px"

        @onCameraChange @_cameraType

    reset: ->
        cancelAnimationFrame @_animationFrame
        @renderer.domElement.remove()
        @init @_dom, @width, @height

    init: (dom, width, height) ->
        if not @checkWebGLsupport()
            return false

        # Renderer
        @domElement = document.querySelector dom
        @_dom = dom

        @renderer = new THREE.WebGLRenderer()
        @setSize width, height

        @domElement.appendChild @renderer.domElement

        # Scene
        @scene = new THREE.Scene()

        # Populate

        # Add all objects to object select
        objectsDom = $('select.object-list')
        for i of window.StudioObjects
            obj = window.StudioObjects[i]
            objectsDom.append "<option value=\"#{i}\">#{obj.name}</option>"

        # test
        @light = new THREE.DirectionalLight 0xffffff
        @light.position.set(1, 20, 60).normalize()
        @light.intensity = 1.6
        @scene.add @light

        @objectManager.studio = @

        #@object = new THREE.Mesh new THREE.CubeGeometry(16, 16, 16), new THREE.MeshNormalMaterial()

        #@scene.add @object
        # /test

        @animate()


window.Studio = Studio

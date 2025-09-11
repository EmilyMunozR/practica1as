function activeMenuOption(href) {
    $(".app-menu .nav-link")
    .removeClass("active")
    .removeAttr('aria-current')

    $(`[href="${(href ? href : "#/")}"]`)
    .addClass("active")
    .attr("aria-current", "page")
}

const app = angular.module("angularjsApp", ["ngRoute"])
app.config(function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix("")

    $routeProvider
    .when("/", {
        templateUrl: "/app",
        controller: "appCtrl"
    })
    .when("/integrantes", {
        templateUrl: "/integrantes",
        controller: "integrantesCtrl"
    })



        
    .when("/equiposintegrantes", {
        templateUrl: "/equiposintegrantes",
        controller: "equiposintegrantesCtrl"
    })
    .when("/equipos", {
        templateUrl: "/equipos",
        controller: "equiposCtrl"
    })
    .when("/proyectos", {
        templateUrl: "/proyectos",
        controller: "proyectosCtrl"
    })
    .when("/proyectosavances", {
        templateUrl: "/proyectosavances",
        controller: "proyectosavancesCtrl"
    })
    .otherwise({
        redirectTo: "/"
    })
})
app.run(["$rootScope", "$location", "$timeout", function($rootScope, $location, $timeout) {
    function actualizarFechaHora() {
        lxFechaHora = DateTime
        .now()
        .setLocale("es")

        $rootScope.angularjsHora = lxFechaHora.toFormat("hh:mm:ss a")
        $timeout(actualizarFechaHora, 1000)
    }

    $rootScope.slide = ""

    actualizarFechaHora()

    $rootScope.$on("$routeChangeSuccess", function (event, current, previous) {
        $("html").css("overflow-x", "hidden")
        
        const path = current.$$route.originalPath

        if (path.indexOf("splash") == -1) {
            const active = $(".app-menu .nav-link.active").parent().index()
            const click  = $(`[href^="#${path}"]`).parent().index()

            if (active != click) {
                $rootScope.slide  = "animate__animated animate__faster animate__slideIn"
                $rootScope.slide += ((active > click) ? "Left" : "Right")
            }

            $timeout(function () {
                $("html").css("overflow-x", "auto")

                $rootScope.slide = ""
            }, 1000)

            activeMenuOption(`#${path}`)
        }
    })
}])


///////////////// App Controller
app.controller("appCtrl", function ($scope, $http) {
    $("#frmInicioSesion").submit(function (event) {
        event.preventDefault()
        $.post("iniciarSesion", $(this).serialize(), function (respuesta) {
            if (respuesta.length) {
                window.location = "/#/integrantes"
                
                return
            }

             alert("Usuario y/o Contraseña Incorrecto(s)")
        })
    })
})


///////////////// integrantes controller

///// Buscar Integrantes
app.controller("integrantesCtrl", function ($scope, $http) {
    function buscarIntegrantes() {
        $.get("/tbodyIntegrantes", function (trsHTML) {
            $("#tbodyIntegrantes").html(trsHTML)
        })
    }
    buscarIntegrantes()
    
    Pusher.logToConsole = true

    var pusher = new Pusher('85576a197a0fb5c211de', {
      cluster: 'us2'
    });

    var channel = pusher.subscribe("integranteschannel")
    channel.bind("integrantesevent", function(data) {
       buscarIntegrantes()
    })


///// Insertar Integrantes
    $(document).on("submit", "#frmIntegrante", function (event) {
        event.preventDefault()

        $.post("/integrante", {
            idIntegrante: "",
            nombreIntegrante: $("#txtNombreIntegrante").val(),
        })
    })
})

///// Eliminar Integrantes
 $(document).on("click", ".btnEliminarIntegrante", function () {
        const id = $(this).data("id")

        if (confirm("¿Seguro que quieres eliminar este integrante?")) {
        $.post("/integrante/eliminar", { id: id }, function () {
            // Elimina la fila del DOM
            $(`button[data-id='${id}']`).closest("tr").remove()
        }).fail(function () {
            alert("Error al eliminar el integrante")
        })
    }
})


///////////////// proyectos controller

app.controller("proyectosCtrl", function ($scope, $http) {
    function buscarIntegrantes() {
        $.get("/tbodyProyectos", function (trsHTML) {
            $("#tbodyProyectos").html(trsHTML)
        })
    }

    buscarProyectos()
    
    Pusher.logToConsole = true

    var pusher = new Pusher('85576a197a0fb5c211de', {
      cluster: 'us2'
    });

    var channel = pusher.subscribe("proyectoschannel")
    channel.bind("proyectosevent", function(data) {
       buscarProyectos()
    })


    $(document).on("submit", "#frmProyectos", function (event) {
        event.preventDefault()

        $.post("/proyecto", {
            idProyecto: "",
            NombreProyecto: $("#txtNombreProyecto").val(),
            Equipo: $("#txtEquipo").val(),
            Objetivo: $("#txtObjetivo").val(),
            Estado: $("#txtEstado").val(),
            
        })
    })
})

//////////////Equipos Controllers///////////////////////////

app.controller("equiposCtrl", function ($scope, $http) {
    function buscarEquipos() {
        $.get("/tbodyEquipos", function (trsHTML) {
            $("#tbodyEquipos").html(trsHTML)
        })
    }

    buscarEquipos()
    
    Pusher.logToConsole = true

    var pusher = new Pusher('85576a197a0fb5c211de', {
      cluster: 'us2'
    });

    var channel = pusher.subscribe("equiposchannel")
    channel.bind("equiposevent", function(data) {
       buscarEquipos()
    })


    $(document).on("submit", "#frmEquipo", function (event) {
        event.preventDefault()

        $.post("/equipo", {
            idEquipo: "",
            nombreEquipo: $("#txtEquipoNombre").val(),
        })
    })
})


 $(document).on("click", ".btnEliminarEquipo", function () {
        const id = $(this).data("id")

        if (confirm("¿Seguro que quieres eliminar este Equipo?")) {
        $.post("/equipo/eliminar", { id: id }, function () {
            // Elimina la fila del DOM
            $(`button[data-id='${id}']`).closest("tr").remove()
        }).fail(function () {
            alert("Error al eliminar el Team")
        })
    }
})
////////////////////////////////////////////////////////////
///////////////// proyectosavances controller

///// Buscar Proyectos Avances
app.controller("proyectosavancesCtrl", function ($scope, $http) {
    function buscarProyectosAvances() {
        $.get("/tbodyProyectosAvances", function (trsHTML) {
            $("#tbodyProyectosAvances").html(trsHTML)
        })
    }
    buscarProyectosAvances()

    Pusher.logToConsole = true

    var pusher = new Pusher('85576a197a0fb5c211de', {
        cluster: 'us2'
    });

    var channel = pusher.subscribe("proyectosavanceschannel")
    channel.bind("proyectosavancesevent", function(data) {
        buscarProyectosAvances()
    })


///// Insertar Proyecto Avance
    $(document).on("submit", "#frmProyectoAvance", function (event) {
        event.preventDefault()

        $.post("/proyectoavance", {
            idProyectoAvance: "",
            idProyecto: $("#slcProyecto").val(),
            progreso: $("#txtProgreso").val(),
            descripcion: $("#txtDescripcion").val(),
        })
    })
})

///// Eliminar Proyecto Avance
$(document).on("click", ".btnEliminarAvance", function () {
    const id = $(this).data("id")

    if (confirm("¿Seguro que quieres eliminar este avance?")) {
        $.post("/proyectoavance/eliminar", { id: id }, function () {
            // Elimina la fila del DOM
            $(`button[data-id='${id}']`).closest("tr").remove()
        }).fail(function () {
            alert("Error al eliminar el avance")
        })
    }
})
///////////////////////////////////////////////////////////
const DateTime = luxon.DateTime
let lxFechaHora

document.addEventListener("DOMContentLoaded", function (event) {
    const configFechaHora = {
        locale: "es",
        weekNumbers: true,
        // enableTime: true,
        minuteIncrement: 15,
        altInput: true,
        altFormat: "d/F/Y",
        dateFormat: "Y-m-d",
        // time_24hr: false
    }

    activeMenuOption(location.hash)
})






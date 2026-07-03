// main.js - Scripts propios de EITEC

// reCAPTCHA callback para formulario de contacto
function onSubmit_contactanos(token) {
    var form = document.getElementById("form_contactanos");
    if (form.checkValidity()) {
        form.submit();
    } else {
        grecaptcha.reset();
        form.reportValidity();
    }
}

$(function () {
    // matchHeight
    $('.match').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false
    });

    // Menú hamburguesa
    $(document).on("click", ".hamburger", function () {
        $(this).toggleClass("is-active");
        $("header .options").toggleClass("active");
    });

    // Overlay de búsqueda
    $(document).on("click", "header .buscar", function () {
        $(".buscando").toggleClass('active');
    });

    $(document).on("click", ".buscando .mask", function () {
        $(".buscando").removeClass('active');
    });

    // Menú options desplegable
    $(document).on("click", ".options p", function () {
        $(this).parent().toggleClass("active");
        $(this).parent().siblings().removeClass("active");
        $(".header .mask").addClass("active");
    });

    $(document).on("click", ".options .active p", function () {
        $(this).parent().removeClass("active");
        $(".header .mask").toggleClass("active");
    });

    $(document).on("click", ".header .mask", function () {
        $(".options p").parent().removeClass("active");
        $(this).removeClass("active");
    });

    // Navbar reduce on scroll
    $(window).trigger('scroll');
    $(window).on('scroll', function () {
        var pixels = 50;
        if ($(window).scrollTop() > pixels) {
            $('#header').addClass('reduce');
        } else {
            $('#header').removeClass('reduce');
        }
    });

    // lightGallery (solo si existe la galería)
    if ($("#gallery").length) {
        $("#gallery").lightGallery({
            thumbnail: false
        });
    }

    // Limpiar opciones vacías del menú
    $(".header ul.options li a").each(function () {
        if ($(this).html().trim() == "") {
            $(this).closest(".options li").remove();
        }
    });
});

$(document).ready(function() {
    ("use strict");

    var window_width = $(window).width(),
        window_height = window.innerHeight,
        header_height = $(".default-header").height(),
        fitscreen = window_height - header_height;

    $(".fullscreen").css("height", window_height);
    $(".fitscreen").css("height", fitscreen);

    // Mobile Navigation
    if ($("#nav-menu-container").length) {
        var $mobile_nav = $("#nav-menu-container").clone().prop({
            id: "mobile-nav",
        });
        $mobile_nav.find("> ul").attr({
            class: "",
            id: "",
        });
        $("body").append($mobile_nav);
        $("body").prepend(
            '<button type="button" id="mobile-nav-toggle"><i class="fas fa-bars"></i></button>'
        );
        $("body").append('<div id="mobile-body-overly"></div>');
        $("#mobile-nav")
            .find(".menu-has-children")
            .prepend('<i class="fas fa-angle-down"></i>');

        $(document).on("click", ".menu-has-children i", function(e) {
            $(this).next().toggleClass("menu-item-active");
            $(this).nextAll("ul").eq(0).slideToggle();
            $(this).toggleClass("fa-angle-up fa-angle-down");
        });

        $(document).on("click", "#mobile-nav-toggle", function(e) {
            $("body").toggleClass("mobile-nav-active");
            $("#mobile-nav-toggle i").toggleClass("fa-times fa-bars");
            $("#mobile-body-overly").toggle();
        });

        $(document).click(function(e) {
            var container = $("#mobile-nav, #mobile-nav-toggle");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($("body").hasClass("mobile-nav-active")) {
                    $("body").removeClass("mobile-nav-active");
                    $("#mobile-nav-toggle i").toggleClass("fa-times fa-bars");
                    $("#mobile-body-overly").fadeOut();
                }
            }
        });
    } else if ($("#mobile-nav, #mobile-nav-toggle").length) {
        $("#mobile-nav, #mobile-nav-toggle").hide();
    }

    // Header scroll class
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $("#header").addClass("header-scrolled");
        } else {
            $("#header").removeClass("header-scrolled");
        }
    });
});
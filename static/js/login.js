$(function() {
    /*==================================================================
                                                                  [ Focus Contact2 ]*/
    $(".input100").each(function() {
        $(this).on("blur", function() {
            if ($(this).val().trim() != "") {
                $(this).addClass("has-val");
            } else {
                $(this).removeClass("has-val");
            }
        });
    });
    /*==================================================================
                                                                      [ Validate ]*/
    var input = $(".validate-input .input100");
    $(".validate-form").on("submit", function() {
        var check = true;
        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }
        return check;
    });
    $(".validate-form .input100").each(function() {
        $(this).focus(function() {
            hideValidate(this);
        });
    });

    function validate(input) {
        if ($(input).attr("type") == "email" || $(input).attr("name") == "email") {
            if (
                $(input)
                .val()
                .trim()
                .match(
                    /^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/
                ) == null
            ) {
                return false;
            }
        } else if ($(input).attr("type") == "tel") {
            if (
                $(input)
                .val()
                .trim()
                .match(/09(0[1-2]|1[0-9]|3[0-9]|2[0-1])-?[0-9]{3}-?[0-9]{4}$/) == null
            ) {
                return false;
            }
        } else if ($(input).attr("type") == "password") {
            if (
                $(input)
                .val()
                .trim()
                .match(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,8}$/) == null
            ) {
                return false;
            }
        } else {
            if ($(input).val().trim() == "") {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass("alert-validate");
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass("alert-validate");
    }
    /*******************************************************/
    var contentWayPoint = function() {
        var i = 0;
        $(".animate-box").waypoint(
            function(direction) {
                if (
                    direction === "down" &&
                    !$(this.element).hasClass("animated-fast")
                ) {
                    i++;

                    $(this.element).addClass("item-animate");
                    setTimeout(function() {
                        $("body .animate-box.item-animate").each(function(k) {
                            var el = $(this);
                            setTimeout(
                                function() {
                                    var effect = el.data("animate-effect");
                                    if (effect === "fadeIn") {
                                        el.addClass("fadeIn animated-fast");
                                    } else if (effect === "fadeInLeft") {
                                        el.addClass("fadeInLeft animated-fast");
                                    } else if (effect === "fadeInRight") {
                                        el.addClass("fadeInRight animated-fast");
                                    } else {
                                        el.addClass("fadeInUp animated-fast");
                                    }

                                    el.removeClass("item-animate");
                                },
                                k * 200,
                                "easeInOutExpo"
                            );
                        });
                    }, 100);
                }
            }, { offset: "85%" }
        );
    };
    $(function() {
        contentWayPoint();
    });
});
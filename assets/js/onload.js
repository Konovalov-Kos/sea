$(document).ready(function(){
    if($(window).scrollTop()>300){
        if(!$("header").hasClass("scrolled")){
            $("header").addClass("scrolled");
        }
    }

    $("#slider").bxSlider({
        prevText:'<i class="fas fa-angle-double-left"></i>',
        nextText:'<i class="fas fa-angle-double-right"></i>'
    });

    $("#clients_slider").bxSlider({
        pager:false,
        minSlides:1,
        maxSlides:6,
        moveSlides:1,
        slideWidth:170,
        slideMargin:30,
        prevText:'<i class="fas fa-angle-left"></i>',
        nextText:'<i class="fas fa-angle-right"></i>'
    });

    $('a[href="#search"]').on('click', function(event) {
        event.preventDefault();
        $('#search').addClass('open');
        $('#search > form > input[type="search"]').focus();
    });

    $('#search, #search button.close').on('click keyup', function(event) {
        if (event.target == this || event.target.className == 'close' || event.keyCode == 27) {
            $('#search').removeClass('open');
        }
    });

    $('form').submit(function(event) {
        event.preventDefault();
        return false;
    });

    $("#menu_toggle_wrap>button").click(function(){
        if($(this).hasClass("is-active")){
            $("#mobile_menu_block").fadeIn(200);
        }else{
            $("#mobile_menu_block").fadeOut(200);
        }
    });
    $("#mobile_menu_block .overlay").click(function(){
        $("#mobile_menu_block").fadeOut(200);
        $("#menu_toggle_wrap>button").removeClass('is-active');
    });

    $(window).scroll(function(){
        if($(window).scrollTop()>300){
            if(!$("header").hasClass("scrolled")){
                $("header").addClass("scrolled");
            }
        }else{
            if($("header").hasClass("scrolled")){
                $("header").removeClass("scrolled");
            }
        }
    });

});
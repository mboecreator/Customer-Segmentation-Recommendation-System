(function($) {
    var $window = $(window),
        $body = $('body'),
        $wrapper = $('#wrapper'),
        $header = $('#header'),
        $banner = $('#banner');

    // Breakpoints.
    breakpoints({
        xlarge:   [ '1281px',  '1680px' ],
        large:    [ '981px',   '1280px' ],
        medium:   [ '737px',   '980px'  ],
        small:    [ '481px',   '736px'  ],
        xsmall:   [ '361px',   '480px'  ],
        xxsmall:  [ null,      '360px'  ]
    });

    // Play initial animations on page load.
    $window.on('load', function() {
        window.setTimeout(function() {
            $body.removeClass('is-preload');
        }, 100);
    });

    // Menu.
    var $menu = $('#menu'),
        $menu_openers = $menu.children('ul').find('.opener');

    // Openers.
    $menu_openers.each(function() {
        var $this = $(this);

        $this.on('click', function(event) {
            // Prevent default.
            event.preventDefault();

            // Toggle.
            $menu_openers.not($this).removeClass('active');
            $this.toggleClass('active');

            // Trigger resize (sidebar lock).
            $window.triggerHandler('resize.sidebar-lock');
        });
    });

    // Sidebar.
    var $sidebar = $('#sidebar'),
        $sidebar_inner = $sidebar.children('.inner');

    // Inactive by default on <= large.
    breakpoints.on('<=large', function() {
        $sidebar.addClass('inactive');
    });

    breakpoints.on('>large', function() {
        $sidebar.removeClass('inactive');
    });

    // Hack: Workaround for Chrome/Android scrollbar position bug.
    if (browser.os == 'android'
    &&   browser.name == 'chrome')
        $('<style>#sidebar .inner::-webkit-scrollbar { display: none; }</style>')
            .appendTo($head);

    // Poptrox.
    $('.gallery').poptrox({
        useBodyOverflow: false,
        usePopupEasyClose: false,
        overlayColor: '#1f2328',
        overlayOpacity: 0.65,
        usePopupDefaultStyling: false,
        usePopupCaption: true,
        popupLoaderText: '',
        windowMargin: 44,
        usePopupNav: true
    });

    // Form validation
    $('form').on('submit', function(e) {
        var $form = $(this);
        
        // Check if it's the upload form
        if ($form.attr('action') === '/upload') {
            var $fileInput = $form.find('input[type="file"]');
            
            if ($fileInput.length > 0 && $fileInput[0].files.length === 0) {
                alert('Please select a file to upload');
                e.preventDefault();
                return false;
            }
        }
    });

    // Handle file upload
    $('input[type="file"]').on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        if (fileName) {
            $(this).next('.custom-file-label').html(fileName);
        }
    });

    // Menu functionality
    (function() {
        // Menu opener click handler
        $('.opener').on('click', function() {
            var $this = $(this);
            var $parent = $this.parent();
            
            // Toggle active class
            $parent.toggleClass('active');
            
            // Toggle submenu
            $parent.find('> ul').slideToggle(200);
        });

        // Smooth scroll for menu links
        $('a[href^="#"]').on('click', function(e) {
            e.preventDefault();
            
            var target = $(this.hash);
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 100
                }, 500);
            }
        });

        // Highlight current menu item
        $(window).on('scroll', function() {
            var scrollDistance = $(window).scrollTop();
            
            $('section').each(function(i) {
                if ($(this).position().top <= scrollDistance + 100) {
                    $('.menu-item').removeClass('active');
                    $('.menu-item').eq(i).addClass('active');
                }
            });
        });
    })();

})(jQuery); 
$(function() {
    
    /*
        AJAX GET
        $.ajax({
            type:'GET',
            url: '/api/order'
            success: function (data){
                console.log(data)
            }
            error: function()
        });

        // can use data inside function success, response is given as argument

        return sample:
        {
            'a':1,
            'b':2
        }

        or

        [
            a,
            b
        ]
        ---------------------

        $.each(<list>,<function>(i,<item>))

        $orders = $('#order');
        $orders.append('<li> my order </li>')

        ------------------------

        AJAX POST

        $.ajax({
            type:'POST',
            url: '/api/order',
            data: <object/dict>
            success: function (data){
                console.log(data)
            }
            error: function()
        });


        ------------------------

        AJAX DELETE

        $.ajax({
            type:'DELETE',
            url: '/api/order',
            data: <object/dict>
            success: function (data){
                console.log(data)
            }
            error: function()
        });

        **** if some elemnts are not there at loading of page/called later then eventListener
        might not attach to it. You can attach a listener to parent tag though

        eg let $orders = parent tag

        $orders.delegate('.remove','click', <function>);

        *** $(this) in success fuction refers to ajax request, so store $(this) outside
        if needed and use it inside with the variable

    */

    // Cashing input fields
    $term = $('#term');
    $cName = $('#cName');
    $cNum = $('#cNum');

    $Mstart = $('#Mstart')
    $Tstart = $('#Tstart')
    $Wstart = $('#Wstart')
    $Rstart = $('#Rstart')
    $Fstart = $('#Fstart')

    $Mend = $('#Mend')
    $Tend = $('#Tend')
    $Wend = $('#Wend')
    $Rend = $('#Rend')
    $Fend = $('#Fend')
    
    //Cashing course-info window and tables window
    $cInfo = $('#cInfo');
    $tables = $('#tables');



    //Reset button
    $('#reset').on('click', function() {
        $term.val('201901');
        $cName.val('AGEI');
        $cNum.val('');

        $Mstart.val(0).trigger('input');
        $Tstart.val(0).trigger('input');
        $Wstart.val(0).trigger('input');
        $Rstart.val(0).trigger('input');
        $Fstart.val(0).trigger('input');

        $Mend.val(24).trigger('input');
        $Tend.val(24).trigger('input');
        $Wend.val(24).trigger('input');
        $Rend.val(24).trigger('input');
        $Fend.val(24).trigger('input');
    });


    // Range sliders, start vs end are consistent
    $('.dayTime-slider.start').on('input', function() {

        //get relative end slider
        $end = $('#' + $(this).attr('id').substr(0,1) + 'end');
        
        // if less put it equal
        if (parseInt($(this).val()) > parseInt($end.val())){
            $end.val($(this).val()).trigger('input');
        }
    });

    $('.dayTime-slider.end').on('input', function() {
        
        //get relative start slider
        $start = $('#' + $(this).attr('id').substr(0,1) + 'start');
        
        // if more put it equal
        if (parseInt($(this).val()) < parseInt($start.val())){

            $start.val($(this).val()).trigger('input');
        }
    });

    
    
    // For Tabs switching 
    $('.tab-panels .tabs li').on('click', ToggleTab);
    
    function ToggleTab() {

        var $panel = $(this).closest('.tab-panels');
    
        $panel.find('.tabs li.active').removeClass('active');
        $(this).addClass('active');
    
        //figure out which panel to show
        var panelToShow = $(this).attr('rel');
    
        //hide current panel if exists (might not at start)
        var $activePanel = $panel.find('.panel.active')
        
        if ($activePanel[0]){
        
            $activePanel.hide(0, showNextPanel);
        
        } else {
            showNextPanel();
        }

        //show next panel
        function showNextPanel() {
            $(this).removeClass('active');
    
            $('#'+panelToShow).show(0, function() {
                $(this).addClass('active');
            });
        }
    };



    // Select course and put in tabs
    $('#select-course').on('click', function() {

        // validate values

        if($term.val() && $cName.val() && $cNum.val()){
            addTab($cInfo,'added','content<br/>content<br/>content<br/>content<br/>content');
        }

    });

    function addTab($tabPanels,header,content) {

        // create
        var $tab = $("<li></li>").text(header).attr({rel:header}).on('click',ToggleTab);

        // add tab
        $tabPanels.find('.tabs').append($tab);
        
        var $panel = $('<div></div>').addClass('panel').attr({id:header}).html(content)
        
        //create and add panel
        $tabPanels.append($panel);

        $tab.click();
    }

});
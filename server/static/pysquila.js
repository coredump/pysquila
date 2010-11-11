function startup() {
    var pickerOptions = { 'showOtherMonths' : true,
                    'selectOtherMonths' : true,
                    'showAnim' : 'blind'
                  }
    $.datepicker.setDefaults(pickerOptions);
                
    $('#datefrom').datepicker();
    $('#dateto').datepicker();
    $('#datefrom').datepicker("setDate", '-1');
    $('#dateto').datepicker("setDate", '+0');
    
    $('#submitbutton').button();
    $('#submitbutton').click(function() { update(); });

    $('#reporttypes').buttonset();

    return true
}

function update() {
    var rType;
    $('#reporttypes input:checked').each(function() {
        rType = this.id;
    });
    console.log(rType);
    return true; 
}

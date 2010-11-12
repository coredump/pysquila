/* Many of the code and inspiration for the js treatment of data came from
   the 'montanha' project by Gustavo Noronha: http://gitorious.org/montanha
*/

$('#document').ready(function() { 
                        startup();
                        show('topusers'); 
                     });

function show(reptype) {
    var initial_date = $('#datefrom').datepicker('getDate').getTime() / 1000;
    var final_date = $('#dateto').datepicker('getDate').getTime() / 1000;
    console.log(initial_date);
    console.log(final_date);
    var columns = [];

    if (reptype == 'topusers') {
        var string_columns = [ 'User', 'Connections', 'Bytes', '% of data',
                               'Used time', '% of time' ];
    }
    else if (reptype == 'topsites') {
        var string_columns = [ 'Site', 'Connections', 'Bytes' ];
    }
    else if (reptype == 'downloads') {
        var string_columns = [ 'User', 'Client Address', 'When', 'What' ];
    }
	
    for (n_columns = 0; n_columns < string_columns.length; n_columns++) {
      
        var col = Object();
        col.label = string_columns[n_columns];
        col.type = 'string';
        columns[n_columns] = col;
        
    }

    var table_elements = build_table_top(columns);
    var table = table_elements[0];
    var tbody = table_elements[1];
    table.setAttribute('class', 'fullwidth');


    var data_table = $('#resultstable').dataTable({
                            'bJQueryUI'   : true,
                            'bProcessing' : true,
                            'bServerSide' : true,
                            'sAjaxSource' : '/' + reptype,
                            'fnServerData': function ( sSource, aoData, fnCallback ) {
                                aoData.push( { 'name': 'initial_date', 'value': initial_date } );
                                aoData.push( { 'name': 'final_date', 'value': final_date } );
                                $.getJSON( sSource, aoData, function (json) { 
                                    fnCallback(json)
                                } );
                            }
    });

    // new FixedHeader(data_table);
    
}

function build_table_top(columns) {

    // Now let's start building the new data display.

    var table = document.createElement('table');
    table.setAttribute('id', 'resultstable');
    var thead = document.createElement('thead');
    table.appendChild(thead)

    var tr = document.createElement('tr');

    thead.appendChild(tr);

    // First of all, the titles.

    for (var i = 0; i < columns.length; i++) {

        var col_label = columns[i]['label'];
        var th = document.createElement('th');
        th.innerHTML = col_label;
        tr.appendChild(th);

    }


    var tbody = document.createElement('tbody');
    table.appendChild(tbody);

    // Place new table in the DOM, replacing the old one.

    var results_pane = document.getElementById('results');

    if (results_pane.firstChild != null) {
        results_pane.replaceChild(table, results_pane.firstChild);
    } else {
        results_pane.appendChild(table);
    }

return [table, tbody];

}


function startup() {
    var today = new Date();
    var pickerOptions = { 'showOtherMonths' : false,
                          'selectOtherMonths' : true,
                          'showAnim' : 'blind'
                        }
    $.datepicker.setDefaults(pickerOptions);
    
    $('#datefrom').datepicker({
        onSelect: function(date, inst) {
            console.log(date);
            $('#dateto').datepicker('option', 'minDate', date);
        }
    })

    $('#dateto').datepicker({
        minDate: today
        }
    );

    $('#datefrom').datepicker('setDate', '+0');
    $('#dateto').datepicker('setDate', '+1');

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
    show(rType);
    return true; 
}


<script type="text/javascript">
$(document).ready(() => {
  $('#load_msg').hide();
  $('#{{ table_id }}').show();
});
</script> 

{{ dataframe }}
<script type="text/javascript">

(function(){
    const onInit = function (e) {
      const api = this.api();

      // For each column
      api
        .columns()
        .eq(0)
        .each((colIdx) => {
          // Set the header cell to contain the input element
          const cell = $('.filters_{{ table_id }} th').eq(
            $(api.column(colIdx).header()).index(),
          );
          const title = $(cell).text();
          $(cell).html('<input type="text" class="fas fa-search" placeholder="&#xF002; Search" style="font-family:FontAwesome 5 Free; width:100%" />');

          // On every keypress in this input
          $(
            'input',
            $('.filters_{{ table_id }} th').eq($(api.column(colIdx).header()).index()),
          )
            .off('keyup change')
            .on('keyup change', function (e) {
              e.stopPropagation();

              // Get the search value
              $(this).attr('title', $(this).val());
              const regexr = '({search})';

              const cursorPosition = this.selectionStart;
              // Search the column for that value
              api
                .column(colIdx)
                .search(
                  this.value !== ''
                    ? regexr.replace('{search}', `(((${this.value})))`)
                    : '',
                  this.value !== '',
                  this.value === '',
                )
                .draw();

              $(this)
                .focus()[0]
                .setSelectionRange(cursorPosition, cursorPosition);
            });
        });
    };

    $(document).ready(() => {
      // Setup - add a text input to each header cell
      $('#{{ table_id }} thead tr')
        .clone(true)
        .addClass('filters_{{ table_id }}')
        .appendTo('#{{ table_id }} thead');

      $('#{{ table_id }}').DataTable({
        sDom: 'lrtip', // removes search box while still allowing search
        searching: true,
        order: [], // Prevent auto sorting
        pageLength: 30,
        orderCellsTop: true,
        fixedHeader: true,
        {{datatables_params}}
        initComplete: onInit,
      });
    });
})();
</script> 
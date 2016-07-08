var search = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('text'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: 'http://localhost:8080/search?q=%QUERY',
        wildcard: '%QUERY'
    }
});


$(document).ready(function() {
    $('#remote .typeahead').typeahead(null, {
        name: 'best-pictures',
        display: 'text',
        source: search
    });
});

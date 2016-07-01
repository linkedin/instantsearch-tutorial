var search = new Bloodhound({
    name: 'search',
    datumTokenizer: function (datum) { return Bloodhound.tokenizers.whitespace(datum); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: 'http://localhost:8080/search?q=%QUERY',
        wildcard: '%QUERY',
        rateLimitWait: 20,
    },
    limit: 20
});


$(document).ready(function() {
    $('#remote .typeahead').typeahead(null, {
        name: 'search-autocomplete',
        display: 'text',
        source: search,
        limit: 20,
        templates: {
            suggestion: function(data) {
                //return '<p><strong>' + data.text + '</strong>' + '<br>' + ' id: ' + data.payload.id + '</p>';
                return '<p>' + data.text + '</p>';
            }
        }
    });
    $('.typeahead').on('typeahead:selected', function(evt, item) {
        // do what you want with the item here
        window.location.href = 'http://stackoverflow.com/questions/' + item.post_id
    })
});

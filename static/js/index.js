// Handles getting user input, interacting with recommendation API, and rendering results
// requires jQuery, which is loaded by index.html

// TODO: redo input using semantic forms
$(document).on('ready', function() {
  $('#loading').hide();
  $('#errorMsg').hide();
  $('#noFollowings').hide();

  $('#submitButton').click(function() {
    $('#appendLog').empty()
    $('#loading').show()
    $('#errorMsg').hide();
    $('#noFollowings').hide();

    // Display current artist to user while loading recommendations
    var artist = $('#artistName').val();
    var textArtist= $('<div></div>').text(artist);
    var artistMarkup = '<p>' + 'If you\'re a fan of ' +
                       '<strong>' + textArtist.html() + ',</strong>' +
                       '<br> you might also dig: <p>'
    $('#appendLog').append(artistMarkup)

    // Get recommendations from server and append them w/ links to DOM
    var url = '/recommender/' + textArtist.text();
    $.get(url, function(data){
      if (data) {
        for (var i = 0; i < data.length; i++) {
          var artistUrl = data[i]['url'];
          var recommendationMarkup = '<a class="artistlink" href="' + 
                                     artistUrl + '">' + 
                                     data[i]['username'] + '</a><br>';
          $('#appendLog').append(recommendationMarkup);
        }
        $('#loading').hide();
      } else {
        // Artist doesn't follow any others, so recommendation can't work
        $('#loading').hide();
        $('#noFollowings').show();
      }
    }).fail(function() { 
      // Ajax request error-- for now we assume it's a lookup error for the input user
      $('#appendLog').empty()
      $('#errorMsg').empty()      
      $('#errorMsg').append('<em>Error, SoundCloud user "' + textArtist.html() + '" not found</em>');
      $('#loading').hide();
      $('#errorMsg').show();
    });
  });
});

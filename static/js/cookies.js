// yeah

$(document).on('ready', function() {

  var cookieString = document.cookie;

  if (cookieString.indexOf('fox') != -1) {
    $('#browser-cookies').append('Found this one.');
  }

  if (cookieString.indexOf('hound') != -1) {
    $('#http-only-cookies').append('Found this one.');
  }

});

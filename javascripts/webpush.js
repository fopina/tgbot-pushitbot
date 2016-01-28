$.dismissableError = function(title, message)
{
  $.blockUI({
    message: "<h3>ERROR " + title + "</h3><h1>" + message + "</h1><h6>click anywhere to dismiss</h6>",
    onOverlayClick: $.unblockUI,
    onBlock: function() {$('.blockUI.blockMsg.blockPage').click($.unblockUI)}
  });
}

$("#pushForm").submit(function(e) {
  e.preventDefault();
  var token = $("#inputToken").val();
  if (token.match(/^[a-f0-9]{32}$/) == null) {
    $.dismissableError('', 'Invalid token');
  }
  else if ($("#message").val() === "") {
    $.dismissableError('', 'Message is empty');
  }
  else {
    localStorage.setItem('pushit-token', token);
    localStorage.setItem('pushit-format', $("#inputFormat").val());
    $.blockUI({ message: 'Pushing...' });
    $.ajax('https://tgbots-fopina.rhcloud.com/pushit/' + $("#inputToken").val(), {
        type:"POST",
        data: $(this).serialize(),
        success:function(data, textStatus, jqXHR) {
          if (data.ok) {
            $.growlUI('Success', 'Message sent!');
          }
          else {
            $.dismissableError(data.code, data.description);
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {
          $.dismissableError('', 'API Failure');
        }
    });
  }
});
(function() {
  $("#inputToken").val(localStorage.getItem('pushit-token'));
  if (window.location.hash.match(/^#[a-f0-9]{32}$/)) {
    $("#inputToken").val(window.location.hash.substring(1));
  }
  $("#inputFormat").val(localStorage.getItem('pushit-format'));
})();

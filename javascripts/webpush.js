$("#pushForm").submit(function(e) {
  e.preventDefault();
  var token = $("#inputToken").val();
  if (token.match(/^[a-f0-9]{32}$/) == null) {
    alert('That token does not look valid!');
  }
  else {
    localStorage.setItem('pushit-token', token);
    localStorage.setItem('pushit-format', $("#inputFormat").val());
    var url = 'https://tgbots-fopina.rhcloud.com/pushit/' + $("#inputToken").val();
    $.ajax(url, {
        type:"POST",
        data: $(this).serialize(),
        success:function(data, textStatus, jqXHR) {
          if (data.ok) {
            alert("Message sent!");
          }
          else {
            alert("Failed (" + data.code + "): " + data.description);
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {alert("API Failure");}
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

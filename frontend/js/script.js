var wsUrl = "ws://localhost/ws/newsapi/?auth="
var newsSocket = null

var localCache = {
    data: {},
    get: function (keyword) {
        return this.data[keyword]
    },
    set: function (keyword, value) {
        this.data[keyword] = value
        return true
    },
    delte: function(){
        this.data = {}
        return true
    }
}

function updateResults(results){
  if(results!=[]){
    html = ""
    results.forEach(element => {
      html +=
      `<div class="newsplate"><div class="info"><h1><a href="`+element.url+`">`+element.title+`</a></h1>`+
      `<p>`+element.description+`</p></div><div class="thumb"><img src="`+element.urlToImage+`"></img></div></div>`
    });
    $("#results").html(html)
  } else {
    $("#results").html(`<div>Processing your request...</div>`)
  }
}


function readCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1,c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}

function logout(){
    localCache.delte()
    $("#liveContent, #register").hide()
}

$( document ).ready(function() {
  $("#createAccountBtn").on('click', function(){
    $("#liveContent, #formContent").hide()
    $("#register").show()
  })

  $("#loginBtn").on('click', function(){
    $.ajax({
      url: "/rest/login/",
      method: "POST",
      headers: {
        "X-CSRFToken": readCookie('csrftoken')
      },
      async: false,
      data: {
        "username": $("#lgnId").val(),
        "password": $("#lgnPassword").val()
      },
      success: function(result) {
        console.log(result)
        token = result.token
        $.ajaxSetup({
          headers: { 'Authorization': 'Token '+token }
        });
        document.cookie += ";token="+token
        newsSocket = new WebSocket(wsUrl+token)
        newsSocket.onmessage = function(e) {
          data = JSON.parse(e.data); 
          if("search" == data[0] && $("#searchBox").val().toUpperCase() == data[1]){
            updateResults(data[2])
          }
        }
        newsSocket.onopen = function open() {
          console.log('WebSockets connection created.');
        }
        $(".wrapper").hide()
        $("#liveContent").show()
      }});
  })

  $("#searchBox").autocomplete({
      source: function( request, response ) {
        $.ajax( {
          url: "/rest/suggest/",
          dataType: "json",
          data: {
            q: request.term
          },
          success: function( data ) {
            console.log(data)
            response( data );
          }
        });
      },
      minLength: 2,
      select: function( event, ui ) {
        console.log( "Selected: " + ui.item.value + " aka " + ui.item.id );
      }
    });

    $("#searchBtn").on('click', function(){
      $.ajax({
        url: '/rest/search/?q='+$("#searchBox").val(),
        success: function(result, txt, xhr) {
          if(xhr.status==200){
            html = ""
            updateResults(result)
            $("#results").html(html)
          } else if(xhr.status==202){
            updateResults([])
            newsSocket.send(JSON.stringify(["search", result]))
          }
        }
      })
    })
    if($.isEmptyObject(localCache.data)){
      logout()
    } else {
        $("#wrapper").hide()
    }
});
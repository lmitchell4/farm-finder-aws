$(document).ready(function() {
  
  // Add shadow to header when page is scrolled down.
  document.addEventListener("scroll", function() {
    if(window.pageYOffset > 0) {
      $("#header").addClass("header-shadow");
    } else {
      $("#header").removeClass("header-shadow");
    }
  });

  // Homepage tile animation.
  getDelayTime = function() {
    var times = [];
    var min = 1, max = 1;
    for(var i = 0; i < 3; i++) {
      times[i] = 1000*(Math.random() * (max - min + 1) + min);
    }
    max_1 = Math.max(times[0],times[1],times[2]);
    times[3] = 1000*(Math.random() * (max - min + 1) + min) + max_1;
    times[4] = 1000*(Math.random() * (max - min + 1) + min) + max_1;
    times[5] = 1000*(Math.random() * (max - min + 1) + min) + max_1;
    max_2 = Math.max(times[3],times[4],times[5]);
    times[6] = 1000*(Math.random() * (max - min + 1) + min) + max_2;
    times[7] = 1000*(Math.random() * (max - min + 1) + min) + max_2;
    times[8] = 1000*(Math.random() * (max - min + 1) + min) + max_2;

    return times;
  }
  var delay_times = getDelayTime();

  getRandomInt = function(x_min,x_max) {
    var x = (Math.floor(Math.random() * (x_max - x_min + 1)) + x_min);
    return x;
  }

  var x = getRandomInt(0,2);
  var y = ["","","","","","","","",""];
  y[x] = "glass.png";
  y[4] = "plant.png";
  if(x == 0) {
    y[8] = "heart.png";
  } else if(x == 1) {
    y[7] = "heart.png";
  } else if(x == 2) {
    y[6] = "heart.png";
  }

  turnCard = function(j) {
    if(y[j] != "") {
      $("#f" + j + " .back").css("background-image", "url('static/images/" + y[j] + "')");
    }
    $("#f" + j).addClass("flipped");
  }
  for(var i = 0; i < y.length; i++) {
    var timer = setTimeout(turnCard, delay_times[i], i);
  }

});
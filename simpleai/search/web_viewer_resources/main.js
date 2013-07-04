var graph_image = null;

function reset_graph_zoom() {
  graph_image.panzoom('reset');
}

function AlgorithmInfoCtrl($scope) {
  $scope.last_event = {name: "hola", description: "chau"};
  $scope.events = [];
  $scope.stats = [];

  //event stream client
  var source = new EventSource('/event_stream');
  source.onmessage = function(event) {
    $scope.$apply(function() {
      data = JSON.parse(event.data);
      $scope.last_event = data.event;
      $scope.stats = data.stats;
      $scope.events.push($scope.last_event);
    });

    if ($scope.last_event.name == 'finished') {
      reset_graph_zoom();
    }

    graph_image.attr('src', '/graph?unique=' + new Date().valueOf());
  };
}

function showTab(tab_name) {
  if (tab_name == 'graph' && $('#graph').is(':visible')) {
    reset_graph_zoom();
  } else {
    $('.tab').hide();
    $('#' + tab_name).show();
  }
}

function controlAlgorithm(order) {
  if ($('#help').is(':visible')) {
    showTab('graph');
  }
  $.ajax({url: '/control/' + order});
}

$(document).ready(function() {
  graph_image = $('#graph_image').panzoom();
  graph_image.panzoom();
  graph_image.bind('mousewheel', function(e) {
    if (e.originalEvent.wheelDelta / 120 > 0) {
      graph_image.panzoom('zoom');
    }
    else {
      graph_image.panzoom('zoom', true);
    }
  });

  $(window).keypress(function(event) {
    if (event.which == 13) {
      event.preventDefault();
      controlAlgorithm('step');
    }
    else if (event.which == 113 || event.which == 81) {
      event.preventDefault();
      controlAlgorithm('stop');
    }
    else if (event.which == 101 || event.which == 69) {
      event.preventDefault();
      controlAlgorithm('play');
    }
    else if (event.which == 112 || event.which == 80) {
      event.preventDefault();
      controlAlgorithm('pause');
    }
  });

  showTab('help');
});


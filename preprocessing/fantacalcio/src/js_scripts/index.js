$(document).ready(function() {

  d3.csv("src/data/stats.csv").then(function(data) {

    data.forEach(function(d) {
      d["Id"] = +d["Id"];
      d["Goal fatti"] = +d["Goal fatti"];
      d["Media voto"] = +d["Media voto"];
      d["Rigori segnati"] = +d["Rigori segnati"];
      d["Media Fantavoto"] = +d["Media Fantavoto"];
      d.goals = d["Goal fatti"] + d["Rigori segnati"];
    });

    var options = {
      num_goals: 3,
      num_players: 4,
      role: "D",
    }

    plotTopScorers(data, options);
    plotTopMediaFantavoto(data, options);

  });

});


function plotTopScorers(data, options) {

  var num_goals = (options.num_goals + 1) || 10;
  var num_players = options.num_players || 10;
  var role = options.role || null;

  console.log(num_goals);

  var margin = 150;

  var container = document.getElementById("cont");

  var width = container.clientWidth - margin,
    height = container.clientHeight - margin;

  var svg = d3.select("#cont").append("svg").attr("id", "topscorers");

  var svg = d3.select("#topscorers")

  console.log(width);
  console.log(height);

  var xScale = d3.scaleBand().range([0, width]).padding(0.5),
    yScale = d3.scaleLinear().range([height, 0]);

  var g = svg.append("g")
    .attr("transform", "translate(" + 50 + "," + 50 + ")");

  if (role != null) {
    data = data.filter(x => x["Ruolo"] == role);
  }

  data.sort((a, b) => b.goals - a.goals);
  filtered = data.filter(function(d) {
    return d.goals >= num_goals;
  });

  filtered = filtered.filter(function(d, i) {
    if (i < num_players) {
      return d
    }
  });
  console.log(filtered);


  xScale.domain(filtered.map(function(d) {
    return d["Nome"];
  }))
  yScale.domain([0, d3.max(filtered, function(d) {
    return d.goals;
  }) + 3]);

  yTickCount = d3.max(yScale.domain()) / 3;

  console.log(d3.max(yScale.domain()));
  console.log(yTickCount);

  if (filtered.length < num_players) {
    title = 'Players who scored more than ' + String(num_goals - 1) + ' goals in Serie A 2019-2020';
  } else {
    title = 'Top ' + String(num_players) + ' players who scored more than ' + String(num_goals) + ' goals in Serie A 2019-2020';
  }

  g.append("g")
    .attr("class", "grid")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale))
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-0.6em")
    .attr("dy", "0.9em")
    .attr("transform", "rotate(-60)");

  g.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(yScale)
      .tickFormat(function(d) {
        return d;
      })
      .ticks(yTickCount)
    );

  g.append('text')
    .attr('x', -(height / 2))
    .attr('y', -30)
    .attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle')
    .text('Number of goals')

  g.append('text')
    .attr('x', width / 2)
    .attr('y', -15)
    .attr('text-anchor', 'middle')
    .text(title)

  g.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(yScale)
      .tickSize(-width, 0, 0)
      .tickFormat("")
      .ticks(yTickCount)
    );

  g.selectAll(".bar")
    .data(filtered)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) {
      return xScale(d["Nome"]);
    })
    .attr("y", function(d) {
      return yScale(d.goals);
    })
    .attr("width", xScale.bandwidth())
    .attr("height", function(d) {
      return height - yScale(d.goals);
    });

}

function plotTopMediaFantavoto(data, options) {

  var num_players = options.num_players || 15;

  var margin = 150;

  var container = document.getElementById("cont");

  var width = container.clientWidth - margin,
    height = container.clientHeight - margin;

  var svg = d3.select("#cont").append("svg").attr("id", "topmedia");

  var svg = d3.select("#topmedia")

  console.log(width);
  console.log(height);

  var xScale = d3.scaleBand().range([0, width]).padding(0.5),
    yScale = d3.scaleLinear().range([height, 0]);

  var g = svg.append("g")
    .attr("transform", "translate(" + 50 + "," + 50 + ")");

  data.sort((a, b) => b["Media Fantavoto"] - a["Media Fantavoto"]);
  filtered = data.filter(function(d, i) {
    if (i < num_players) {
      return d["Media Fantavoto"];
    }
  });


  xScale.domain(filtered.map(function(d) {
    return d["Nome"];
  }))
  yScale.domain([0, d3.max(filtered, function(d) {
    return d["Media Fantavoto"];
  }) + 1]);

  g.append("g")
    .attr("class", "grid")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale))
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-0.6em")
    .attr("dy", "0.9em")
    .attr("transform", "rotate(-60)");

  g.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(yScale)
      .tickFormat(function(d) {
        return d;
      })
      .ticks(23)
    );

  g.append('text')
    .attr('x', -(height / 2))
    .attr('y', -30)
    .attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle')
    .text('Fantavoto average')

  g.append('text')
    .attr('x', width / 2)
    .attr('y', -15)
    .attr('text-anchor', 'middle')
    .text('Top ' + String(num_players) + ' players who had the highest Fantavoto in Serie A 2019-2020')

  g.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(yScale)
      .tickSize(-width, 0, 0)
      .tickFormat("")
      .ticks(23)
    );

  g.selectAll(".bar")
    .data(filtered)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) {
      return xScale(d["Nome"]);
    })
    .attr("y", function(d) {
      return yScale(d["Media Fantavoto"]);
    })
    .attr("width", xScale.bandwidth())
    .attr("height", function(d) {
      return height - yScale(d["Media Fantavoto"]);
    });
}

function showTSbuttons() {
  var row = $('<div />')
    .addClass("dropdown")
    .appendTo($('#menus'))

  var button = $('<button />')
    .addClass('dropbtn')
    .appendTo(row)

  var dropdownContent = $('<div />')
    .addClass("dropdown-content")
    .appendTo(button)
    .text("Choose number of goals")

  var con1 = $('<a />')
    .attr("onclick", "updateNumGoals(" + 0 + ")")

  //FIX HERE! go on with others buttons

}

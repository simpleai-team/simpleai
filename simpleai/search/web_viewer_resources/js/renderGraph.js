// ************** Generate the tree diagram	 *****************
function renderGraph(graphData) {
    var margin = { top: 20, right: 120, bottom: 20, left: 120 },
        width = (graphData.nodes_count * 50) - margin.right - margin.left,
        height = ((graphData.max_depth + 1) * 200) - margin.top - margin.bottom;

    var i = 0,
        duration = 0,
        root;

    var tree = d3.layout.tree().size([width, height]);

    var diagonal = d3.svg.diagonal().projection(function (d) { return [d.x, d.y]; });

    $("#graph-image").html("");

    var svg = d3.select("#graph-image").append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    function update(source) {
        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

        // Normalize for fixed-depth.
        nodes.forEach(function (d) { d.y = d.depth * 180; });

        // Update the nodes…
        var node = svg.selectAll("g.node").data(nodes, function (d) {
            return d.id || (d.id = ++i);
        });

        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
            .attr("class", function (d) {
                let classesCss = ""
                d.modifiers?.forEach(modifier => {
                    switch (modifier) {
                        case modifier === "choosen":
                            classesCss += "choosen"
                        case modifier === "newly":
                            classesCss += "newly"
                        case modifier === "goal":
                            classesCss += "goal"
                        case modifier === "visited":
                            classesCss += "visited"
                        default:
                            classesCss += "newly"
                    }
                })
                return `node ${classesCss}`
            })
            .attr("transform", function (d) { return "translate(" + source.x0 + "," + source.y0 + ")"; })
            .on("click", click);

        nodeEnter.append("circle")
            .attr("r", 1e-6)
            .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; })
            .on("mouseenter", function(d){
                d3.select(this.parentNode).select("text").text(function (d) { return d.name })
                
            })
            .on("mouseleave", function(d){
                d3.select(this.parentNode).select("text").text(function (d) { return `${d.name.slice(0, 10)}...`; })

            });

        nodeEnter.append("text")
            .attr("x", function (d) { return d.children || d._children ? -13 : 13; })
            .attr("dy", ".35em")
            .attr("text-anchor", function (d) { return d.children || d._children ? "end" : "start"; })
            .text(function (d) { return `${d.name.slice(0, 10)}...`; })
            .style("fill-opacity", 1e-6)

        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });

        nodeUpdate.select("circle")
            .attr("r", 10)
            .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; });

        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function (d) { return "translate(" + source.x + "," + source.y + ")"; })
            .remove();

        nodeExit.select("circle")
            .attr("r", 1e-6);

        nodeExit.select("text")
            .style("fill-opacity", 1e-6);

        // Update the links…
        var link = svg.selectAll("path.link")
            .data(links, function (d) { return d.target.id; });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function (d) {
                var o = { x: source.x0, y: source.y0 };
                return diagonal({ source: o, target: o });
            });

        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function (d) {
                var o = { x: source.x, y: source.y };
                return diagonal({ source: o, target: o });
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function (d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    // Toggle children on click.
    function click(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    }

    root = graphData.nodes[0];
    root.x0 = height / 2;
    root.y0 = 0;
    update(root);
    d3.select(self.frameElement).style("height", "500px");
}

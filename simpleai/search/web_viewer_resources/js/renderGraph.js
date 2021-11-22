// ************** Generate the tree diagram	 *****************
function renderGraph(graphData) {
    var margin = { top: 30, right: 150, bottom: 30, left: 150 },
        width = (graphData.nodes_count * 75) - margin.right - margin.left,
        height = (graphData.max_depth * 200) - margin.top - margin.bottom;

    var nodeIndex = 0,
        duration = 0,
        root;

    var tree = d3.layout.tree().size([width, height]);

    var diagonal = d3.svg.diagonal().projection(function (node) { return [node.x, node.y]; });

    /* It need to re-render the tree */
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
        nodes.forEach(function (node) { node.y = node.depth * 180; });

        // Update the nodes…
        var node = svg.selectAll("g.node").data(nodes, function (node) {
            return node.id || (node.id = ++nodeIndex);
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
            .attr("transform", function (node) { return "translate(" + source.x0 + "," + source.y0 + ")"; })
            .on("click", click);

        nodeEnter.append("circle")
            .attr("r", 1e-6)
            .style("fill", function (node) { return node._children ? "lightsteelblue" : "#fff"; })
            .on("mouseenter", function (node) {
                d3.select(this.parentNode).select("text")
                .text(function (node) { return `${node.tooltip}` })
            })
            .on("mouseleave", function(node){
                d3.select(this.parentNode).select("text").text(function (node) { return `${node.name}`; })

            });

        nodeEnter.append("text")
            .attr("x", function (node) { return node.children || node._children ? -13 : 13; })
            .attr("dy", "2.35em")
            .attr("dx", function (node) { return node.children || node._children ? "6.35em" : "-6.35em";} )
            .attr("text-anchor", function (node) { return node.children || node._children ? "end" : "start"; })
            .text(function (node) { return `${node.name}` })
            .style("fill-opacity", 1e-6)

        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function (node) { return "translate(" + node.x + "," + node.y + ")"; });

        nodeUpdate.select("circle")
            .attr("r", 10)
            .style("fill", function (node) { return node._children ? "lightsteelblue" : "#fff"; });

        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function (node) { return "translate(" + source.x + "," + source.y + ")"; })
            .remove();

        nodeExit.select("circle")
            .attr("r", 1e-6);

        nodeExit.select("text")
            .style("fill-opacity", 1e-6);

        // Update the links…
        var link = svg.selectAll("path.link")
            .data(links, function (node) { return node.target.id; });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function (node) {
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
            .attr("d", function (node) {
                var o = { x: source.x, y: source.y };
                return diagonal({ source: o, target: o });
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function (node) {
            node.x0 = node.x;
            node.y0 = node.y;
        });
    }

    // Toggle children on click.
    function click(node) {
        if (node.children) {
            node._children = node.children;
            node.children = null;
        } else {
            node.children = node._children;
            node._children = null;
        }
        update(node);
    }

    root = graphData.nodes[0];
    root.x0 = height / 2;
    root.y0 = 0;
    update(root);
    d3.select(self.frameElement).style("height", "500px");
}

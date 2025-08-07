function renderBarChart(targetId, width, height, data) {
  const margin = { top: 20, right: 20, bottom: 60, left: 40 };

  const svg = d3.select(targetId)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const x = d3.scaleBand()
    .domain(data.map(d => d.label))
    .range([margin.left, width - margin.right])
    .padding(0.1);

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.values)])
    .nice()
    .range([height - margin.bottom, margin.top]);

  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "rotate(-40)")
    .style("text-anchor", "end");

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));

  svg.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", d => x(d.label))
    .attr("y", d => y(d.values))
    .attr("width", x.bandwidth())
    .attr("height", d => height - margin.bottom - y(d.values))
    .attr("fill", "#69b3a2");
}


function renderLineChart(targetId, width, height, data) {
  const margin = { top: 20, right: 20, bottom: 60, left: 40 };

  const svg = d3.select(targetId)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const x = d3.scaleBand()
    .domain(data.map(d => d.label))
    .range([margin.left, width - margin.right])
    .padding(0.1);

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.values)])
    .nice()
    .range([height - margin.bottom, margin.top]);

  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "rotate(-40)")
    .style("text-anchor", "end");

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));

  const line = d3.line()
    .x(d => x(d.label) + x.bandwidth() / 2)
    .y(d => y(d.values));

  svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "#69b3a2")
    .attr("stroke-width", 2)
    .attr("d", line);

  svg.selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", d => x(d.label) + x.bandwidth() / 2)
    .attr("cy", d => y(d.values))
    .attr("r", 4)
    .attr("fill", "#69b3a2");
}

function geoChart(targetId, width, height, geoData) {
    const svg = d3.select(targetId)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const projection = d3.geoOrthographic()
        .scale(height / 2.1)
        .translate([width / 2, height / 2])
        .clipAngle(90)
        .precision(0.1);

    const path = d3.geoPath().projection(projection);

    let rotation = [0, 0];
    let v0, r0, q0;

    d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(world => {
        const countries = topojson.feature(world, world.objects.countries);

        const sphere = svg.append("path")
            .datum({ type: "Sphere" })
            .attr("fill", "#e0f7fa")
            .attr("stroke", "#000")
            .attr("stroke-width", 0.5)
            .attr("d", path);

        const countryPaths = svg.append("g")
            .selectAll("path")
            .data(countries.features)
            .enter().append("path")
            .attr("fill", "#ccc")
            .attr("stroke", "#999")
            .attr("stroke-width", 0.5)
            .attr("d", path);

        const points = svg.append("g")
            .selectAll("circle")
            .data(geoData)
            .enter()
            .append("circle")
            .attr("cx", d => projection([+d.lon, +d.lat])[0])
            .attr("cy", d => projection([+d.lon, +d.lat])[1])
            .attr("r", 3)
            .attr("fill", "red")
            .attr("opacity", 0.6);

        svg.call(d3.drag()
            .on("start", () => {
                v0 = versor.cartesian(projection.invert(d3.pointer(event, svg.node())));
                r0 = rotation;
                q0 = versor(r0);
            })
            .on("drag", () => {
                const v1 = versor.cartesian(projection.invert(d3.pointer(event, svg.node())));
                const q1 = versor.multiply(q0, versor.delta(v0, v1));
                rotation = versor.rotation(q1);
                projection.rotate(rotation);
                sphere.attr("d", path);
                countryPaths.attr("d", path);
                points.attr("cx", d => projection([+d.lon, +d.lat])[0])
                      .attr("cy", d => projection([+d.lon, +d.lat])[1]);
            })
        );
    });
}

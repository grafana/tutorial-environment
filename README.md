# Introduction to Monitoring with Grafana

This repository contains the training resources for the _Introduction to Monitoring with Grafana_ workshop.

## Prequisites

You will need to have the following installed locally to complete this workshop:

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

If you're running Docker for Desktop for macOS or Windows, Docker Compose is already included in your installation.

## Set up the sample application

- Clone this repository:

```
git clone https://github.com/grafana/monitoring-intro-workshop.git
```

- Go to the directory where you cloned this repository:

```
cd monitoring-intro-workshop
```

- Start the sample application:

```
docker-compose up -d
```

This might take a few minutes, depending on your internet connection.

- Ensure all services are up-and-running:

```
docker-compose up -d
```

All services should say `Up`.

- Browse to [localhost:8081](http://localhost:8081) to start using the sample application.

## Time series with Prometheus

The sample application exposes its metrics under the [/metrics](http://localhost:8081/metrics) endpoint. Prometheus uses this endpoint to collect measurements.

- Browse to [http://localhost:8081/metrics](http://localhost:8081/metrics) to see all the metrics exposed by the sample application.

- Refresh the page a couple of times to take new measurements.

## Visualizing time series

- Browse to [Grafana](http://localhost:3000), and log in using the default credentials:
  - Username: admin
  - Password: admin

### Add a Prometheus data source

- In the side bar, click **Configuration** -> **Data Sources**.

- Click **Add data source**, and select **Prometheus** from the list of available data sources.

- In the **URL** box, type `http://prometheus:9090`.

- Click **Save & Test** to save your changes.

### Explore time series

Grafana lets you explore and compare metrics from your data sources.

- In the side bar, click **Explore**.

- In the **Query** box, type the following, and press Enter:

```
tns_request_duration_seconds_count
```

- In the top right corner, click the drop down on the **Run Query** button, and select "5s" to have Grafana run your query every 5 seconds.

PromQL is a powerful query language that lets you apply transformations to your queries. Since `tns_request_duration_seconds_count` is a _counter_, it will only increase. For something more interesting, try the `rate` and `sum` functions:

- Add the `rate` function to your query to visualize the rate of requests per second:

```
irate(tns_request_duration_seconds_count[5m])
```

- Add the `sum` function to your query to group time series by route:

```
sum(irate(tns_request_duration_seconds_count[5m])) by(route)
```

Go back to the sample application and generate some traffic by adding new links, voting, or just refresh the browser.

_Note:_ If you don't want to manually refresh the browser, [hey](https://github.com/rakyll/hey) is a great tool to generate traffic.

```
hey -m GET http://localhost:8081
hey -m POST -H "Content-Type: application/x-www-form-urlencoded" -d "title=Example&url=http://example.com" http://localhost:8081/post
```


## Visualizing logs

### Add a Loki data source

- In the side bar, click **Configuration** -> **Data Sources**.

- Click **Add data source**, and select **Loki** from the list of available data sources.

- In the **URL** box, type `http://loki:3100`.

- Click **Save & Test** to save your changes.

### Explore logs

- In the side bar, click **Explore**.

- In the dropdown at the top, select the "Loki" data source.

- In the **Query** box, type the following, and press Enter to display all logs within the log file of the sample application:

```
{filename="/var/log/tns-app.log"}
```

- Filter log lines based on a substring:

```
{filename="/var/log/tns-app.log"} |= "error"
```

Grafana only shows logs within the current time interval. This lets you narrow down your logs to a certain time.

- Click and drag over a log occurrence in the graph to filter logs based on time.

## Building dashboards

### Panels

Panels are the building blocks of Grafana dashboards. Every panel consists by a _query_ and a _visualization_.

- In the side bar, click **Create** to create a new dashboard.
- Click **Add query**, and enter the query from earlier:

```
sum(rate(tns_request_duration_seconds_count[5m])) by(route)
```

- In the **Legend** box, enter `{{route}}` to rename the time series in the legend.

- Click the **Visualization** panel tab to the left to go to the visualization settings for the panel.

- Enable the **Stack** option to stack the series on top of each other. This makes it easier to see the total traffic across all routes.

- Click the **General** panel tab, and change the title to "Traffic".

- Click the arrow in the top-left corner to go back to the dashboard view.

- Click the **Save dashboard** icon at the top of the dashboard, to save your dashboard.

### Annotations

Whenever things go bad, it can be invaluable to understand the context in which the system failed. Time of last deploy, or database migration can offer insight into what might have caused an outage. Annotations lets you add custom events to your graphs.

- To manually add an annotation, left-click anywhere in your graph, and click **Add annotation**.
- Describe what you did, and optionally add tags for more context.

Let your team know that you did some testing for a while, by clicking and dragging an interval, while pressing Ctrl (or Cmd on macOS).

Instead of manually annotating your dashboards, you can tell Grafana to get annotations from a data source.

- Select **Dashboard settings** from the top of the dashboard view.
- Click **Annotations**, then **New Annotation Query**.
- In the **Name** box, type "Errors".
- Select "Loki" from the **Data source** drop down.
- In the **Query** box, type a LogQL query:

```
{filename="/var/log/tns-app.log"} |= "error"
```

- Click **Add** and go back to your dashboard.

The log lines returned by your query are now displayed as annotations in the graph.

## Effective monitoring

### RED

RED, or Rate, Errors, and Duration, is a method for monitoring services. Let's create a RED dashboard for our sample application.

In the last exercise, you created a panel to visualize the _Rate_ of requests, or traffic.

Next, we'll add one for _Errors_, and _Duration_.

- Add another Graph panel for _Errors_:

```
sum(irate(tns_request_duration_seconds_count{status_code!~"2.."}[5m]))
```

- Add a third Graph panel to display _Duration_:

```
histogram_quantile(0.99, sum(irate(tns_request_duration_seconds_bucket[5m])) by(le))
```

To be able to troubleshoot any errors, let's add a logs panel to our dashboard:

- Create another panel with a Logs visualization.
- In the **Query** settings, select the "Loki" data source, and enter the query:

```
{filename="/var/log/tns-app.log"}
```

- Go back to you dashboard. With the current dashboard, we can quickly see when an error occurred, and what may have caused it.

/*!

=========================================================
* Paper Dashboard React - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)

* Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
// react plugin used to create charts
import { Line, Pie } from "react-chartjs-2";
// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,
} from "reactstrap";
import Chart from "react-apexcharts";
// core components
import {
  dashboard24HoursPerformanceChart,
  dashboardEmailStatisticsChart,
  // dashboardNASDAQChart,
} from "variables/charts.js";
import axios from "axios";
import moment from "moment";

class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      AqiInfo: null,
      weatherInfo: null,
      weatherInfoExtraTemp_min: null,
      weatherInfoExtraTemp_max: null,
      weatherTimeStamp: null,
      windSpeedInfo: null,
      time_zone: null,
      btcPrice: null,
      options: {
        chart: {
          id: "basic-bar",
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999],
        },
      },
      series: [
        {
          name: "series-1",
          data: [30, 40, 45, 50, 49, 60, 70, 91],
        },
      ],
    };
  }

  componentDidMount() {
    axios
      .request({
        method: "GET",
        url:
          "http://api.openweathermap.org/data/2.5/weather?q=Dublin&units=metric&appid=d50542e129f589c12a362e67f91906fe",
      })
      .then((response) => {
        const weatherInfo = response.data.main.temp;
        const weatherInfoExtraTemp_min = response.data.main.temp_min;
        const weatherInfoExtraTemp_max = response.data.main.temp_max;
        const time_zone = response.data.timezone;
        const weatherTimeStamp = response.data.sys.sunrise - -time_zone;
        const windSpeedInfo = response.data.wind.speed;
        console.log("<<<< API INFO >>>>");
        console.log(response.data);
        this.setState({ weatherInfo: weatherInfo });
        this.setState({ weatherInfoExtraTemp_min: weatherInfoExtraTemp_min });
        this.setState({ weatherInfoExtraTemp_max: weatherInfoExtraTemp_max });

        console.log("<<< WEATHER TIME STAMP >>>");
        console.log(time_zone);
        this.setState({ weatherTimeStamp: weatherTimeStamp });
        this.setState({ windSpeedInfo: windSpeedInfo });
      })
      .catch((error) => {
        alert(error.message);
      });

    axios
      .request({
        method: "GET",
        url:
          "http://api.openweathermap.org/data/2.5/air_pollution?lat=53.3302&lon=6.3106&appid=d50542e129f589c12a362e67f91906fe",
      })
      .then((response) => {
        const AqiInfo = response.data.list[0].main.aqi;
        console.log("<<< AIR POLLUTION >>>");
        console.log(response.data);
        this.setState({ AqiInfo: AqiInfo });
      })
      .catch((error) => {
        console.error(error);
      });
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col lg="3" md="6" sm="6">
              <Card className="card-stats">
                <CardBody>
                  <Row>
                    <Col md="4" xs="5">
                      <div className="icon-big text-center icon-warning">
                        <i className="fas fa-thunderstorm-sun fa-2x fa-fw"> </i>
                      </div>
                    </Col>
                    <Col md="8" xs="7">
                      <div className="numbers">
                        <p className="card-category">Weather</p>
                        <CardTitle tag="p">
                          {this.state.weatherInfo}&deg;C
                        </CardTitle>
                        <p style={{ opacity: 0.6, fontSize: "small" }}>
                          Minimum - {this.state.weatherInfoExtraTemp_min}
                          &deg;C Maximum - {this.state.weatherInfoExtraTemp_max}
                          &deg;C
                        </p>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
                <CardFooter>
                  <hr />
                  <div className="stats">
                    <i className="fas fa-sync-alt fa-spin fa-1.5x fa-fw"></i>{" "}
                    Updated
                    <p>
                      {this.state.weatherInfo &&
                        moment.unix(this.state.weatherTimeStamp).format("lll")}
                    </p>
                  </div>
                </CardFooter>
              </Card>
            </Col>
            <Col lg="3" md="6" sm="6">
              <Card className="card-stats">
                <CardBody>
                  <Row>
                    <Col md="4" xs="5">
                      <div className="icon-big text-center icon-warning">
                        <i class="fas fa-wind fa-2x fa-fw"></i>
                      </div>
                    </Col>
                    <Col md="8" xs="7">
                      <div className="numbers">
                        <p className="card-category">Air Quality Index</p>
                        <CardTitle tag="p">{this.state.AqiInfo}</CardTitle>
                        <p style={{ opacity: 0.6, fontSize: "small" }}>
                          Wind - {this.state.windSpeedInfo}m/s
                        </p>
                        <p />
                      </div>
                    </Col>
                  </Row>
                </CardBody>
                {/* <<<<<<<<<<<<<< DUMMY PLACEHOLDERS - START>>>>>>>>>>> */}
                <CardFooter>
                  <hr />
                  <div className="stats">
                    <i className="fas fa-sync-alt fa-spin fa-1.5x fa-fw" />{" "}
                    Updated
                    <p>
                      {this.state.weatherInfo &&
                        moment.unix(this.state.weatherTimeStamp).format("lll")}
                    </p>
                  </div>
                </CardFooter>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col md="12">
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">Users Behavior</CardTitle>
                  <p className="card-category">24 Hours performance</p>
                </CardHeader>
                <CardBody>
                  <Line
                    data={dashboard24HoursPerformanceChart.data}
                    options={dashboard24HoursPerformanceChart.options}
                    width={400}
                    height={100}
                  />
                </CardBody>
                <CardFooter>
                  <hr />
                  <div className="stats">
                    <i className="fa fa-history" /> Updated 3 minutes ago
                  </div>
                </CardFooter>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col md="4">
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">Email Statistics</CardTitle>
                  <p className="card-category">Last Campaign Performance</p>
                </CardHeader>
                <CardBody>
                  <Pie
                    data={dashboardEmailStatisticsChart.data}
                    options={dashboardEmailStatisticsChart.options}
                  />
                </CardBody>
                <CardFooter>
                  <div className="legend">
                    <i className="fa fa-circle text-primary" /> Opened{" "}
                    <i className="fa fa-circle text-warning" /> Read{" "}
                    <i className="fa fa-circle text-danger" /> Deleted{" "}
                    <i className="fa fa-circle text-gray" /> Unopened
                  </div>
                  <hr />
                  <div className="stats">
                    <i className="fa fa-calendar" /> Number of emails sent
                  </div>
                </CardFooter>
              </Card>
            </Col>
            <Col md="8">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">NASDAQ: AAPL</CardTitle>
                  <p className="card-category">Line Chart with Points</p>
                </CardHeader>
                <CardBody>
                  <div className="mixed-chart">
                    <Chart
                      options={this.state.options}
                      series={this.state.series}
                      type="bar"
                      height="250"
                    />
                  </div>
                </CardBody>
                <CardFooter>
                  {/* <div className="chart-legend">
                    <i className="fa fa-circle text-info" /> Tesla Model S{" "}
                    <i className="fa fa-circle text-warning" /> BMW 5 Series
                  </div> */}
                  <hr />
                  <div className="card-stats">
                    <i className="fa fa-check" /> Data information certified
                  </div>
                </CardFooter>
                {/* <<<<<<<<<<<<<< DUMMY PLACEHOLDERS - END >>>>>>>>>>> */}
              </Card>
            </Col>
          </Row>
        </div>
      </>
    );
  }
}
export default Dashboard;

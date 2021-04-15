import React from "react";
// react plugin used to create charts
// import { Line, Pie } from "react-chartjs-2";
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
import axios from "axios";
import moment from "moment";

class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      PollutionData: null,
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
      options_temperature: {
        stroke: {
          curve: "smooth",
        },
        chart: {
          id: "basic-bar",
        },
        markers: {
          size: 5,
        },
        colors: ["#0037ff"],
      },
      series_temperature: [],
      options_humidity: {
        stroke: {
          curve: "smooth",
        },
        chart: {
          id: "basic-bar",
        },
        markers: {
          size: 5,
        },
        colors: ["#ff7300"],
      },
      series_population: [],
      options_population: {
        stroke: {
          curve: "smooth",
        },
        chart: {
          id: "basic-bar",
        },
        markers: {
          size: 5,
        },
        colors: ["#ff7300"],
      },
      series_humidity: [],
      graphLoading: false,
    };
  }

  populateTemperatureHumidityCharts(data) {
    let x = Object.keys(data);
    let y = Object.values(data);

    x.shift();
    y.shift();

    let y_temperature = [];
    let y_humidity = [];
    let weatherData = [];

    for (let i = 0; i < y.length; i++) {
      y_temperature.push(y[i].TEMPERATURE);
      y_humidity.push(y[i].HUMIDITY);
      weatherData.push(y[i].WEATHER);
    }

    this.setState({
      options_temperature: {
        xaxis: {
          categories: x,
        },
        annotations: {
          xaxis: [
            {
              x: x[x.length - 1],
            },
          ],
        },
      },
      series_temperature: [
        {
          name: "Temperatures",
          data: y_temperature,
        },
      ],

      options_humidity: {
        xaxis: {
          categories: x,
        },
        annotations: {
          xaxis: [
            {
              x: x[x.length - 1],
            },
          ],
        },
      },
      series_humidity: [
        {
          name: "Humidity",
          data: y_humidity,
        },
      ],

      graphLoading: false,
    });
  }

  populatePopulation(ireland_population, dublin_population) {
    let x = []
    let y_ireland = []
    let y_dublin = []
    let y_ireland_not_dublin = []

    for(let i=0; i<ireland_population.length; i++) {
      x.push(ireland_population[i].year);
      y_ireland.push(ireland_population[i].population);
      y_dublin.push(dublin_population[i].population);
      y_ireland_not_dublin.push(ireland_population[i].population - dublin_population[i].population);
    }

    this.setState({
      options_population: {
        xaxis: {
          categories: x,
        },
        annotations: {
          xaxis: [
            {
              x: x[x.length - 1],
            },
          ],
        }
      },
      series_population: [
        {
          name: "Ireland Population",
          data: y_ireland,
          color: "blue"
        },
        {
          name: "Ireland Population without Dublin",
          data: y_ireland_not_dublin,
          color: "orange"
        },
        {
          name: "Dublin Population",
          data: y_dublin,
          color: "red"
        }
      ],

      graphLoading: false,
    });
  }

  componentDidMount() {
    this.setState({
      graphLoading: true,
    });

    axios
      .request({
        method: "GET",
        url:
          "https://api.openweathermap.org/data/2.5/weather?q=Dublin&units=metric&appid=d50542e129f589c12a362e67f91906fe",
      })
      .then((response) => {
        const weatherInfo = response.data.main.temp;
        const weatherInfoExtraTemp_min = response.data.main.temp_min;
        const weatherInfoExtraTemp_max = response.data.main.temp_max;
        const time_zone = response.data.timezone;
        const weatherTimeStamp = response.data.sys.sunrise - -time_zone;
        const windSpeedInfo = response.data.wind.speed;
        this.setState({ weatherInfo: weatherInfo });
        this.setState({ weatherInfoExtraTemp_min: weatherInfoExtraTemp_min });
        this.setState({ weatherInfoExtraTemp_max: weatherInfoExtraTemp_max });
        this.setState({ weatherTimeStamp: weatherTimeStamp });
        this.setState({ windSpeedInfo: windSpeedInfo });
      })
      .catch((error) => {
        alert(error.message);
      });

    axios
      .request({
        method: "GET",
        url: "/main/weather_forecast/",
      })
      .then((response) => {
        const data = response.data.DATA.RESULT;
        this.populateTemperatureHumidityCharts(data);
        localStorage.setItem("weather_forecast", JSON.stringify(data));
      })
      .catch((err) => {
        if (localStorage.getItem("weather_forecast") != null) {
          const data = JSON.parse(localStorage.getItem("weather_forecast"));
          this.populateTemperatureHumidityCharts(data);
        }
      });

    axios
      .request({
        method: "GET",
        url: "/main/ireland_population/",
      })
      .then((response) => {
        const ireland_population = response.data.DATA.RESULT;

        axios
          .request({
            method: "GET",
            url: "/main/dublin_population/",
          })
          .then((response) => {
            const dublin_population = response.data.DATA.RESULT;
            console.log(dublin_population)
            
            localStorage.setItem("ireland_population", JSON.stringify(ireland_population));
            localStorage.setItem("dublin_population", JSON.stringify(dublin_population));
            this.populatePopulation(ireland_population, dublin_population);
          })
      })
      .catch((err) => {
        console.log(err);
        if (localStorage.getItem("dublin_population") != null) {
          const dublin_population = JSON.parse(localStorage.getItem("dublin_population"));
          const ireland_population = JSON.parse(localStorage.getItem("ireland_population"));
          this.populatePopulation(ireland_population, dublin_population);
        }
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
                          &deg;C <br />
                          Maximum - {this.state.weatherInfoExtraTemp_max}
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

          {/** HISTORICAL - AIR POLLUTION vs POPULATION */}
          {/**LINKS 
          https://data.cso.ie/
          https://www.dublindashboard.ie/themes#environment
          
        */}

          <Row></Row>

          {/** WEATHER STUFF */}

          <Row>
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">
                    Temperature Forecast{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                  </CardTitle>
                  <p className="card-category">14 Days Forecast</p>
                </CardHeader>
                <CardBody>
                  <div className="mixed-chart">
                    <Chart
                      options={this.state.options_temperature}
                      series={this.state.series_temperature}
                      type="line"
                      height="250"
                    />
                  </div>
                </CardBody>
                <CardFooter>
                  <hr />
                  <div className="card-stats">
                    <i className="fa fa-check" /> Data information certified
                  </div>
                </CardFooter>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">
                    Humidity Forecast{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                  </CardTitle>
                  <p className="card-category">14 Days Forecast</p>
                </CardHeader>
                <CardBody>
                  <div className="mixed-chart">
                    <Chart
                      options={this.state.options_humidity}
                      series={this.state.series_humidity}
                      type="line"
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
              </Card>
            </Col>
          </Row>

          {/**WEATHER STUFF END */}

          <Row>
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">
                    Population Correlation{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                  </CardTitle>
                </CardHeader>
                <CardBody>
                  <div className="mixed-chart">
                    <Chart
                      options={this.state.options_population}
                      series={this.state.series_population}
                      type="line"
                      height="600"
                    />
                  </div>
                </CardBody>
                <CardFooter>
                  <hr />
                  <div className="card-stats">
                    <i className="fa fa-check" /> Data information certified
                  </div>
                </CardFooter>
              </Card>
            </Col>
          </Row>
        </div>
      </>
    );
  }
}
export default Dashboard;

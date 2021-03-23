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
import axios from "axios";
// react plugin used to create google maps
import Chart from "react-apexcharts";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { AntPath } from 'leaflet-ant-path';
// reactstrap components
import {
  Card,
  CardTitle,
  CardFooter,
  CardHeader,
  CardBody,
  Row,
  Col,
  FormGroup,
  Label,
  Input,
} from "reactstrap";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const iconDefault = L.divIcon({
  className: "custom-pin",
  iconAnchor: [0, 24],
  labelAnchor: [-6, 0],
  popupAnchor: [0, -36],
  html: `<i class="fa fa-map-marker-alt fa-3x" style="color:blue;"></i>`,
});

L.Marker.prototype.options.icon = iconDefault;

class Buses extends React.Component {
  setBusesGraph(x, y) {
    console.log(x, y);
    this.setState({
      options: {
        xaxis: {
          categories: x,
        },
        annotations: {
          xaxis: [
            {
              x: x[x.length - 1],
              borderColor: "#00E396",
              label: {
                borderColor: "#00E396",
                orientation: "horizontal",
                text: "Prediction",
              },
            },
          ],
        },
      },
      series: [
        {
          name: "Buses in use",
          data: y,
        },
      ],
      graphLoading: false,
    });
  }

  drawPathBetweenBusStops(startStop, destinationStop) {
    // const start = [53.344, -6.233];
    // const destination = [53.342, -6.236];

    const map = this.state.map;

    // Retrieve start & destination stops coordinates
    let start = null;
    let destination = null;
    for (const busStop of this.state.busStops) {
      if (busStop.stop == startStop) {
        start = [busStop.lat, busStop.lng];
      } else if (busStop.stop == destinationStop) {
        destination = [busStop.lat, busStop.lng];
      }

      if (start && destination) break;
    }

    const apiKey = '5b3ce3597851110001cf62489c45fd4df8464534ba7a6bab835d5cc8';

    axios
      .get(`https://api.openrouteservice.org/v2/directions/driving-hgv?api_key=${apiKey}&start=${start.reverse().join(',')}&end=${destination.reverse().join(',')}`)
      .then(res => {
        let latlngs = [];
        latlngs.push(start.reverse());
        for (const c of res.data.features[0].geometry.coordinates) {
          latlngs.push(c.reverse());
        }
        latlngs.push(destination.reverse());

        const options = {
          "delay": 400,
          "dashArray": [
            10,
            20
          ],
          "weight": 5,
          "color": "#0000FF",
          "pulseColor": "#FFFFFF",
          "paused": false,
          "reverse": false,
          "hardwareAccelerated": true
        };

        const antPolyline = new AntPath(latlngs, options);
        antPolyline.addTo(map);
      })
      .catch(err => {
        console.log(err);
      });
  }

  drawPathBetweenBusStopsId(startStop, destinationStop) {
    // const start = [53.344, -6.233];
    // const destination = [53.342, -6.236];

    const map = this.state.map;

    // Retrieve start & destination stops coordinates
    let start = null;
    let destination = null;
    for (const busStop of this.state.busStops) {
      if (busStop.stop_id == startStop) {
        start = [busStop.lat, busStop.lng];
      } else if (busStop.stop_id == destinationStop) {
        destination = [busStop.lat, busStop.lng];
      }

      if (start && destination) break;
    }

    const apiKey = '5b3ce3597851110001cf62489c45fd4df8464534ba7a6bab835d5cc8';

    axios
      .get(`https://api.openrouteservice.org/v2/directions/driving-hgv?api_key=${apiKey}&start=${start.reverse().join(',')}&end=${destination.reverse().join(',')}`)
      .then(res => {
        let latlngs = [];
        latlngs.push(start.reverse());
        for (const c of res.data.features[0].geometry.coordinates) {
          latlngs.push(c.reverse());
        }
        latlngs.push(destination.reverse());

        const options = {
          "delay": 400,
          "dashArray": [
            10,
            20
          ],
          "weight": 5,
          "color": "#0000FF",
          "pulseColor": "#FFFFFF",
          "paused": false,
          "reverse": false,
          "hardwareAccelerated": true
        };

        const antPolyline = new AntPath(latlngs, options);
        antPolyline.addTo(map);
      })
      .catch(err => {
        console.log(err);
      });
  }

  populateBusStops() {
    axios
      .get('http://127.0.0.1:8000/main/busstop_locations/')
      .then(res => {
        let busStops_tmp = [];
        let busStops_list = [];
        let counter = 0;
        for (const stop of Object.keys(res.data.DATA.RESULT)) {
          //if (counter++ > 800) break;
          if (busStops_tmp.includes(res.data.DATA.RESULT[stop].STOP_ID) == false) {
            busStops_tmp.push(res.data.DATA.RESULT[stop].STOP_ID);
            busStops_list.push({
              stop: stop,
              stop_id: res.data.DATA.RESULT[stop].STOP_ID,
              name: res.data.DATA.RESULT[stop].STOP_NAME,
              lat: res.data.DATA.RESULT[stop].STOP_LAT,
              lng: res.data.DATA.RESULT[stop].STOP_LON,
              icon: iconDefault,
              });
           }
        }
        this.setState({ busStops: busStops_list });

        // this.drawPathBetweenBusStops("stop_76", "stop_85");
        this.populateTrips();
      })
      .catch(error => {
        console.error(error);
      });
  }

  drawPathForTrip(index) {
    console.log(this.state.busTrips)
    let trip = this.state.busTrips[index];
    let stops_list = trip.stops_list;

    for(let i=0; i<stops_list.length-1; i++) {
      console.log(stops_list[i].stop_id)
      console.log(stops_list[i+1].stop_id)
      this.drawPathBetweenBusStopsId(stops_list[i].stop_id, stops_list[i+1].stop_id);
    }

  }

  populateTrips(){
    axios
      .get('http://127.0.0.1:8000/main/busstop_timings/')
      .then(res => {
        let trips_list = [];
        for (const trip of Object.keys(res.data.DATA.RESULT)) {
          trips_list.push({
            trip: trip,
            trip_id: res.data.DATA.RESULT[trip].TRIP_ID,
            route_id: res.data.DATA.RESULT[trip].ROUTE_ID,
            stops_list: res.data.DATA.RESULT[trip].STOP_INFO,
            icon: iconDefault,
            });
        }
        
        this.setState({ busTrips: trips_list });
        for(let i=0; i<this.state.busTrips.length; i++) {
          this.drawPathForTrip(i);
        }
      })
      .catch(error => {
        console.error(error);
      });
  }

  componentDidMount() {
    this.populateBusStops();
  }

  constructor(props) {
    super(props);

    this.state = {
      map: null,
      markers: [],
      busStops: [],
      busTrips: [],
      options: {
        chart: {
          id: "basic-bar",
        },
      },
      series: [],
      busSelection: "ALL",
      graphLoading: true,
    };

    this.mapCreated = this.mapCreated.bind(this);
    this.drawPathBetweenBusStops = this.drawPathBetweenBusStops.bind(this);
  }

  onChangeBusSelection(e) {
    alert(`Bus changed to ${e}`);
  }

  /**
   * Triggered when the map is created; currently creates path between two points for test purposes
   * 
   * References:
   * https://openrouteservice.org/
   * https://rubenspgcavalcante.github.io/leaflet-ant-path/​​​​​​​
   * 
   * @param {*} map 
   */
  mapCreated(map) {
    this.setState({ map: map });
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col md="12">
              <Card>
                <CardHeader>Buses Availability</CardHeader>
                <CardBody>
                  <div className="leaflet-container">
                    <MapContainer
                      whenCreated={this.mapCreated}
                      style={{ width: "100%", height: "600px" }}
                      center={[53.345, -6.26]}
                      zoom={13}
                      scrollWheelZoom={false}
                    >
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {this.state.busStops.map(
                        ({ stop, name, lat, lng, icon }, idx) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={[lat, lng]}
                            icon={icon}
                          >
                            <Popup>
                              <p>
                                <b>{name}</b><br />
                                {/* <i>{stop}</i> */}
                              </p>
                            </Popup>
                          </Marker>
                        )
                      )}
                    </MapContainer>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">
                    Buses Usage{" "}
                    <i
                      style={{
                        display: this.state.graphLoading
                          ? "inline-block"
                          : "none",
                      }}
                      className="fas fa-sync-alt fa-spin fa-1x fa-fw"
                    ></i>
                  </CardTitle>
                  <p className="card-category">
                    Evolution of Buses usage over time
                  </p>
                </CardHeader>
                <CardBody>
                  <FormGroup row>
                    <Col sm={12} md={4}>
                      <Label>Bus [idk] selection</Label>
                      <Input
                        type="select"
                        name="select"
                        onChange={this.onChangeBusSelection}
                        value={this.state.busSelection}
                      >
                        <option>ALL</option>
                        {this.state.markers.map(
                          ({ position, content }, index) => (
                            <option key={index}>{content}</option>
                          )
                        )}
                      </Input>
                    </Col>
                  </FormGroup>

                  <div className="mixed-chart">
                    <Chart
                      options={this.state.options}
                      series={this.state.series}
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
        </div>
      </>
    );
  }
}

export default Buses;

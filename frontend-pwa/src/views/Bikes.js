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
// react plugin used to create google maps
import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  Marker,
} from "react-google-maps";
import Chart from "react-apexcharts";
// reactstrap components
import { Card, CardTitle, CardFooter, CardHeader, CardBody, Row, Col } from "reactstrap";

const MapWrapper = withScriptjs(
  withGoogleMap((props) => (
    <GoogleMap
      defaultZoom={13}
      defaultCenter={{ lat: 40.748817, lng: -73.985428 }}
      defaultOptions={{
        scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
        styles: [
          {
            featureType: "water",
            stylers: [
              {
                saturation: 43,
              },
              {
                lightness: -11,
              },
              {
                hue: "#0088ff",
              },
            ],
          },
          {
            featureType: "road",
            elementType: "geometry.fill",
            stylers: [
              {
                hue: "#ff0000",
              },
              {
                saturation: -100,
              },
              {
                lightness: 99,
              },
            ],
          },
          {
            featureType: "road",
            elementType: "geometry.stroke",
            stylers: [
              {
                color: "#808080",
              },
              {
                lightness: 54,
              },
            ],
          },
          {
            featureType: "landscape.man_made",
            elementType: "geometry.fill",
            stylers: [
              {
                color: "#ece2d9",
              },
            ],
          },
          {
            featureType: "poi.park",
            elementType: "geometry.fill",
            stylers: [
              {
                color: "#ccdca1",
              },
            ],
          },
          {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [
              {
                color: "#767676",
              },
            ],
          },
          {
            featureType: "road",
            elementType: "labels.text.stroke",
            stylers: [
              {
                color: "#ffffff",
              },
            ],
          },
          {
            featureType: "poi",
            stylers: [
              {
                visibility: "off",
              },
            ],
          },
          {
            featureType: "landscape.natural",
            elementType: "geometry.fill",
            stylers: [
              {
                visibility: "on",
              },
              {
                color: "#b8cb93",
              },
            ],
          },
          {
            featureType: "poi.park",
            stylers: [
              {
                visibility: "on",
              },
            ],
          },
          {
            featureType: "poi.sports_complex",
            stylers: [
              {
                visibility: "on",
              },
            ],
          },
          {
            featureType: "poi.medical",
            stylers: [
              {
                visibility: "on",
              },
            ],
          },
          {
            featureType: "poi.business",
            stylers: [
              {
                visibility: "simplified",
              },
            ],
          },
        ],
      }}
    >
      <Marker position={{ lat: 40.748817, lng: -73.985428 }} />
    </GoogleMap>
  ))
);

class Bikes extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      options: {
        chart: {
          id: "basic-bar"
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
        }
      },
      series: [
        {
          name: "series-1",
          data: [30, 40, 45, 50, 49, 60, 70, 91]
        }
      ]
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col md="12">
              <Card>
                <CardHeader>Google Maps</CardHeader>
                <CardBody>
                  <div
                    id="map"
                    className="map"
                    style={{ position: "relative", overflow: "hidden" }}
                  >
                    <MapWrapper
                      googleMapURL="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY_HERE"
                      loadingElement={<div style={{ height: `100%` }} />}
                      containerElement={<div style={{ height: `100%` }} />}
                      mapElement={<div style={{ height: `100%` }} />}
                    />
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col md="12">
              <Card className="card-chart">
                <CardHeader>
                  <CardTitle tag="h5">Bikes Usage</CardTitle>
                  <p className="card-category">Evolution of bikes usage over time</p>
                </CardHeader>
                <CardBody>
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

export default Bikes;

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
  Table,
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

class Parkings extends React.Component {
  setParkingMarkers(parkings_coordinates_dictionary) {
    let { markers } = this.state;

    axios
      .get("http://127.0.0.1:8000/main/parkings_availability/")
      .then(async (res) => {
        let parkings_avaliabilities = res.data.DATA.RESULT[0].parkings;
        console.log(parkings_avaliabilities);

        for (let i = 0; i < parkings_avaliabilities.length; i++) {
          let parking_name = parkings_avaliabilities[i].name;

          // Add markers
          markers.push({
            name: parking_name,
            area: parkings_coordinates_dictionary[parking_name].area,
            position: [
              parkings_coordinates_dictionary[parking_name].lat,
              parkings_coordinates_dictionary[parking_name].lng,
            ],
            availableSpaces: parkings_avaliabilities[i].availableSpaces,
            icon: {
              className: "custom-pin",
              iconAnchor: [0, 24],
              labelAnchor: [-6, 0],
              popupAnchor: [0, -36],
              html: `<i class="fas fa-parking fa-3x" style="color:blue;"></i>`,
            },
          });
        }

        console.log(markers);
        this.setState({ markers });
      })
      .catch((err) => {
        console.log(err);
      });
  }

  getParkingCoordinatesAndSetMarkers() {
    axios
      .get("http://127.0.0.1:8000/main/parkings_locations/")
      .then(async (res) => {
        const parkings_coordinates = res.data.DATA.RESULT;

        let parkings_coordinates_dictionary = {};

        for (let i = 0; i < parkings_coordinates.length; i++) {
          parkings_coordinates_dictionary[parkings_coordinates[i]["name"]] = {
            area: parkings_coordinates[i]["area"],
            lat: parkings_coordinates[i]["lat"],
            lng: parkings_coordinates[i]["lng"],
          };
        }

        this.setParkingMarkers(parkings_coordinates_dictionary);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  componentDidMount() {
    this.getParkingCoordinatesAndSetMarkers();
    // localStorage.setItem("parkings_availability", JSON.stringify(markers));
    // })
    // .catch((err) => {
    //   console.log(err);
    //   if (localStorage.getItem("parkings_availability") != null) {
    //     const markers = JSON.parse(
    //       localStorage.getItem("parkings_availability")
    //     );
    //     this.setState({ markers });
    //   }
    // });
  }

  constructor(props) {
    super(props);

    this.state = {
      markers: [],
    };
  }

  render() {
    return (
      <>
        <div className="content">
          <Row>
            <Col>
              <Card>
                <CardHeader>
                  <CardTitle tag="h5">Parkings Availability</CardTitle>
                </CardHeader>
                <CardBody>
                  <div className="leaflet-container">
                    <MapContainer
                      style={{ width: "100%", height: "600px" }}
                      center={[53.345, -6.26]}
                      zoom={15}
                      scrollWheelZoom={false}
                    >
                      <TileLayer
                        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {this.state.markers.map(
                        (
                          { position, name, availableSpaces, area, icon },
                          idx
                        ) => (
                          <Marker
                            key={`marker-${idx}`}
                            position={position}
                            icon={L.divIcon(icon)}
                          >
                            <Popup>
                              <p>
                                <b>{name}</b>
                              </p>
                              <p>{"Area: " + area}</p>
                              <p>{"Available Spaces: " + availableSpaces}</p>
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
        </div>
      </>
    );
  }
}

export default Parkings;

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
  getParkingCoordinates() {
    try {
      // const res = await axios.get(
      //   "http://127.0.0.1:8000/main/bikestands_details/?type=live"
      // );
      // const bikeStationsLive = res.data.DATA.RESULT;
      // return bikeStationsLive;
      let parkings_coordinates = [
        {
          name: "PARNELL",
          area: "Northwest",
          lat: 53.35081,
          lng: -6.26831,
        },
        {
          name: "ILAC",
          area: "Northwest",
          lat: 53.34861,
          lng: -6.26884,
        },
        {
          name: "JERVIS",
          area: "Northwest",
          lat: 53.34878,
          lng: -6.26667,
        },
        {
          name: "ARNOTTS",
          area: "Northwest",
          lat: 53.34908,
          lng: -6.26006,
        },
        {
          name: "MARLBORO",
          area: "Northeast",
          lat: 53.352600098081375,
          lng: -6.258366086014968,
        },
        {
          name: "ABBEY",
          area: "Northeast",
          lat: 53.35024325062157,
          lng: -6.254233328658077,
        },
        {
          name: "THOMASST",
          area: "Southwest",
          lat: 53.34381779026483,
          lng: -6.2802188590302395,
        },
        {
          name: "C/CHURCH",
          area: "Southwest",
          lat: 53.3433754859322,
          lng: -6.269683162040512,
        },
        {
          name: "SETANTA",
          area: "Southeast",
          lat: 53.342046862254755,
          lng: -6.256021086015311,
        },
        {
          name: "DAWSON",
          area: "Southeast",
          lat: 53.340471400850085,
          lng: -6.256018776761035,
        },
        {
          name: "TRINITY",
          area: "Southeast",
          lat: 53.34416060960417,
          lng: -6.262745776634299,
        },
        {
          name: "GREENRCS",
          area: "Southeast",
          lat: 53.342438538176374,
          lng: -6.263818974717609,
        },
        {
          name: "DRURY",
          area: "Southeast",
          lat: 53.342987236356,
          lng: -6.2631027690892935,
        },
        {
          name: "B/THOMAS",
          area: "Southeast",
          lat: 53.34268459927202,
          lng: -6.261434643686948,
        },
      ];

      let parkings_coordinates_dictionary = {};

      for (let i = 0; i < parkings_coordinates.length; i++) {
        parkings_coordinates_dictionary[parkings_coordinates[i]["name"]] = {
          area: parkings_coordinates[i]["area"],
          lat: parkings_coordinates[i]["lat"],
          lng: parkings_coordinates[i]["lng"],
        };
      }

      return parkings_coordinates_dictionary;
    } catch (e) {
      console.log(e);
    }
  }

  componentDidMount() {
    // axios
    //   .get("http://127.0.0.1:8000/main/bikestands_details/?type=locations")
    //   .then(async (res) => {

    let { markers } = this.state;

    // const bikeStations = res.data.DATA.RESULT;
    const result = {
      updateTimestamp: "2021-03-22 10:12:53",
      parkings: [
        {
          name: "PARNELL",
          area: "Northwest",
          availableSpaces: 338,
        },
        {
          name: "ILAC",
          area: "Northwest",
          availableSpaces: 12,
        },
        {
          name: "THOMASST",
          area: "Southwest",
          availableSpaces: 256,
        },
        {
          name: "DAWSON",
          area: "Southeast",
          availableSpaces: null, // May happen if no recent data from the API; just put "No data" in the front-end display?
        },
      ],
    };

    const parkings_avaliabilities = result.parkings;
    const parkings_coordinates = this.getParkingCoordinates();
    console.log(parkings_coordinates["PARNELL"]);

    for (let i = 0; i < parkings_avaliabilities.length; i++) {
      let parking_name = parkings_avaliabilities[i].name;

      // Add markers
      markers.push({
        name: parking_name,
        area: parkings_coordinates[parking_name].area,
        position: [
          parkings_coordinates[parking_name].lat,
          parkings_coordinates[parking_name].lng,
        ],
        availableSpaces: parkings_avaliabilities[i].availableSpaces,
        icon: {
          className: "custom-pin",
          iconAnchor: [0, 24],
          labelAnchor: [-6, 0],
          popupAnchor: [0, -36],
          html: `<i class="fa fa-map-marker-alt fa-3x" style="color:red;"></i>`,
        },
      });
    }

    console.log(markers);
    this.setState({ markers });
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
                      zoom={13}
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

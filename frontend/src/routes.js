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
import Dashboard from "views/Dashboard.js";
// import Notifications from "views/Notifications.js";
import Icons from "views/Icons.js";
// import Typography from "views/Typography.js";
// import TableList from "views/Tables.js";
// import Maps from "views/Map.js";
// import UserPage from "views/User.js";
// import UpgradeToPro from "views/Upgrade.js";

var routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "fas fa-university",
    component: Dashboard,
    layout: "/admin",
  },
  {
    path: "/bikes",
    name: "Bikes",
    icon: "fas fa-bicycle",
    component: Icons,
    layout: "/admin",
  },
  {
    path: "/buses",
    name: "Buses",
    icon: "fas fa-bus-alt",
    component: Icons,
    layout: "/admin",
  },
  {
    path: "/traffic",
    name: "Traffic",
    icon: "fas fa-traffic-light",
    component: Icons,
    layout: "/admin",
  },
  {
    path: "/bins",
    name: "Public bins",
    icon: "fas fa-dumpster",
    component: Icons,
    layout: "/admin",
  },
  {
    path: "/parkings",
    name: "Parkings",
    icon: "fas fa-parking",
    component: Icons,
    layout: "/admin",
  },
  {
    path: "/emergency",
    name: "Emergency Services",
    icon: "fas fa-ambulance",
    component: Icons,
    layout: "/admin",
  },
  {
    path: "/footfalls",
    name: "Footfalls",
    icon: "fas fa-shoe-prints",
    component: Icons,
    layout: "/admin",
  },
  // {
  //   path: "/icons",
  //   name: "Icons",
  //   icon: "nc-icon nc-diamond",
  //   component: Icons,
  //   layout: "/admin",
  // },
  // {
  //   path: "/maps",
  //   name: "Maps",
  //   icon: "nc-icon nc-pin-3",
  //   component: Maps,
  //   layout: "/admin",
  // },
  // {
  //   path: "/notifications",
  //   name: "Notifications",
  //   icon: "nc-icon nc-bell-55",
  //   component: Notifications,
  //   layout: "/admin",
  // },
  // {
  //   path: "/user-page",
  //   name: "User Profile",
  //   icon: "nc-icon nc-single-02",
  //   component: UserPage,
  //   layout: "/admin",
  // },
  // {
  //   path: "/tables",
  //   name: "Table List",
  //   icon: "nc-icon nc-tile-56",
  //   component: TableList,
  //   layout: "/admin",
  // },
  // {
  //   path: "/typography",
  //   name: "Typography",
  //   icon: "nc-icon nc-caps-small",
  //   component: Typography,
  //   layout: "/admin",
  // },
];
export default routes;

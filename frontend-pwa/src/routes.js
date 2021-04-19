import Dashboard from "views/Dashboard.js";
import Bikes from "views/Bikes.js";
import Buses from "views/Buses.js";
import Parkings from "views/Parkings";
import Footfall from "views/Footfall";
import EmergencyServices from "views/EmergencyServices";

var routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "fas fa-university",
    component: Dashboard,
    layout: "/admin",
    requiresAuth: false,
  },
  {
    path: "/bikes",
    name: "Bikes",
    icon: "fas fa-bicycle",
    component: Bikes,
    layout: "/admin",
    requiresAuth: true,
  },
  {
    path: "/buses",
    name: "Buses",
    icon: "fas fa-bus-alt",
    component: Buses,
    layout: "/admin",
    requiresAuth: true,
  },
  {
    path: "/parkings",
    name: "Parkings",
    icon: "fas fa-parking",
    component: Parkings,
    layout: "/admin",
    requiresAuth: true,
  },
  {
    path: "/emergency",
    name: "Emergency Services",
    icon: "fas fa-ambulance",
    component: EmergencyServices,
    layout: "/admin",
    requiresAuth: true,
  },
  {
    path: "/footfalls",
    name: "Footfalls",
    icon: "fas fa-shoe-prints",
    component: Footfall,
    layout: "/admin",
    requiresAuth: true,
  },
];
export default routes;

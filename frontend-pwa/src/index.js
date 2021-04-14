import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import * as serviceWorkerRegistration from "./serviceWorkerRegistration";
import reportWebVitals from "./reportWebVitals";

import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/paper-dashboard.scss?v=1.2.0";
import "assets/demo/demo.css";
import "perfect-scrollbar/css/perfect-scrollbar.css";

import AdminLayout from "layouts/Admin.js";
import { Auth0Provider } from "@auth0/auth0-react";
import axios from "axios";

axios.defaults.baseURL = process.env.REACT_APP_API_URL;
const auth0redirectUri = process.env.REACT_APP_URL + "/admin/dashboard";

const hist = createBrowserHistory();

ReactDOM.render(
  <React.StrictMode>
    <Auth0Provider
      domain={process.env.REACT_APP_AUTH0_DOMAIN}
      clientId={process.env.REACT_APP_AUTH0_CLIENT_ID}
      // redirectUri={window.location.origin + "/admin/login"}
      redirectUri={auth0redirectUri}
    >
      <Router history={hist}>
        <Switch>
          <Route exact path="/">
            <Redirect to="/admin/dashboard" />
          </Route>
          <Route path="/admin" render={(props) => <AdminLayout {...props} />} />
        </Switch>
      </Router>
    </Auth0Provider>
  </React.StrictMode>,
  document.getElementById("root")
);

serviceWorkerRegistration.register();
reportWebVitals();

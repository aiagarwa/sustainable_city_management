import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from './reportWebVitals';


import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/paper-dashboard.scss?v=1.2.0";
import "assets/demo/demo.css";
import "perfect-scrollbar/css/perfect-scrollbar.css";

import AdminLayout from "layouts/Admin.js";
import { Auth0Provider } from "@auth0/auth0-react";

const hist = createBrowserHistory();

ReactDOM.render(
  <React.StrictMode>
    <Auth0Provider
      domain={process.env.REACT_APP_AUTH0_DOMAIN}
      clientId={process.env.REACT_APP_AUTH0_CLIENT_ID}
      // redirectUri={window.location.origin + "/admin/login"}
      redirectUri="http://localhost:3000/admin/login"
    >
      <Router history={hist}>
        <Switch>
          <Route path="/admin" render={(props) => <AdminLayout {...props} />} />
        </Switch>
      </Router>
    </Auth0Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorkerRegistration.register();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();


// ReactDOM.render(
//     <Router history={hist}>
//       <Switch>
//         <Route path="/admin" render={(props) => <AdminLayout {...props} />} />
//         <Redirect to="/admin/dashboard" />
//       </Switch>
//     </Router>,
//   document.getElementById("root")
// );

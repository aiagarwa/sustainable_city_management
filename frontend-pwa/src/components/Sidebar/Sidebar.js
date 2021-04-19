import React from "react";
import { NavLink } from "react-router-dom";
import { Nav } from "reactstrap";
// javascript plugin used to create scrollbars on windows
import PerfectScrollbar from "perfect-scrollbar";

import logo from "logo.svg";
import { withAuth0 } from "@auth0/auth0-react";

var ps;

class Sidebar extends React.Component {
  constructor(props) {
    super(props);
    this.activeRoute.bind(this);
    this.sidebar = React.createRef();
  }
  // verifies if routeName is the one active (in browser input)
  activeRoute(routeName) {
    return this.props.location.pathname.indexOf(routeName) > -1 ? "active" : "";
  }
  componentDidMount() {
    if (navigator.platform.indexOf("Win") > -1) {
      ps = new PerfectScrollbar(this.sidebar.current, {
        suppressScrollX: true,
        suppressScrollY: false,
      });
    }
  }
  componentWillUnmount() {
    if (navigator.platform.indexOf("Win") > -1) {
      ps.destroy();
    }
  }
  render() {
    const {
      isLoading,
      isAuthenticated,
      loginWithRedirect,
      logout,
    } = this.props.auth0;

    let logInOutButton;
    if (isAuthenticated) {
      logInOutButton = (
        <li>
          <a
            href
            onClick={() => logout()}
            className="nav-link"
            activeClassName="active"
          >
            <i className="fas fa-user-slash" />
            <p>Logout</p>
          </a>
        </li>
      );
    } else {
      logInOutButton = (
        <li>
          <a
            href
            onClick={() => loginWithRedirect()}
            className="nav-link"
            activeClassName="active"
          >
            <i className="fas fa-user-tie" />
            <p>Login</p>
          </a>
        </li>
      );
    }

    let nav = (
      <Nav>
        <li>
          <a href className="nav-link">
            Loading...
          </a>
        </li>
      </Nav>
    );
    if (!isLoading) {
      nav = (
        <Nav>
          {logInOutButton}
          {this.props.routes.map((prop, key) => {
            if (prop.requiresAuth && !isAuthenticated) return;

            return (
              <li
                className={
                  this.activeRoute(prop.path) + (prop.pro ? " active-pro" : "")
                }
                key={key}
              >
                <NavLink
                  to={prop.layout + prop.path}
                  className="nav-link"
                  activeClassName="active"
                >
                  <i className={prop.icon} />
                  <p>{prop.name}</p>
                </NavLink>
              </li>
            );
          })}
        </Nav>
      );
    }

    return (
      <div
        className="sidebar"
        data-color={this.props.bgColor}
        data-active-color={this.props.activeColor}
      >
        <div className="logo">
          <a href="/" className="simple-text logo-mini">
            <div className="logo-img">
              <img src={logo} alt="react-logo" />
            </div>
          </a>
          <a href="/" className="simple-text logo-normal">
            City Manager
          </a>
        </div>
        <div className="sidebar-wrapper" ref={this.sidebar}>
          {nav}
        </div>
      </div>
    );
  }
}

export default withAuth0(Sidebar);

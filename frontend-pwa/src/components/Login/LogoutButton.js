import React, { Component } from "react";
import { withAuth0 } from "@auth0/auth0-react";
import "./LogoutButton.css";

class LogoutButton extends Component {
  render() {
    const { logout, isAuthenticated } = this.props.auth0;

    return isAuthenticated && <button onClick={() => logout()}>Log Out</button>;
  }
}

export default withAuth0(LogoutButton);
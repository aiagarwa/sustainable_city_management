import React from "react";
import LoginButton from "../components/Login/LoginButton";
import LogoutButton from "../components/Login/LogoutButton";
import Profile from "../components/Login/Profile";
// reactstrap components
import { Row } from "reactstrap";

class Login extends React.Component {
  render() {
    return (
      <>
        <div className="content">
          <Row>
            <LoginButton />
            <LogoutButton />
            <Profile />
          </Row>
        </div>
      </>
    );
  }
}

export default Login;

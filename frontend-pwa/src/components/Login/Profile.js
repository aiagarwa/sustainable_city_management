import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import JSONPretty from "react-json-pretty";
import "./Profile.css";

const Profile = () => {
  const { user, isAuthenticated } = useAuth0();
  console.log(user);

  return (
    isAuthenticated && (
      <div className="profile">
        {/* <img src={user.picture} alt={user.name} /> */}
        <h2>{user.name}</h2>
        <p>{user.email}</p>
        <JSONPretty data={user} />
        {/* {JSON.stringify(user, null, 2)} */}
      </div>
    )
  );
};

export default Profile;

//ATTENTION !!!! Private Key - Do not Share (Delete before Deployed)
// 010DKQZ4Q172VKHXR7ZSD58L2FC101

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchProfile } from "../api/auth";
import { getAccessToken, clearTokens } from "../utils/token";

interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  address: string;
  age: number;
  birthday: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      navigate("/login");
      return;
    }
    fetchProfile(token)
      .then(setProfile)
      .catch(() => navigate("/login"));
  }, [navigate]);
  const handleLogout = () => {
    clearTokens();
    navigate("/login");
  };
  if (!profile) return <p>Loading...</p>;
  return (
    <div style={{ maxWidth: 600, margin: "auto", paddingTop: 40 }}>
      <h2>Welcome, {profile.first_name || profile.username}!</h2>
      <button onClick={handleLogout}>Logout</button>
      <hr />
      <h3>Profile Details</h3>
      <table>
        <tbody>
          <tr><td><b>Name</b></td><td>{profile.first_name} {profile.last_name}</td></tr>
          <tr><td><b>Email</b></td><td>{profile.email}</td></tr>
          <tr><td><b>Address</b></td><td>{profile.address}</td></tr>
          <tr><td><b>Age</b></td><td>{profile.age}</td></tr>
          <tr><td><b>Birthday</b></td><td>{profile.birthday}</td></tr>
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
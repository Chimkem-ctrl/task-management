import { Navigate } from "react-router-dom";
import { getAccessToken } from "../utils/token";

const ProtectedRoute = ({ children }: { children: any }) => {
  const token = getAccessToken();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
import { Outlet, Navigate } from "react-router-dom";
import { useSelector } from "react-redux"

const PrivateRoutes = () => {
    let auth = useSelector(state => state.auth) // fix to authenticate

    return(
        auth.token ? <Outlet /> : <Navigate to="/login" />
    )
}

export default PrivateRoutes
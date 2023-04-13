import {useAuth0} from "@auth0/auth0-react";

export default function Navbar() {
  const { isAuthenticated, user, loginWithRedirect, logout } = useAuth0();

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light border-bottom">
      <div className="container">
        <a className="navbar-brand" href="/">
          Eddie's Blog
        </a>
          {isAuthenticated ? (
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <button
                  className="nav-link btn"
                  onClick={() =>
                    logout({
                      logoutParams: {
                        returnTo: typeof window != "undefined" && location.origin,
                      },
                    })
                  }
                >
                  {user && user.name ? user.name + " |" : ""} Logout
                </button>
              </li>
            </ul>
          ) : (
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <button className="nav-link btn" onClick={() => loginWithRedirect()}>
                  Login
                </button>
              </li>
            </ul>
          )}
        </div>
    </nav>
  );
}

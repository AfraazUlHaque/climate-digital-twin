import ThemeToggle from "./ThemeToggle";

export default function Navbar() {

    return (

        <header className="navbar">

            <div>

                <h2>

                    AI Climate Digital Twin

                </h2>

                <p>

                    Kerala • Tamil Nadu • Weighted GNN

                </p>

            </div>

            <div className="navbar-right">

                <ThemeToggle />

            </div>

        </header>

    );

}
import React from 'react';
import axios from 'axios';
import Login from './components/Login/Login';
import Header from './components/Header';
import DisplayEventVenueData from './components/Data/DisplayEventVenueData';


class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isLoggedIn: false,
			userProfile: null,
		};
	}

	componentDidMount() {
		// check if user is logged in and set state accordingly
		const isLoggedIn = localStorage.getItem('isLoggedIn');
		this.setState({ isLoggedIn });

		if (isLoggedIn) {
			this.fetchUserProfile();
		}
	}

	fetchUserProfile() {
		axios.get('/user-profile')
			.then(response => {
				this.setState({ userProfile: response.data });
			})
			.catch(error => {
				console.error('Error fetching user profile:', error);
			});
	};


	render() {
		return (
			<div>
				{/* since this is technically index/home page */}
				<div style={{ textAlign: 'center' }}>
					<Header />
					begin by logging in to spotify :D<br></br>
					<Login /><br></br><br></br>

					<DisplayEventVenueData />
				</div>
				{/* if /login/ begin PKCE flow */}
			</div>
		)
	}

}

export default App;

import React from 'react';
import axios from 'axios';
// import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      events: [],
      venues: []
    };
  }

  fetchData(endpoint) {
    axios.get(`http://localhost:8000${endpoint}`)
      .then(res => {
        const data = res.data;
        console.log(endpoint, "data:", data);
        this.setState({
          [endpoint.slice(1, -1)]: data
        });
      })
      .catch(err => {
        console.log(err);
      });
  }

  componentDidMount() {
    this.fetchData('/events/');
    this.fetchData('/venues/');
  }


  render() {
    if (!this.state.events || !this.state.venues) {
      return <div>Loading...</div>;
    }
    
    return (
      <div>
        <h1 style={{ textAlign: 'center' }}>Event Data Generated From Django</h1>
        <div style={{ display: 'flex', margin: '10px' }}>
          <div style={{ flex: 1 }}>
            {this.state.events && this.state.events.map(event => (
              // Render each event
              <div key={event.id}>
                <hr></hr>
                <img src={event.image} style={{maxWidth: "50%"}} alt=''></img>
                <h2>{event.name}</h2>
                <p>{event.event_id}</p>
                <p>{event.price}</p>
                <p>{event.summary}</p>
                <a href={event.tickets_url}>tickets</a>
              </div>
            ))}
          </div>
          <div style={{ flex: 1 }}>
            {this.state.venues && this.state.venues.map(venue => (
              <div key={venue.id}>
                <hr></hr>
                <h2>{venue.name}</h2>
                <p>{venue.venue_id}</p>
                <p>{venue.address}</p>
                <p>{venue.summary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

}

export default App;

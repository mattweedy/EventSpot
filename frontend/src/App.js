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
        const data = res.data.results;
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
    let e_data;
    let v_data;
    e_data = this.fetchData('/events/');
    v_data = this.fetchData('/venues/');
  }


  render() {
    if (!this.state.events || !this.state.venues) {
      return <div>Loading...</div>;
    }

    return (
      <div>
        <h1 style={{ textAlign: 'center' }}>Event Data Generated From Django</h1>
        <div style={{ display: 'flex' }}>
          <div style={{ flex: 1 }}>
            {this.state.events.map(output => (
              <div key={output.id}>
                <hr></hr>
                <img src={output.image} style={{maxWidth: "50%"}}></img>
                <h2>{output.name}</h2>
                <p>{output.event_id}</p>
                <p>{output.price}</p>
                <p>{output.summary}</p>
                <a href={output.tickets_url}>tickets</a>
              </div>
            ))}
          </div>
          <div style={{ flex: 1 }}>
            {this.state.venues.map(output => (
              <div key={output.id}>
                <hr></hr>
                <h2>{output.name}</h2>
                <p>{output.venue_id}</p>
                <p>{output.address}</p>
                <p>{output.summary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

}

export default App;

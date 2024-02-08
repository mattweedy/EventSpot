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

  // componentDidMount() {
  //   this.fetchData('/events/');
  //   this.fetchData('/venues/');
  // }

  componentDidMount() {
    let e_data;
    let v_data;
    e_data = this.fetchData('/events/');
    v_data = this.fetchData('/venues/');
  }

  render() {
    if (!this.state.events) {
      return <div>Loading...</div>;
    }

    return (
      <div>
        <h1>Event Data Generated From Django</h1>
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
    )
  }

}

export default App;

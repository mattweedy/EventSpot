import React from 'react';
import axios from 'axios';
// import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      events: []
    };
  }

  componentDidMount() {
    let data;
    axios.get('http://localhost:8000/events/')
      .then(res => {
        data = res.data.results;
        console.log("data : ", data);
        this.setState({
           events: data
        });
      })
      .catch(err => {console.log(err)})
  }

  render() {
    if (!this.state.events) {
      return <div>Loading...</div>;
    }

    return (
      <div>
        <h1>Event Data Generated From Django</h1>
        {/* {console.log(this.state.events)} */}
        {this.state.events.map(event_data => (
          <div key={event_data.id}>
            <hr></hr>
            <img src={event_data.image} style={{maxWidth: "50%"}}></img>
            <h2>{event_data.name}</h2>
            <p>{event_data.event_id}</p>
            <p>{event_data.price}</p>
            <a href={event_data.tickets_url}>tickets</a>
          </div>
        ))}
      </div>
    )
  }

}

export default App;

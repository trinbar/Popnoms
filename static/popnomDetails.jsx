class Event extends React.Component {
  constructor() {
    super();
    console.log('hi 1');
    this.state = {
      events: []
    };
  }

  componentDidMount() {
    console.log('hi');
    fetch('/popnom_details')
      .then(res => res.json())
      .then(events => {
        this.setState({ events: events });
      });
  }

  render() {
    return (
      <div>
        <h1>Event Detail from API</h1>
        {this.state.events.map(events => {
          return (
            <ul key={events.event_id}>
              <li>ID: {event.event_id}</li>
              <li>Name: {event.name}</li>
              <li>Description: {event.description}</li>
            </ul>
          );
        })}
      </div>
    );
  }
}

ReactDOM.render(<Events />, document.getElementById('root'));

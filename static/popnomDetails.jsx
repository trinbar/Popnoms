class Event extends React.Component {
    constructor() {
        super();
        console.log('hi 1');
        this.state = {
            event: []
        };
    };
}

    componentDidMount() {
        console.log('hi 2');
        fetch('/popnom_details')
            .then(res => res.json())
            .then(event => {
                this.setState({ event: event});
            });
    }

    render() {
        return (
            <div>
                <h1>Popnom Details</h1>
                {this.state.event.map(event => {
                    return (
                    <ul key={event.name}>
                        <li>Popnom Name: {event.name.text}</li>
                        <li>Local Start Time: {event.start.local}</li>
                        <li>Local End Time: {event.end.local}</li><
                        <li>Description: {event.description.text}</li>
                        </ul>
                    );
                )}
            </div> 
        );
    }

ReactDOM.render(<Events />, document.getElementById('root'));